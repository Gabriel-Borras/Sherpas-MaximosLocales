"""Tests de los mensajes de demo de La Radio (botones Día 0/3/14/30 y caída de bolsa)."""

from __future__ import annotations

import json
import os
import re
import unittest
from unittest.mock import MagicMock, patch
from urllib.parse import urlsplit

from backend import radio_demo
from backend.llm_proxy import LLMProxyClient
from backend.notifications import NotificationEngine
from backend.server import BadRequestError, ServerState, _handle_telegram

CASES = ("michael-carter", "samantha-lewis", "timothy-melanie-weah", "daniel-emily-johnson")
HOOK = "https://n8n.example.test/webhook/sherpas-radio"


class DayPayloadTests(unittest.TestCase):
    def test_every_case_has_one_message_per_demo_day(self) -> None:
        for case_id in CASES:
            for day in radio_demo.DEMO_DAYS:
                with self.subTest(case=case_id, day=day):
                    p = radio_demo.day_payload(case_id, day)
                    self.assertEqual(p["day"], day)
                    self.assertEqual(p["case_id"], case_id)
                    self.assertTrue(p["message_plain"].startswith("• "))
                    # Nunca "Owner A/B" en el destinatario: el aviso es para todo el hogar.
                    self.assertIsNone(re.search(r"Owner\s+[AB]\b", p["target_owner"]))

    def test_ids_are_unique_so_n8n_never_dedupes_a_click(self) -> None:
        a = radio_demo.day_payload("michael-carter", 3)
        b = radio_demo.day_payload("michael-carter", 3)
        self.assertNotEqual(a["notification_id"], b["notification_id"])

    def test_invalid_day(self) -> None:
        with self.assertRaises(ValueError):
            radio_demo.day_payload("michael-carter", 5)


class ShockPayloadTests(unittest.TestCase):
    def test_matches_april_2025_and_uses_real_recovery(self) -> None:
        p = radio_demo.shock_payload("daniel-emily-johnson", 8)
        self.assertEqual(p["matched_event_date"], "2025-04-02")
        self.assertIn("abril de 2025", p["anti_panic_message_plain"])
        self.assertIn("8,1 %", p["anti_panic_message_plain"])
        self.assertIn("61 días", p["anti_panic_message_plain"])
        self.assertIn("buen camino", p["anti_panic_message_plain"])
        self.assertEqual(p["type"], "macro_shock_radio")

    def test_every_number_comes_from_the_case_data(self) -> None:
        for case_id in CASES:
            with self.subTest(case=case_id):
                engine = NotificationEngine(case_id)
                household = engine.case_data["investment_analysis"]["key_metrics"]["performanceAnalysis"]["household"]
                text = radio_demo.shock_payload(case_id, 8)["anti_panic_message_plain"]
                self.assertIn(f"{household['maxDrawdownRecoveryDays']} días", text)
                self.assertIn(f"{abs(household['maxDrawdown3y']) * 100:.1f}".replace(".", ","), text)

    def test_small_drop_matches_a_small_real_event(self) -> None:
        p = radio_demo.shock_payload("michael-carter", 4)
        self.assertEqual(p["matched_event_date"], "2023-07-26")
        self.assertIn("15 días", p["anti_panic_message_plain"])  # recuperación real de ese evento

    def test_invalid_drop(self) -> None:
        with self.assertRaises(ValueError):
            radio_demo.shock_payload("michael-carter", 0)


class DemoEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = ServerState(llm_client=LLMProxyClient(team_key="", transport="urllib"))
        self.sent: list[dict] = []

        def fake_urlopen(req, timeout):
            self.sent.append(json.loads(req.data.decode("utf-8")))
            response = MagicMock()
            response.__enter__.return_value = response
            return response

        self.fake_urlopen = fake_urlopen
        self.env = {"N8N_WEBHOOK_URL": HOOK, "SHERPAS_ENABLE_TELEGRAM_TEST": "1"}

    def call(self, route: str, body: dict):
        with patch.dict(os.environ, self.env, clear=True), patch("backend.server.load_env_file"), \
                patch("backend.server.urllib.request.urlopen", side_effect=self.fake_urlopen):
            return _handle_telegram("POST", urlsplit(route), body, self.state)

    def test_day_button_sends_exactly_one_message(self) -> None:
        status, data = self.call("/api/telegram/demo/day", {"case_id": "timothy-melanie-weah", "day": 14})
        self.assertEqual(status, 200)
        self.assertTrue(data["sent"])
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(self.sent[0]["day"], 14)

    def test_shock_button_sends_exactly_one_message(self) -> None:
        status, data = self.call("/api/telegram/demo/shock", {"case_id": "michael-carter"})
        self.assertEqual(status, 200)
        self.assertEqual(len(self.sent), 1)
        self.assertIn("62 días", data["preview"])

    def test_bad_input(self) -> None:
        with self.assertRaises(BadRequestError):
            self.call("/api/telegram/demo/day", {"day": 3})
        with self.assertRaises(BadRequestError):
            self.call("/api/telegram/demo/day", {"case_id": "michael-carter", "day": "x"})

    def test_hidden_when_demo_disabled(self) -> None:
        self.env = {"N8N_WEBHOOK_URL": HOOK}
        with self.assertRaises(KeyError):
            self.call("/api/telegram/demo/day", {"case_id": "michael-carter", "day": 0})
        with patch.dict(os.environ, self.env, clear=True), patch("backend.server.load_env_file"):
            _, cfg = _handle_telegram("GET", urlsplit("/api/telegram/config"), {}, self.state)
        self.assertFalse(cfg["demo_buttons"])


if __name__ == "__main__":
    unittest.main()
