"""Tests del modo Día a Día (plan, estado de cada día, avisos cada 2 días, endpoints)."""

from __future__ import annotations

import json
import os
import unittest
from unittest.mock import MagicMock, patch
from urllib.parse import urlsplit

from backend import dia_a_dia, telegram_relay
from backend.irl_engine import create_irl_run
from backend.llm_proxy import LLMProxyClient
from backend.server import BadRequestError, ServerState, _handle_dia_a_dia

CASES = ("michael-carter", "samantha-lewis", "timothy-melanie-weah", "daniel-emily-johnson")
HOOK = "https://n8n.example.test/webhook/sherpas-radio"


def all_done(plan, up_to_day):
    return {s["step_id"]: list(s["required_members"]) for s in plan["steps"] if s["day"] <= up_to_day}


class PlanTests(unittest.TestCase):
    def test_plan_texts_come_verbatim_from_the_irl_engine(self) -> None:
        for case_id in CASES:
            with self.subTest(case=case_id):
                engine = create_irl_run(case_id)
                real = {s.step_id: s for s in engine.steps}
                plan = dia_a_dia.build_plan(case_id)
                self.assertTrue(plan["steps"])
                for step in plan["steps"]:
                    self.assertLessEqual(step["day"], 30)
                    self.assertEqual(step["title"], real[step["step_id"]].title)
                    self.assertEqual(step["action_plain"], real[step["step_id"]].action_plain)

    def test_why_is_short_and_grounded(self) -> None:
        for case_id in CASES:
            engine = create_irl_run(case_id)
            for step in dia_a_dia.build_plan(case_id)["steps"]:
                with self.subTest(case=case_id, step=step["step_id"]):
                    self.assertLess(len(step["why"]), 160)
                    inertia = engine._step_inertia_snapshot(next(s for s in engine.steps if s.step_id == step["step_id"]), step["day"] + 1)
                    if inertia.get("label"):
                        self.assertIn(inertia["label"], step["why"])
                    elif step["why"]:
                        self.assertIn(step["why"][len("Para "):-1], next(s for s in engine.steps if s.step_id == step["step_id"]).action_plain)

    def test_couple_members_use_first_names(self) -> None:
        plan = dia_a_dia.build_plan("timothy-melanie-weah")
        self.assertTrue(plan["is_couple"])
        self.assertEqual(plan["members"], [{"id": "A", "name": "Timothy"}, {"id": "B", "name": "Melanie"}])


class DayStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = dia_a_dia.build_plan("michael-carter")  # pasos en Días 0, 3, 14 y 30

    def test_task_days_show_the_step(self) -> None:
        st = dia_a_dia.day_status(self.plan, 3, {})
        self.assertEqual(st["mode"], "task")
        self.assertEqual([s["day"] for s in st["today"]], [3])

    def test_empty_day_with_everything_done_is_wait(self) -> None:
        st = dia_a_dia.day_status(self.plan, 5, all_done(self.plan, 3))
        self.assertEqual(st["mode"], "wait")
        self.assertEqual(st["next_day"], 14)
        self.assertFalse(st["reminder_due"])

    def test_empty_day_with_something_pending_reminds(self) -> None:
        st = dia_a_dia.day_status(self.plan, 5, {})
        self.assertEqual(st["mode"], "pending")
        self.assertEqual({p["day"] for p in st["pending"]}, {0, 3})
        self.assertEqual(st["pending"][0]["missing_names"], ["Michael"])

    def test_reminders_every_two_days_from_the_oldest_pending(self) -> None:
        due = [d for d in range(0, 14) if dia_a_dia.day_status(self.plan, d, {})["reminder_due"]]
        self.assertEqual(due, [2, 4, 6, 8, 10, 12])

    def test_couple_step_is_pending_until_both_confirm(self) -> None:
        plan = dia_a_dia.build_plan("timothy-melanie-weah")
        joint = next(s for s in plan["steps"] if s["day"] == 3 and s["required_members"] == ["A", "B"])
        done = all_done(plan, 0)
        done[joint["step_id"]] = ["A"]
        st = dia_a_dia.day_status(plan, 4, done)
        pending = {p["step_id"]: p for p in st["pending"]}
        self.assertEqual(pending[joint["step_id"]]["missing_names"], ["Melanie"])


