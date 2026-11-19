"""End-to-end HTTP demo tests across all 4 official Sherpa Financiero cases."""

from __future__ import annotations

import json
import threading
import unittest
from urllib import error, request

from backend.behavioral_narrator import (
    extract_case_allowed_numbers,
    load_case,
    verify_text_numbers_against_case,
)
from backend.llm_proxy import LLMProxyClient
from backend.server import create_server


CASE_CONFIGS = {
    "michael-carter": {
        "dual": False,
        "partners": (),
        "option_id": "umbrella",
    },
    "samantha-lewis": {
        "dual": False,
        "partners": (),
        "option_id": "home_insurance",
    },
    "timothy-melanie-weah": {
        "dual": True,
        "partners": ("Timothy", "Melanie"),
        "option_id": "pay_card_18k",
    },
    "daniel-emily-johnson": {
        "dual": True,
        "partners": ("Daniel", "Emily"),
        "option_id": "life_insurance",
    },
}


class E2EDemoTests(unittest.TestCase):
    """Exercise the complete demo flow against the real HTTP server without TEAM_KEY."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server(
            port=0,
            llm_client=LLMProxyClient(team_key="", transport="urllib"),
        )
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def api_request(self, method: str, path: str, payload: object = None):
        """Send an HTTP request and return (status, headers, parsed_body)."""
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        req = request.Request(
            f"{self.base_url}{path}",
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            response = request.urlopen(req)
        except error.HTTPError as exc:
            response = exc
        with response:
            raw = response.read()
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type and raw:
                parsed = json.loads(raw)
            elif "text" in content_type or "calendar" in content_type:
                parsed = raw.decode("utf-8")
            else:
                parsed = raw
            return response.status, response.headers, parsed

    def assert_zero_invented_numbers(self, case_id: str, payload: dict) -> None:
        """Verify that every number in an AI payload exists in the grounded case."""
        allowed = extract_case_allowed_numbers(load_case(case_id))
        verified, unverified = verify_text_numbers_against_case(
            json.dumps(payload, ensure_ascii=False),
            allowed,
        )
        self.assertTrue(
            verified,
            f"Unverified numbers detected for {case_id}: {unverified}",
        )

    def _run_full_case_e2e(self, case_id: str) -> None:
        config = CASE_CONFIGS[case_id]
        dual = config["dual"]
        option_id = config["option_id"]

        # 1. GET /api/cases/{id}
        status, _, case_doc = self.api_request("GET", f"/api/cases/{case_id}")
        self.assertEqual(status, 200)
        self.assertEqual(case_doc["meta"]["slug"], case_id)
        self.assertTrue({"score", "persona", "projections", "facts"} <= set(case_doc))

        # 2. POST /api/ai/reframe in ES and EN (blind_spot_contrast + 0 invented numbers)
        for lang in ("ES", "EN"):
            status, _, reframe = self.api_request(
                "POST",
                "/api/ai/reframe",
                {
                    "case_id": case_id,
                    "topic": "overview",
                    "lens": "both",
                    "lang": lang,
                    "context": {
                        "top_rank": "O3",
                        "thermometer": 80,
                        "subjective": "market drop",
                        "concerns": ["O3", "O1"],
                    },
                },
            )
            self.assertEqual(status, 200)
            self.assertEqual(reframe["lang"], lang)
            self.assertFalse(reframe["used_llm"])
            self.assertTrue(reframe["llm_fallback_used"])
            self.assertEqual(reframe["fallback_reason"], "missing_team_key")
            self.assertTrue(reframe["verified_numbers_only"])
            self.assertIn("blind_spot_contrast", reframe)
            expected_band = "alto" if lang == "ES" else "high"
            self.assertEqual(
                reframe["blind_spot_contrast"]["thermometer_band"], expected_band
            )
            self.assert_zero_invented_numbers(case_id, reframe)

        # 3. POST /api/ai/pact (anxiety_gap with thermometer A/B + 0 invented numbers)
        for lang in ("ES", "EN"):
            status, _, pact = self.api_request(
                "POST",
                "/api/ai/pact",
                {
                    "case_id": case_id,
                    "lang": lang,
                    "member_a_votes": {
                        "top_fears": ["O1", "O3"],
                        "risk_choice": "Growth",
                        "thermometer": 80,
                    },
                    "member_b_votes": {
                        "top_fears": ["O1", "O2"],
                        "risk_choice": "Moderate",
                        "thermometer": 30,
                    },
                },
            )
            self.assertEqual(status, 200)
            self.assertEqual(pact["lang"], lang)
            self.assertFalse(pact["used_llm"])
            self.assertEqual(pact["llm_fallback_used"], dual)
            self.assertTrue(pact["verified_numbers_only"])
            if dual:
                gap = pact.get("anxiety_gap")
                self.assertIsInstance(gap, dict)
                self.assertTrue(gap["available"])
                self.assertEqual(gap["member_a_thermometer"], 80)
                self.assertEqual(gap["member_b_thermometer"], 30)
                self.assertEqual(gap["gap"], 50)
                self.assertIn(gap["band"], ("alta", "alto", "high"))
            else:
                self.assertIsNone(pact.get("anxiety_gap"))
            self.assert_zero_invented_numbers(case_id, pact)

        # 4. POST /api/ai/brief in ES and EN (0 invented numbers)
        for lang in ("ES", "EN"):
            status, _, brief = self.api_request(
                "POST",
                "/api/ai/brief",
                {
                    "case_id": case_id,
                    "lang": lang,
                    "fear_ranking": ["O1", "O2"],
                    "subjective_concerns": "Market volatility",
                },
            )
            self.assertEqual(status, 200)
            self.assertEqual(brief["lang"], lang)
            self.assertFalse(brief["used_llm"])
            self.assertTrue(brief["llm_fallback_used"])
            self.assertTrue(brief["verified_numbers_only"])
            self.assertTrue(brief.get("markdown_brief"))
            self.assert_zero_invented_numbers(case_id, brief)

        # 5. Basecamp session (/api/sessions)
        status, _, session = self.api_request(
            "POST", "/api/sessions", {"case_id": case_id}
        )
        self.assertEqual(status, 201)
        session_id = session["session_id"]
        prefix = f"/api/sessions/{session_id}"

        self.assertEqual(self.api_request("GET", prefix)[0], 200)
        self.assertEqual(
            self.api_request("POST", f"{prefix}/quest", {"ranked_concerns": ["O1"]})[0],
            200,
        )

        if dual:
            partner_a, partner_b = config["partners"]
            status, _, cordada_a = self.api_request(
                "POST",
                f"{prefix}/cordada",
                {"partner": partner_a, "choices": [option_id]},
            )
            self.assertEqual(status, 200)
            self.assertTrue(cordada_a["blind_pending"])

            status, _, cordada_b = self.api_request(
                "POST",
                f"{prefix}/cordada",
                {"partner": partner_b, "choices": [option_id]},
            )
            self.assertEqual(status, 200)
            self.assertFalse(cordada_b["blind_pending"])

        status, _, preview = self.api_request(
            "POST", f"{prefix}/mountain/preview", {"option_id": option_id}
        )
        self.assertEqual(status, 200)
        self.assertEqual(preview["option_id"], option_id)

        status, _, decided = self.api_request(
            "POST", f"{prefix}/mountain/decide", {"option_id": option_id}
        )
        self.assertEqual(status, 200)
        self.assertFalse(decided.get("blocked", False))

        status, _, session_brief = self.api_request("GET", f"{prefix}/advisor-brief")
        self.assertEqual(status, 200)
        self.assertTrue({"fears", "ranked_concerns", "step_1", "views"} <= set(session_brief))

        # 6. Run IRL: Day 0, 3, 14, 30
        status, _, created_irl = self.api_request(
            "POST", "/api/irl", {"case_id": case_id}
        )
        self.assertEqual(status, 201)
        run_id = created_irl["run_id"]

        for day in (0, 3, 14, 30):
            if day > 0:
                status, _, adv = self.api_request(
                    "POST", f"/api/irl/{run_id}/advance", {"day": day}
                )
                self.assertEqual(status, 200)
                self.assertEqual(adv["current_day"], day)

            status, _, run_state = self.api_request("GET", f"/api/irl/{run_id}")
            self.assertEqual(status, 200)
            active_steps = run_state["timeline_view"]["active_steps"]
            day_steps = [s for s in active_steps if s.get("day") == day]
            self.assertTrue(day_steps, f"No active IRL steps found for {case_id} on day {day}")
            for step in day_steps:
                required_members = step.get("required_members") or ["single"]
                checked = None
                for member in required_members:
                    check_payload = {"step_id": step["step_id"]}
                    if member != "single":
                        check_payload["member"] = member
                    status, _, checked = self.api_request(
                        "POST", f"/api/irl/{run_id}/check", check_payload
                    )
                    self.assertEqual(status, 200)
                self.assertIsNotNone(checked)
                self.assertTrue(checked["is_completed"])

        status, _, inertia = self.api_request("GET", f"/api/irl/{run_id}/inertia")
        self.assertEqual(status, 200)
        self.assertIn("active_levers", inertia)

        # 7. La Radio del Sherpa + .ics download
        status, _, radio = self.api_request("GET", f"/api/radio/{run_id}")
        self.assertEqual(status, 200)
        self.assertIn("milestones", radio)
        self.assertEqual(len(radio["macro_shocks"]), 11)

        status, _, shock = self.api_request(
            "POST",
            f"/api/radio/{run_id}/shock",
            {"alert_type": "tariffs", "headline": "Aranceles y caida bursatil"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(shock["kind"], "macro_shock")

        status, headers, calendar = self.api_request("GET", f"/api/radio/{run_id}/ics")
        self.assertEqual(status, 200)
        self.assertTrue(headers["Content-Type"].startswith("text/calendar"))
        self.assertIn("BEGIN:VCALENDAR", calendar)
        self.assertIn("END:VCALENDAR", calendar)

    def test_e2e_michael_carter(self) -> None:
        self._run_full_case_e2e("michael-carter")

    def test_e2e_samantha_lewis(self) -> None:
        self._run_full_case_e2e("samantha-lewis")

    def test_e2e_timothy_melanie_weah(self) -> None:
        self._run_full_case_e2e("timothy-melanie-weah")

    def test_e2e_daniel_emily_johnson(self) -> None:
        self._run_full_case_e2e("daniel-emily-johnson")


if __name__ == "__main__":
    unittest.main()
