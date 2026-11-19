"""Tests for the backend -> n8n -> Telegram delivery plumbing."""

from __future__ import annotations

import json
import os
import tempfile
import threading
import unittest
from unittest.mock import MagicMock, patch
from urllib import error
from urllib.parse import urlsplit

from backend import telegram_relay
from backend.llm_proxy import LLMProxyClient
from backend.server import (
    ServerState,
    _emit_n8n_webhook,
    _handle_telegram,
    _post_n8n,
)

HOOK = "https://n8n.example.test/webhook/sherpas-radio"


def _state() -> ServerState:
    return ServerState(llm_client=LLMProxyClient(team_key="", transport="urllib"))


class SecretHeaderTests(unittest.TestCase):
    def _capture(self):
        sent = []

        def fake_urlopen(req, timeout):
            sent.append((req, timeout))
            response = MagicMock()
            response.__enter__.return_value = response
            return response

        return sent, fake_urlopen

    def test_secret_header_is_sent_only_when_configured(self) -> None:
        sent, fake = self._capture()
        with patch.dict(os.environ, {"N8N_WEBHOOK_URL": HOOK, "N8N_WEBHOOK_SECRET": "s3cret"}, clear=True), \
                patch("backend.server.urllib.request.urlopen", side_effect=fake):
            self.assertTrue(_post_n8n({"a": 1}))
        self.assertEqual(sent[0][0].get_header("X-sherpas-secret"), "s3cret")
        self.assertEqual(sent[0][1], 2)

        sent.clear()
        with patch.dict(os.environ, {"N8N_WEBHOOK_URL": HOOK}, clear=True), \
                patch("backend.server.load_env_file"), \
                patch("backend.server.urllib.request.urlopen", side_effect=fake):
            self.assertTrue(_post_n8n({"a": 1}))
        self.assertIsNone(sent[0][0].get_header("X-sherpas-secret"))

    def test_post_returns_false_without_url_or_on_failure(self) -> None:
        with patch.dict(os.environ, {}, clear=True), patch("backend.server.load_env_file"):
            self.assertFalse(_post_n8n({"a": 1}))
        with patch.dict(os.environ, {"N8N_WEBHOOK_URL": HOOK}, clear=True), \
                patch("backend.server.urllib.request.urlopen", side_effect=error.URLError("down")):
            self.assertFalse(_post_n8n({"a": 1}))