class NotificationTests(unittest.TestCase):
    def test_task_day_message_includes_step_and_why(self) -> None:
        n = dia_a_dia.notification_for_day("michael-carter", 0)
        plan = dia_a_dia.build_plan("michael-carter")
        self.assertEqual(n["kind"], "milestone")
        self.assertIn(plan["steps"][0]["title"], n["message_plain"])
        self.assertIn("Por qué:", n["message_plain"])
        self.assertNotRegex(n["target_owner"], r"Owner\s+[AB]")

    def test_reminder_names_who_is_missing(self) -> None:
        n = dia_a_dia.notification_for_day("timothy-melanie-weah", 2)
        self.assertEqual(n["kind"], "overdue_insistence")
        self.assertIn("Falta: Melanie", n["message_plain"])

    def test_nothing_on_odd_days_or_when_all_done(self) -> None:
        self.assertIsNone(dia_a_dia.notification_for_day("michael-carter", 1))
        plan = dia_a_dia.build_plan("michael-carter")
        self.assertIsNone(dia_a_dia.notification_for_day("michael-carter", 6, all_done(plan, 3)))

    def test_day_out_of_range(self) -> None:
        with self.assertRaises(ValueError):
            dia_a_dia.notification_for_day("michael-carter", 31)


class EndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = ServerState(llm_client=LLMProxyClient(team_key="", transport="urllib"))
        self.sent: list[dict] = []

        def fake_urlopen(req, timeout):
            self.sent.append(json.loads(req.data.decode("utf-8")))
            response = MagicMock()
            response.__enter__.return_value = response
            return response

        self.fake = fake_urlopen

    def call(self, method, path, body=None, env=None):
        with patch.dict(os.environ, env if env is not None else {"N8N_WEBHOOK_URL": HOOK}, clear=True), \
                patch("backend.server.load_env_file"), \
                patch("backend.server.urllib.request.urlopen", side_effect=self.fake):
            return _handle_dia_a_dia(method, urlsplit(path), body or {}, self.state)

    def test_get_plan(self) -> None:
        status, data = self.call("GET", "/api/dia-a-dia/samantha-lewis")
        self.assertEqual(status, 200)
        self.assertEqual(data["case_id"], "samantha-lewis")

    def test_day_with_notify_sends_one_message(self) -> None:
        status, data = self.call("POST", "/api/dia-a-dia/michael-carter/day", {"day": 3, "completed": {}, "notify": True})
        self.assertEqual(status, 200)
        self.assertEqual(data["status"]["mode"], "task")
        self.assertTrue(data["notification"]["sent"])
        self.assertTrue(data["notification"]["configured"])
        self.assertEqual(len(self.sent), 1)

    def test_day_without_notify_sends_nothing(self) -> None:
        _, data = self.call("POST", "/api/dia-a-dia/michael-carter/day", {"day": 2, "completed": {}})
        self.assertTrue(data["status"]["reminder_due"])
        self.assertIsNone(data["notification"])
        self.assertEqual(self.sent, [])

    def test_without_n8n_reports_not_configured(self) -> None:
        _, data = self.call("POST", "/api/dia-a-dia/michael-carter/day", {"day": 0, "notify": True}, env={})
        self.assertFalse(data["notification"]["configured"])
        self.assertFalse(data["notification"]["sent"])

    def test_bad_input(self) -> None:
        with self.assertRaises(BadRequestError):
            self.call("POST", "/api/dia-a-dia/michael-carter/day", {"day": 40})
        with self.assertRaises(BadRequestError):
            self.call("POST", "/api/dia-a-dia/michael-carter/day", {"day": 1, "completed": {"x": "A"}})
        with self.assertRaises(KeyError):
            self.call("GET", "/api/dia-a-dia/michael-carter/otra")


class SchedulerCadenceTests(unittest.TestCase):
    def test_overdue_insistence_only_every_two_days(self) -> None:
        state = ServerState(llm_client=LLMProxyClient(team_key="", transport="urllib"))
        now = [1_000_000.0]
        emitted: list[dict] = []
        scheduler = telegram_relay.NotificationScheduler(
            state, lambda n, r: emitted.append(n), day_seconds=10, max_day=12, clock=lambda: now[0], notify_days=[]
        )
        with patch("backend.server.time.time", return_value=now[0]):
            state.runs.create("michael-carter")
        for _ in range(13):
            scheduler.tick()
            now[0] += 10
        overdue = [n for n in emitted if n["kind"] == "overdue_insistence"]
        self.assertTrue(overdue)
        self.assertTrue(all(int(n["days_overdue"]) % 2 == 0 for n in overdue))


if __name__ == "__main__":
    unittest.main()
