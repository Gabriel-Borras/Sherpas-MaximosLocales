"""HTTP integration tests for the unified deterministic server."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from urllib import error, request
from urllib.parse import urlsplit
from unittest.mock import MagicMock, patch

from backend.behavioral_narrator import (
    extract_case_allowed_numbers,
    load_case,
    verify_text_numbers_against_case,
)
from backend.llm_proxy import LLMProxyClient
from backend.mcp_client import CaseNotFoundError
from backend.server import (
    BadRequestError,
    ServerState,
    _handle_ai,
    _handle_irl,
    _handle_radio,
    _handle_rooms,
    _n8n_webhook_url,
    create_server,
)


ROOT = Path(__file__).resolve().parent.parent


class UnifiedServerTests(unittest.TestCase):
    """Exercise every public route against one real threaded HTTP server."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tempdir = tempfile.TemporaryDirectory()
        frontend = Path(cls.tempdir.name) / "frontend"
        frontend.mkdir()
        (frontend / "index.html").write_text("<h1>Sherpa</h1>", encoding="utf-8")
        (frontend / "app.js").write_text("console.log('sherpa');", encoding="utf-8")

        # An explicitly empty key makes the no-network deterministic path
        # independent from a developer's local .env file.
        cls.server = create_server(
            port=0,
            frontend_dir=frontend,
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
        cls.tempdir.cleanup()

    def api_request(self, method: str, path: str, payload=None):
        """Send one request and return status, headers and JSON/text payload."""
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

    def test_health_static_files_cors_and_static_fallback(self) -> None:
        status, headers, body = self.api_request("GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"status": "ok"})
        self.assertEqual(headers["Access-Control-Allow-Origin"], "*")

        status, headers, body = self.api_request("GET", "/")
        self.assertEqual(status, 200)
        self.assertEqual(body, "<h1>Sherpa</h1>")
        self.assertIn("text/html", headers["Content-Type"])

        status, headers, body = self.api_request("GET", "/app.js")
        self.assertEqual(status, 200)
        self.assertEqual(body, "console.log('sherpa');")
        self.assertIn("javascript", headers["Content-Type"])

        for path in ("/missing.css", "/%2e%2e/backend/server.py"):
            with self.subTest(path=path):
                status, _, body = self.api_request("GET", path)
                self.assertEqual(status, 404)
                self.assertEqual(body["error"], "not_found")

        # A deployment without a frontend directory still answers with a JSON
        # API-style 404 instead of exposing a filesystem exception.
        missing_frontend = Path(self.tempdir.name) / "frontend-missing"
        fallback_server = create_server(port=0, frontend_dir=missing_frontend)
        fallback_thread = threading.Thread(
            target=fallback_server.serve_forever, daemon=True
        )
        fallback_thread.start()
        try:
            with self.assertRaises(error.HTTPError) as raised:
                request.urlopen(
                    f"http://127.0.0.1:{fallback_server.server_port}/"
                )
            self.assertEqual(raised.exception.code, 404)
            self.assertEqual(json.load(raised.exception)["error"], "not_found")
        finally:
            fallback_server.shutdown()
            fallback_server.server_close()
            fallback_thread.join()

    def test_cases_expedition_aliases_and_session_routes(self) -> None:
        status, _, cases = self.api_request("GET", "/api/cases")
        self.assertEqual(status, 200)
        self.assertIn("michael-carter", {case["id"] for case in cases["cases"]})
        michael_summary = next(
            case for case in cases["cases"] if case["id"] == "michael-carter"
        )
        self.assertTrue(
            {"id", "name", "score", "status", "household_type"}
            <= set(michael_summary)
        )
        self.assertNotIn("meta", michael_summary)

        # No display mode means the literal document consumed by cases-data.js,
        # not TimelineEngine's normalised overview.
        status, _, raw_case = self.api_request("GET", "/api/cases/michael-carter")
        self.assertEqual(status, 200)
        self.assertEqual(
            set(raw_case),
            {
                "meta",
                "score",
                "persona",
                "projections",
                "goals",
                "facts",
                "savingsWaterfall",
                "shocks",
                "performanceSummary",
            },
        )
        self.assertEqual(raw_case["meta"]["slug"], "michael-carter")
        self.assertTrue(
            {"published_score", "pillars", "top_moves", "combined_moves"}
            <= set(raw_case["score"])
        )
        self.assertTrue(
            {"objectiveConcerns", "tensions"} <= set(raw_case["persona"])
        )
        self.assertIn("yearly", raw_case["projections"])
        self.assertNotIn("mode", raw_case)
        source = (ROOT / "frontend" / "cases-data.js").read_text(encoding="utf-8")
        marker = "const CASES_DATA = "
        start = source.index(marker) + len(marker)
        official_cases, _ = json.JSONDecoder().raw_decode(source[start:])
        self.assertEqual(raw_case, official_cases["michael-carter"])

        status, _, case = self.api_request("GET", "/api/cases/michael-carter?mode=math")
        self.assertEqual(status, 200)
        self.assertEqual(case["mode"], "math")
        self.assertEqual(case["id"], "michael-carter")

        status, _, overview = self.api_request(
            "GET", "/api/cases/michael-carter/overview"
        )
        self.assertEqual(status, 200)
        self.assertEqual(overview["mode"], "plain")
        self.assertIn("views", overview)

        status, _, expedition = self.api_request(
            "POST", "/api/expedition", {"case_id": "michael-carter"}
        )
        self.assertEqual(status, 201)
        expedition_id = expedition["session_id"]
        prefix = f"/api/expedition/{expedition_id}"

        self.assertEqual(self.api_request("GET", prefix)[0], 200)
        quest_status, _, quest_state = self.api_request(
            "POST", f"{prefix}/quest", {"ranked_concerns": ["O1"]}
        )
        self.assertEqual(quest_status, 200)
        self.assertEqual(quest_state["active_camp"]["id"], "camp_2047_retire")
        self.assertEqual(quest_state["camps"][0]["id"], "camp_2047_retire")
        preview_status, _, preview = self.api_request(
            "POST", f"{prefix}/preview", {"option_id": "cut_withdrawals"}
        )
        self.assertEqual(preview_status, 200)
        self.assertEqual(preview["option_id"], "cut_withdrawals")
        self.assertEqual(
            self.api_request("POST", f"{prefix}/decide", {"option_id": "cut_withdrawals"})[0],
            200,
        )
        self.assertEqual(self.api_request("GET", f"{prefix}/overview?mode=plain")[0], 200)
        self.assertEqual(self.api_request("GET", f"{prefix}/advisor-brief")[0], 200)
        self.assertEqual(self.api_request("POST", f"{prefix}/restart", {})[0], 200)

        # /api/sessions remains the canonical delegated API and supports cordada.
        status, _, session = self.api_request(
            "POST", "/api/sessions", {"case_id": "timothy-melanie-weah"}
        )
        self.assertEqual(status, 201)
        session_prefix = f"/api/sessions/{session['session_id']}"
        self.assertEqual(self.api_request("GET", session_prefix)[0], 200)
        self.assertEqual(self.api_request("POST", f"{session_prefix}/quest", {"ranked_concerns": ["O1"]})[0], 200)
        cordada_status, _, cordada = self.api_request(
            "POST",
            f"{session_prefix}/cordada",
            {"partner": "Timothy", "choices": ["pay_card_18k"]},
        )
        self.assertEqual(cordada_status, 200)
        self.assertTrue(cordada["blind_pending"])

        # The aliases expose the same cordada transition and mountain state.
        status, _, dual = self.api_request(
            "POST", "/api/expedition", {"case_id": "timothy-melanie-weah"}
        )
        self.assertEqual(status, 201)
        dual_prefix = f"/api/expedition/{dual['session_id']}"
        self.assertEqual(
            self.api_request("POST", f"{dual_prefix}/quest", {"ranked_concerns": ["O1"]})[0],
            200,
        )
        self.assertEqual(
            self.api_request(
                "POST",
                f"{dual_prefix}/cordada",
                {"partner": "Timothy", "choices": ["pay_card_18k"]},
            )[0],
            200,
        )
        self.assertEqual(
            self.api_request(
                "POST",
                f"{dual_prefix}/cordada",
                {"partner": "Melanie", "choices": ["pay_card_18k"]},
            )[0],
            200,
        )
        self.assertEqual(self.api_request("GET", f"/api/sessions/{dual['session_id']}/mountain")[0], 200)
        blocked_status, _, blocked = self.api_request(
            "POST", f"{dual_prefix}/decide", {"option_id": "keep_inertia"}
        )
        self.assertEqual(blocked_status, 200)
        self.assertTrue(blocked["blocked"])
        self.assertEqual(self.api_request("POST", f"{dual_prefix}/rewind", {})[0], 200)

    def test_expedition_and_session_reorder_camps_by_top1_fear(self) -> None:
        # Session creation with fear_ranking reorders immediately.
        status, _, created = self.api_request(
            "POST",
            "/api/expedition",
            {"case_id": "michael-carter", "fear_ranking": ["O1"]},
        )
        self.assertEqual(status, 201)
        self.assertEqual(created["active_camp"]["id"], "camp_2047_retire")
        self.assertEqual(
            [camp["id"] for camp in created["camps"]],
            ["camp_2047_retire", "camp_2026", "camp_2027_home"],
        )

        # Submitting a different Top-1 fear via /api/expedition/{id}/quest reorders cleanly from base.
        exp_prefix = f"/api/expedition/{created['session_id']}"
        status, _, home_state = self.api_request(
            "POST", f"{exp_prefix}/quest", {"ranked_concerns": ["O2"]}
        )
        self.assertEqual(status, 200)
        self.assertEqual(home_state["active_camp"]["id"], "camp_2027_home")
        self.assertEqual(
            [camp["id"] for camp in home_state["camps"]],
            ["camp_2027_home", "camp_2026", "camp_2047_retire"],
        )

        status, _, shield_state = self.api_request(
            "POST", f"{exp_prefix}/quest", {"ranked_concerns": ["O4"]}
        )
        self.assertEqual(status, 200)
        self.assertEqual(shield_state["active_camp"]["id"], "camp_2026")
        self.assertEqual(
            shield_state["active_camp"]["options"][0]["id"], "umbrella"
        )

        # Canonical /api/sessions/{id}/quest also adapts camps for Samantha Lewis.
        status, _, sam = self.api_request(
            "POST", "/api/sessions", {"case_id": "samantha-lewis"}
        )
        self.assertEqual(status, 201)
        sam_prefix = f"/api/sessions/{sam['session_id']}"
        status, _, sam_home = self.api_request(
            "POST", f"{sam_prefix}/quest", {"ranked_concerns": ["O3"]}
        )
        self.assertEqual(status, 200)
        self.assertEqual(
            sam_home["active_camp"]["id"], "camp_2027_2030_transitions"
        )
        self.assertEqual(
            sam_home["camps"][0]["id"], "camp_2027_2030_transitions"
        )

    def test_irl_radio_and_calendar_routes(self) -> None:
        status, _, created = self.api_request(
            "POST", "/api/irl", {"case_id": "michael-carter"}
        )
        self.assertEqual(status, 201)
        run_id = created["run_id"]
        self.assertEqual(created["focus_mode_view"]["focus_step"]["step_id"], "step_0_pay_amex")

        status, _, run = self.api_request("GET", f"/api/irl/{run_id}")
        self.assertEqual(status, 200)
        self.assertEqual(set(run) >= {"focus_mode_view", "timeline_view", "mountain_overview"}, True)

        status, _, checked = self.api_request(
            "POST", f"/api/irl/{run_id}/check", {"step_id": "step_0_pay_amex"}
        )
        self.assertEqual(status, 200)
        self.assertTrue(checked["is_completed"])
        self.assertEqual(
            self.api_request(
                "POST", f"/api/irl/{run_id}/uncheck", {"step_id": "step_0_pay_amex"}
            )[2]["is_completed"],
            False,
        )
        status, _, timeline = self.api_request("POST", f"/api/irl/{run_id}/advance", {"day": 3})
        self.assertEqual(status, 200)
        self.assertEqual(timeline["current_day"], 3)
        self.assertEqual(self.api_request("POST", f"/api/irl/{run_id}/repeat", {})[0], 200)
        status, _, inertia = self.api_request("GET", f"/api/irl/{run_id}/inertia")
        self.assertEqual(status, 200)
        self.assertIn("active_levers", inertia)

        status, _, historical = self.api_request("GET", "/api/radio")
        self.assertEqual(status, 200)
        self.assertEqual(len(historical["historical_shocks"]), 11)
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
        self.assertEqual(shock["matched_event"]["date_label"], "2025-04-02")

        status, headers, calendar = self.api_request("GET", f"/api/radio/{run_id}/ics")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Type"], "text/calendar; charset=utf-8")
        self.assertIn("BEGIN:VCALENDAR", calendar)

    def test_options_bad_requests_and_not_found(self) -> None:
        status, headers, body = self.api_request("OPTIONS", "/api/irl")
        self.assertEqual(status, 204)
        self.assertEqual(body, b"")
        self.assertEqual(headers["Access-Control-Allow-Origin"], "*")

        status, _, body = self.api_request("GET", "/api/cases/michael-carter?mode=invalid")
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "bad_request")
        status, _, body = self.api_request("POST", "/api/irl", {})
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "bad_request")
        invalid = request.Request(
            f"{self.base_url}/api/irl",
            data=b"not-json",
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaises(error.HTTPError) as raised:
            request.urlopen(invalid)
        self.assertEqual(raised.exception.code, 400)
        self.assertEqual(json.load(raised.exception)["error"], "bad_request")
        status, _, body = self.api_request("GET", "/api/irl/missing")
        self.assertEqual(status, 404)
        self.assertEqual(body["error"], "not_found")
        status, _, body = self.api_request("GET", "/api/does-not-exist")
        self.assertEqual(status, 404)
        self.assertEqual(body["error"], "not_found")


class N8NWebhookUnitTests(unittest.TestCase):
    """Exercise optional n8n effects without opening a webhook socket."""

    def setUp(self) -> None:
        self.state = ServerState(
            llm_client=LLMProxyClient(team_key="", transport="urllib")
        )

    @staticmethod
    def milestone_notification(case_id: str) -> dict[str, object]:
        return {
            "notification_id": "notif-test",
            "kind": "milestone",
            "type": "milestone_insistence",
            "day": 3,
            "severity": "warning",
            "case_id": case_id,
            "target_owner": "Michael",
            "title": "Hito de prueba",
            "message_plain": "Completa el paso.",
            "message_math": "Completa el paso con matematicas.",
            "deep_link": "irl://node/test#step=test",
            "internal_only": "must not be sent",
        }

    def capture_webhook(self):
        sent: list[tuple[request.Request, float]] = []
        delivered = threading.Event()

        def fake_urlopen(webhook_request, timeout):
            sent.append((webhook_request, timeout))
            delivered.set()
            response = MagicMock()
            response.__enter__.return_value = response
            return response

        return sent, delivered, fake_urlopen

    def assert_request(
        self,
        sent: list[tuple[request.Request, float]],
        expected_payload: dict[str, object],
    ) -> None:
        self.assertEqual(len(sent), 1)
        webhook_request, timeout = sent[0]
        self.assertEqual(webhook_request.full_url, "https://n8n.example.test/hook")
        self.assertEqual(webhook_request.get_method(), "POST")
        self.assertEqual(webhook_request.get_header("Content-type"), "application/json")
        self.assertEqual(timeout, 2)
        self.assertEqual(
            json.loads(webhook_request.data.decode("utf-8")), expected_payload
        )

    def test_advance_emits_exact_milestone_payload(self) -> None:
        run_id, engine = self.state.runs.create("michael-carter")
        notification = self.milestone_notification(engine.case_id)
        expected = {
            key: notification[key]
            for key in (
                "notification_id", "kind", "type", "day", "severity", "case_id",
                "target_owner", "title", "message_plain", "message_math", "deep_link",
            )
        }
        expected["run_id"] = run_id
        sent, delivered, fake_urlopen = self.capture_webhook()

        with patch.dict(
            os.environ, {"N8N_WEBHOOK_URL": "https://n8n.example.test/hook"}, clear=False
        ), patch(
            "backend.server.NotificationEngine.generate_milestone_notifications",
            return_value=[notification],
        ), patch("backend.server.urllib.request.urlopen", side_effect=fake_urlopen):
            status, _ = _handle_irl(
                "POST", urlsplit(f"/api/irl/{run_id}/advance"), {"day": 3}, self.state
            )
            self.assertEqual(status, 200)
            self.assertTrue(delivered.wait(1))

        self.assert_request(sent, expected)

    def test_check_emits_exact_milestone_payload(self) -> None:
        run_id, engine = self.state.runs.create("michael-carter")
        notification = self.milestone_notification(engine.case_id)
        expected = {
            key: notification[key]
            for key in (
                "notification_id", "kind", "type", "day", "severity", "case_id",
                "target_owner", "title", "message_plain", "message_math", "deep_link",
            )
        }
        expected["run_id"] = run_id
        sent, delivered, fake_urlopen = self.capture_webhook()

        with patch.dict(
            os.environ, {"N8N_WEBHOOK_URL": "https://n8n.example.test/hook"}, clear=False
        ), patch(
            "backend.server.NotificationEngine.generate_milestone_notifications",
            return_value=[notification],
        ), patch("backend.server.urllib.request.urlopen", side_effect=fake_urlopen):
            status, _ = _handle_irl(
                "POST",
                urlsplit(f"/api/irl/{run_id}/check"),
                {"step_id": "step_0_pay_amex"},
                self.state,
            )
            self.assertEqual(status, 200)
            self.assertTrue(delivered.wait(1))

        self.assert_request(sent, expected)

    def test_shock_emits_exact_notification_with_run_id(self) -> None:
        run_id, engine = self.state.runs.create("michael-carter")
        notification = {
            "notification_id": "notif-macro-test",
            "kind": "macro_shock",
            "type": "macro_shock_radio",
            "case_id": engine.case_id,
            "headline": "Shock de prueba",
            "matched_event": {"name": "Evento de prueba"},
            "anti_panic_message_plain": "No vender.",
        }
        expected = {**notification, "run_id": run_id}
        sent, delivered, fake_urlopen = self.capture_webhook()

        with patch.dict(
            os.environ, {"N8N_WEBHOOK_URL": "https://n8n.example.test/hook"}, clear=False
        ), patch(
            "backend.server.NotificationEngine.generate_macro_shock_notification",
            return_value=notification,
        ), patch("backend.server.urllib.request.urlopen", side_effect=fake_urlopen):
            status, response, _ = _handle_radio(
                "POST",
                urlsplit(f"/api/radio/{run_id}/shock"),
                {"event_name": "April 2025 tariffs shock"},
                self.state,
            )
            self.assertEqual(status, 200)
            self.assertEqual(response["run_id"], run_id)
            self.assertTrue(delivered.wait(1))

        self.assert_request(sent, expected)

    def test_webhook_failures_never_break_advance_response(self) -> None:
        failures = (
            error.URLError("n8n unavailable"),
            error.HTTPError("https://n8n.example.test/hook", 500, "error", {}, None),
        )
        for webhook_error in failures:
            with self.subTest(webhook_error=type(webhook_error).__name__):
                run_id, _ = self.state.runs.create("michael-carter")
                attempted = threading.Event()

                def failing_urlopen(*args, **kwargs):
                    attempted.set()
                    raise webhook_error

                with patch.dict(
                    os.environ, {"N8N_WEBHOOK_URL": "https://n8n.example.test/hook"}, clear=False
                ), patch("backend.server.urllib.request.urlopen", side_effect=failing_urlopen):
                    status, response = _handle_irl(
                        "POST", urlsplit(f"/api/irl/{run_id}/advance"), {"day": 3}, self.state
                    )
                    self.assertEqual(status, 200)
                    self.assertEqual(response["run_id"], run_id)
                    self.assertTrue(attempted.wait(1))

    def test_missing_webhook_url_is_a_silent_noop(self) -> None:
        run_id, _ = self.state.runs.create("michael-carter")
        with patch.dict(os.environ, {}, clear=True), patch(
            "backend.server.urllib.request.urlopen"
        ) as urlopen:
            status, response = _handle_irl(
                "POST", urlsplit(f"/api/irl/{run_id}/advance"), {"day": 3}, self.state
            )

        self.assertEqual(status, 200)
        self.assertEqual(response["run_id"], run_id)
        urlopen.assert_not_called()

    def test_webhook_url_loads_from_dotenv_only_when_not_in_environment(self) -> None:
        def load_dotenv() -> None:
            os.environ["N8N_WEBHOOK_URL"] = "https://n8n.example.test/from-dotenv"

        with patch.dict(os.environ, {}, clear=True), patch(
            "backend.server.load_env_file", side_effect=load_dotenv
        ) as load_env_file:
            self.assertEqual(
                _n8n_webhook_url(), "https://n8n.example.test/from-dotenv"
            )
            load_env_file.assert_called_once_with()


class NarrativeRouteUnitTests(unittest.TestCase):
    """Exercise narrative POST dispatch without binding a sandbox-blocked socket."""

    def setUp(self) -> None:
        self.state = ServerState(
            llm_client=LLMProxyClient(team_key="", transport="urllib")
        )

    def post(self, path: str, payload: dict[str, object]) -> tuple[int, object]:
        """Match the HTTP adapter's 400/404 exception-to-response contract."""
        try:
            return _handle_ai("POST", urlsplit(path), payload, self.state)
        except (BadRequestError, ValueError, TypeError) as exc:
            return 400, {"error": "bad_request", "message": str(exc)}
        except (KeyError, FileNotFoundError, CaseNotFoundError) as exc:
            return 404, {"error": "not_found", "message": str(exc)}

    def test_post_narrative_routes_fall_back_without_team_key_and_use_only_case_numbers(self) -> None:
        requests = (
            (
                "/api/ai/reframe",
                {
                    "case_id": "michael-carter",
                    "topic": "home_purchase",
                    "lens": "both",
                },
            ),
            (
                "/api/ai/pact",
                {
                    "case_id": "timothy-melanie-weah",
                    "member_a_votes": {
                        "top_fears": ["O1", "O3"],
                        "risk_choice": "Growth",
                    },
                    "member_b_votes": {
                        "top_fears": ["O1", "O2"],
                        "risk_choice": "Moderate",
                    },
                },
            ),
            (
                "/api/ai/brief",
                {
                    "case_id": "daniel-emily-johnson",
                    "fear_ranking": ["O2", "O1"],
                    "couple_votes": {
                        "member_a": {"risk_choice": "Growth"},
                        "member_b": {"risk_choice": "Moderate"},
                    },
                },
            ),
        )

        for path, payload in requests:
            with self.subTest(path=path):
                status, narrative = self.post(path, payload)
                self.assertEqual(status, 200)
                self.assertIsInstance(narrative, dict)
                self.assertFalse(narrative["used_llm"])
                self.assertTrue(narrative["llm_fallback_used"])
                self.assertEqual(narrative["fallback_reason"], "missing_team_key")
                self.assertTrue(narrative["verified_numbers_only"])

                case = load_case(narrative["case_id"])
                allowed = extract_case_allowed_numbers(case)
                verified, unverified = verify_text_numbers_against_case(
                    json.dumps(narrative, ensure_ascii=False), allowed
                )
                self.assertTrue(
                    verified,
                    f"El endpoint incorporó números no verificados: {unverified}",
                )

    def test_post_narrative_routes_return_400_or_404_for_invalid_payloads_and_cases(self) -> None:
        for path in ("/api/ai/reframe", "/api/ai/pact", "/api/ai/brief"):
            with self.subTest(path=path, payload="missing case_id"):
                status, body = self.post(path, {})
                self.assertEqual(status, 400)
                self.assertEqual(body["error"], "bad_request")

            with self.subTest(path=path, payload="unknown case_id"):
                status, body = self.post(path, {"case_id": "case-does-not-exist"})
                self.assertEqual(status, 404)
                self.assertEqual(body["error"], "not_found")

        invalid_payloads = (
            ("/api/ai/reframe", {"case_id": "michael-carter", "lens": 7}),
            ("/api/ai/reframe", {"case_id": "michael-carter", "lang": "FR"}),
            ("/api/ai/pact", {"case_id": "timothy-melanie-weah", "member_a_votes": []}),
            ("/api/ai/brief", {"case_id": "michael-carter", "fear_ranking": "O1"}),
        )
        for path, payload in invalid_payloads:
            with self.subTest(path=path, payload=payload):
                status, body = self.post(path, payload)
                self.assertEqual(status, 400)
                self.assertEqual(body["error"], "bad_request")

    def test_post_narrative_routes_support_lang_en_blind_spot_and_anxiety_gap(self) -> None:
        status, reframe = self.post(
            "/api/ai/reframe",
            {
                "case_id": "michael-carter",
                "topic": "overview",
                "lens": "both",
                "lang": "en",
                "context": {
                    "top_rank": "O3",
                    "thermometer": 80,
                    "subjective": "market drop",
                    "concerns": ["O3", "O1"],
                },
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(reframe["lang"], "EN")
        self.assertFalse(reframe["used_llm"])
        self.assertTrue(reframe["llm_fallback_used"])
        self.assertIn("blind_spot_contrast", reframe)
        self.assertEqual(reframe["blind_spot_contrast"]["thermometer_band"], "high")
        self.assertIn("What worries you most", reframe["blind_spot_contrast"]["contrast_summary"])

        status, pact = self.post(
            "/api/ai/pact",
            {
                "case_id": "timothy-melanie-weah",
                "lang": "EN",
                "member_a_votes": {"top_fears": ["O1"], "risk_choice": "Growth", "thermometer": 75},
                "member_b_votes": {"top_fears": ["O1"], "risk_choice": "Moderate", "thermometer": 30},
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(pact["lang"], "EN")
        self.assertEqual(pact["anxiety_gap"]["gap"], 45)
        self.assertEqual(pact["anxiety_gap"]["band"], "high")

        status, brief = self.post(
            "/api/ai/brief",
            {
                "case_id": "samantha-lewis",
                "lang": "EN",
                "fear_ranking": ["O1", "O2"],
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(brief["lang"], "EN")
        self.assertIn("## 1. Fear Ranking", brief["markdown_brief"])


class RoomRouteUnitTests(unittest.TestCase):
    """Exercise two-device room synchronization without binding a TCP socket."""

    case_id = "timothy-melanie-weah"

    def setUp(self) -> None:
        self.state = ServerState(
            llm_client=LLMProxyClient(team_key="", transport="urllib")
        )

        def only_test_case(case_id: str) -> dict[str, str]:
            if case_id != self.case_id:
                raise CaseNotFoundError(f"Caso no encontrado: {case_id}")
            return {"id": case_id}

        # Isolate the unit tests from MCP/local I/O while retaining the same
        # generic case-provider seam used by ServerState in production.
        self.state.case_provider = only_test_case

    def room_request(
        self,
        method: str,
        path: str,
        payload: dict[str, object] | None = None,
    ) -> tuple[int, object]:
        """Match the HTTP adapter's 400/404 exception-to-response contract."""
        try:
            return _handle_rooms(
                method, urlsplit(path), payload or {}, self.state
            )
        except (BadRequestError, ValueError, TypeError) as exc:
            return 400, {"error": "bad_request", "message": str(exc)}
        except (KeyError, FileNotFoundError, CaseNotFoundError) as exc:
            return 404, {"error": "not_found", "message": str(exc)}

    def test_room_syncs_evaluations_and_all_four_decision_stages(self) -> None:
        status, room = self.room_request("POST", "/api/rooms", {"case_id": self.case_id})
        self.assertEqual(status, 201)
        self.assertIsInstance(room, dict)
        room_id = room["room_id"]
        self.assertEqual(
            room,
            {
                "room_id": room_id,
                "case_id": self.case_id,
                "share_query": f"?case={self.case_id}&room={room_id}&member=B",
                "evaluation": {"A": None, "B": None},
                "evaluation_ready": False,
                "decisions": {},
            },
        )

        evaluation_a = {
            "member": "A",
            "top_fears": ["O1", "O3"],
            "thermometer": 7,
            "priority": "liquidity",
            "subjective": "No quedarnos sin colchón.",
        }
        status, after_a = self.room_request(
            "POST", f"/api/rooms/{room_id}/evaluation", evaluation_a
        )
        self.assertEqual(status, 200)
        self.assertEqual(after_a["evaluation"]["A"], {key: value for key, value in evaluation_a.items() if key != "member"})
        self.assertIsNone(after_a["evaluation"]["B"])
        self.assertFalse(after_a["evaluation_ready"])

        evaluation_b = {
            "member": "B",
            "top_fears": ["O2", "O1"],
            "thermometer": 4,
            "priority": "debt",
            "subjective": "El interés de la tarjeta.",
        }
        status, after_b = self.room_request(
            "POST", f"/api/rooms/{room_id}/evaluation", evaluation_b
        )
        self.assertEqual(status, 200)
        self.assertEqual(after_b["evaluation"]["B"], {key: value for key, value in evaluation_b.items() if key != "member"})
        self.assertTrue(after_b["evaluation_ready"])

        stage_votes = (
            (0, "good", "good", True),
            (1, "bad", "bad", True),
            (2, "good", "good", True),
            (3, "good", "bad", False),
        )
        for stage, route_a, route_b, aligned in stage_votes:
            with self.subTest(stage=stage):
                status, after_vote_a = self.room_request(
                    "POST",
                    f"/api/rooms/{room_id}/decision",
                    {"member": "A", "stage": stage, "route": route_a, "label": "A"},
                )
                self.assertEqual(status, 200)
                self.assertFalse(after_vote_a["decisions"][str(stage)]["ready"])

                status, after_vote_b = self.room_request(
                    "POST",
                    f"/api/rooms/{room_id}/decision",
                    {"member": "B", "stage": str(stage), "route": route_b, "label": "B"},
                )
                self.assertEqual(status, 200)
                decision = after_vote_b["decisions"][str(stage)]
                self.assertTrue(decision["ready"])
                self.assertEqual(decision["aligned"], aligned)
                self.assertEqual(decision["A"]["route"], route_a)
                self.assertEqual(decision["B"]["route"], route_b)

        status, current = self.room_request("GET", f"/api/rooms/{room_id}")
        self.assertEqual(status, 200)
        self.assertEqual(current, after_vote_b)

    def test_room_validation_returns_400_or_404(self) -> None:
        for payload, expected_status in (
            ({}, 400),
            ({"case_id": "missing-case"}, 404),
        ):
            with self.subTest(create=payload):
                status, body = self.room_request("POST", "/api/rooms", payload)
                self.assertEqual(status, expected_status)
                self.assertEqual(
                    body["error"],
                    "bad_request" if expected_status == 400 else "not_found",
                )

        status, body = self.room_request("GET", "/api/rooms/missing-room")
        self.assertEqual(status, 404)
        self.assertEqual(body["error"], "not_found")

        _, room = self.room_request("POST", "/api/rooms", {"case_id": self.case_id})
        room_id = room["room_id"]
        invalid_requests = (
            (f"/api/rooms/{room_id}/evaluation", {"member": "C"}),
            (f"/api/rooms/{room_id}/decision", {"member": "C", "stage": 0, "route": "good"}),
            (f"/api/rooms/{room_id}/decision", {"member": "A", "stage": 0, "route": "sideways"}),
            (f"/api/rooms/{room_id}/decision", {"member": "A", "stage": 4, "route": "good"}),
        )
        for path, payload in invalid_requests:
            with self.subTest(path=path, payload=payload):
                status, body = self.room_request("POST", path, payload)
                self.assertEqual(status, 400)
                self.assertEqual(body["error"], "bad_request")


class TelegramDeepLinkUnitTests(unittest.TestCase):
    """Verify /api/radio exposes telegram_bot_username and telegram_deep_link."""

    def test_radio_exposes_default_and_custom_telegram_deep_link(self) -> None:
        state = ServerState()
        with patch.dict(os.environ, {"TELEGRAM_BOT_USERNAME": ""}, clear=False):
            status, payload, _ = _handle_radio("GET", urlsplit("/api/radio"), {}, state)
            self.assertEqual(status, 200)
            self.assertEqual(payload["telegram_bot_username"], "SherpasRadioBot")
            self.assertEqual(
                payload["telegram_deep_link"],
                "https://t.me/SherpasRadioBot?start=demo_client",
            )
            status, case_payload, _ = _handle_radio(
                "GET",
                urlsplit("/api/radio/michael-carter?owner=Michael"),
                {},
                state,
            )
            self.assertEqual(status, 200)
            self.assertEqual(
                case_payload["telegram_deep_link"],
                "https://t.me/SherpasRadioBot?start=michael-carter_Michael",
            )

        with patch.dict(os.environ, {"TELEGRAM_BOT_USERNAME": "@CustomSherpaBot"}, clear=False):
            status, custom_payload, _ = _handle_radio(
                "GET",
                urlsplit("/api/radio/timothy-melanie-weah?owner=A"),
                {},
                state,
            )
            self.assertEqual(status, 200)
            self.assertEqual(custom_payload["telegram_bot_username"], "CustomSherpaBot")
            self.assertEqual(
                custom_payload["telegram_deep_link"],
                "https://t.me/CustomSherpaBot?start=timothy-melanie-weah_A",
            )


class RepositoryFrontendTests(unittest.TestCase):
    """Serve the checked-in frontend rather than the isolated test fixture."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server(port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def get_text(self, path: str):
        with request.urlopen(f"{self.base_url}{path}") as response:
            return response.status, response.headers, response.read().decode("utf-8")

    def test_checked_in_frontend_html_and_post_cima_script_are_served(self) -> None:
        status, headers, html = self.get_text("/")
        self.assertEqual(status, 200)
        self.assertIn("text/html", headers["Content-Type"])
        self.assertIn('id="app"', html)

        status, headers, script = self.get_text("/post-cima.js")
        self.assertEqual(status, 200)
        self.assertIn("javascript", headers["Content-Type"])
        self.assertIn("SherpaPostCima", script)


class RepositoryContractTests(unittest.TestCase):
    def test_namespace_package_and_new_python_files_are_utf8_without_bom(self) -> None:
        self.assertFalse((ROOT / "backend" / "__init__.py").exists())
        for path in (ROOT / "backend" / "server.py", Path(__file__)):
            self.assertFalse(path.read_bytes().startswith(b"\xef\xbb\xbf"), str(path))
            path.read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