class OutboxTests(unittest.TestCase):
    def test_failed_delivery_is_parked_and_replayed_in_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
                patch.dict(os.environ, {"N8N_WEBHOOK_URL": HOOK, "SHERPAS_OUTBOX_DIR": tmp}, clear=True):
            attempted = threading.Event()

            def failing(*args, **kwargs):
                attempted.set()
                raise error.URLError("down")

            with patch("backend.server.urllib.request.urlopen", side_effect=failing):
                _emit_n8n_webhook({"notification_id": "n1"})
                _emit_n8n_webhook({"notification_id": "n2"})
                self.assertTrue(attempted.wait(1))
                for _ in range(100):
                    if telegram_relay.pending_count() == 2:
                        break
                    threading.Event().wait(0.02)
            self.assertEqual(telegram_relay.pending_count(), 2)

            delivered: list[str] = []

            def send(payload):
                delivered.append(payload["notification_id"])
                return True

            self.assertEqual(telegram_relay.drain_outbox(send), 2)
            self.assertEqual(sorted(delivered), ["n1", "n2"])
            self.assertEqual(telegram_relay.pending_count(), 0)

    def test_drain_stops_at_first_failure_and_keeps_the_rest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"SHERPAS_OUTBOX_DIR": tmp}, clear=True):
            for i in range(3):
                telegram_relay.record_failure({"notification_id": f"n{i}"})
            calls = []

            def send(payload):
                calls.append(payload["notification_id"])
                return payload["notification_id"] == "n0"

            self.assertEqual(telegram_relay.drain_outbox(send), 1)
            self.assertEqual(calls, ["n0", "n1"])
            self.assertEqual(telegram_relay.pending_count(), 2)

    def test_outbox_is_noop_when_disabled(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(telegram_relay.outbox_path())
            self.assertFalse(telegram_relay.record_failure({"a": 1}))
            self.assertEqual(telegram_relay.pending_count(), 0)
            self.assertEqual(telegram_relay.drain_outbox(lambda p: True), 0)


class SchedulerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = _state()
        self.clock_now = [1_000_000.0]
        self.emitted: list[tuple[str, dict]] = []
        self.scheduler = telegram_relay.NotificationScheduler(
            self.state,
            lambda notification, run_id: self.emitted.append((run_id, notification)),
            day_seconds=86400,
            max_day=40,
            clock=lambda: self.clock_now[0],
        )

    def _create_run(self, case_id="michael-carter") -> str:
        with patch("backend.server.time.time", return_value=self.clock_now[0]):
            run_id, _ = self.state.runs.create(case_id)
        return run_id

    def test_day_zero_is_emitted_once_and_never_repeated(self) -> None:
        self._create_run()
        first = self.scheduler.tick()
        self.assertGreater(first, 0)
        self.assertEqual(self.scheduler.tick(), 0)
        ids = [n["notification_id"] for _, n in self.emitted]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(n["day"] == 0 for _, n in self.emitted))

    def test_real_time_advances_plan_days_and_emits_new_alerts(self) -> None:
        run_id = self._create_run()
        self.scheduler.tick()
        engine, _ = self.state.runs.get(run_id)
        self.assertEqual(engine.current_day, 0)

        self.clock_now[0] += 3 * 86400 + 5
        emitted_day3 = self.scheduler.tick()
        self.assertEqual(engine.current_day, 3)
        self.assertGreater(emitted_day3, 0)
        self.assertTrue(any(n["day"] == 3 for _, n in self.emitted))

        self.clock_now[0] += 27 * 86400
        self.scheduler.tick()
        self.assertEqual(engine.current_day, 30)
        self.assertTrue(any(n["day"] == 30 for _, n in self.emitted))

    def test_plan_day_is_capped_by_max_day(self) -> None:
        run_id = self._create_run()
        self.clock_now[0] += 1000 * 86400
        self.scheduler.tick()
        engine, _ = self.state.runs.get(run_id)
        self.assertEqual(engine.current_day, 40)

    def test_accelerated_demo_clock(self) -> None:
        scheduler = telegram_relay.NotificationScheduler(
            self.state, lambda n, r: self.emitted.append((r, n)), day_seconds=60, clock=lambda: self.clock_now[0]
        )
        run_id = self._create_run()
        self.clock_now[0] += 14 * 60
        scheduler.tick()
        engine, _ = self.state.runs.get(run_id)
        self.assertEqual(engine.current_day, 14)

    def test_every_run_is_handled_and_drain_is_called(self) -> None:
        drained = []
        scheduler = telegram_relay.NotificationScheduler(
            self.state, lambda n, r: self.emitted.append((r, n)), clock=lambda: self.clock_now[0],
            drain=lambda: drained.append(1) or 0,
        )
        self._create_run("michael-carter")
        self._create_run("timothy-melanie-weah")
        scheduler.tick()
        self.assertEqual({run for run, _ in self.emitted}, {"irl-1", "irl-2"})
        self.assertEqual(drained, [1])

    def test_scheduler_thread_starts_and_stops(self) -> None:
        ticked = threading.Event()
        scheduler = telegram_relay.NotificationScheduler(self.state, lambda n, r: None)
        scheduler.tick = lambda: ticked.set() or 0  # type: ignore[method-assign]
        scheduler.start(0.01)
        self.assertTrue(ticked.wait(1))
        self.assertTrue(scheduler.running)
        scheduler.stop()

    def test_scheduler_interval_parsing(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(telegram_relay.scheduler_interval(), 0.0)
        with patch.dict(os.environ, {"SHERPAS_SCHEDULER_INTERVAL": "30"}, clear=True):
            self.assertEqual(telegram_relay.scheduler_interval(), 30.0)
        with patch.dict(os.environ, {"SHERPAS_SCHEDULER_INTERVAL": "abc"}, clear=True):
            self.assertEqual(telegram_relay.scheduler_interval(), 0.0)


class TelegramEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = _state()

    def test_config_reports_state_without_secrets(self) -> None:
        with patch.dict(
            os.environ,
            {"N8N_WEBHOOK_URL": HOOK, "N8N_WEBHOOK_SECRET": "s3cret", "TELEGRAM_BOT_USERNAME": "@MiBot"},
            clear=True,
        ):
            status, data = _handle_telegram("GET", urlsplit("/api/telegram/config"), {}, self.state)
        self.assertEqual(status, 200)
        self.assertTrue(data["n8n_configured"])
        self.assertTrue(data["secret_configured"])
        self.assertEqual(data["telegram_bot_username"], "MiBot")
        self.assertEqual(data["telegram_deep_link_template"], "https://t.me/MiBot?start=<case_id>_<owner>")
        self.assertNotIn("s3cret", json.dumps(data))
        self.assertNotIn(HOOK, json.dumps(data))

    def test_test_endpoint_is_disabled_by_default(self) -> None:
        with patch.dict(os.environ, {"N8N_WEBHOOK_URL": HOOK}, clear=True), self.assertRaises(KeyError):
            _handle_telegram("POST", urlsplit("/api/telegram/test"), {}, self.state)

    def test_test_endpoint_emits_message_when_enabled(self) -> None:
        sent = []
        delivered = threading.Event()

        def fake_urlopen(req, timeout):
            sent.append(json.loads(req.data.decode("utf-8")))
            delivered.set()
            response = MagicMock()
            response.__enter__.return_value = response
            return response

        env = {"N8N_WEBHOOK_URL": HOOK, "SHERPAS_ENABLE_TELEGRAM_TEST": "1"}
        with patch.dict(os.environ, env, clear=True), \
                patch("backend.server.urllib.request.urlopen", side_effect=fake_urlopen):
            status, data = _handle_telegram(
                "POST", urlsplit("/api/telegram/test"), {"case_id": "michael-carter", "owner": "A"}, self.state
            )
            self.assertTrue(delivered.wait(1))
        self.assertEqual(status, 202)
        self.assertEqual(sent[0]["case_id"], "michael-carter")
        self.assertEqual(sent[0]["target_owner"], "A")
        self.assertEqual(sent[0]["kind"], "test")

    def test_test_endpoint_requires_n8n_url(self) -> None:
        from backend.server import BadRequestError

        with patch.dict(os.environ, {"SHERPAS_ENABLE_TELEGRAM_TEST": "1"}, clear=True), \
                patch("backend.server.load_env_file"), self.assertRaises(BadRequestError):
            _handle_telegram("POST", urlsplit("/api/telegram/test"), {}, self.state)

    def test_unknown_route_is_not_found(self) -> None:
        with self.assertRaises(KeyError):
            _handle_telegram("GET", urlsplit("/api/telegram/nope"), {}, self.state)


if __name__ == "__main__":
    unittest.main()
