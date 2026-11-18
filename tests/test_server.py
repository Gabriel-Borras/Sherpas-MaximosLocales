"""HTTP integration tests for the unified deterministic server."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib import error, request

from backend.server import create_server


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

        cls.server = create_server(port=0, frontend_dir=frontend)
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
        self.assertEqual(
            self.api_request("POST", f"{prefix}/quest", {"ranked_concerns": ["O1"]})[0],
            200,
        )
        preview_status, _, preview = self.api_request(
            "POST", f"{prefix}/preview", {"option_id": "umbrella"}
        )
        self.assertEqual(preview_status, 200)
        self.assertEqual(preview["option_id"], "umbrella")
        self.assertEqual(
            self.api_request("POST", f"{prefix}/decide", {"option_id": "umbrella"})[0],
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
