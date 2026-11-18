"""Tests for verified cases, expeditions, and API adapters."""

import copy
import io
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

from backend.api import (
    SessionStore,
    create_http_server,
    create_wsgi_app,
    dispatch_request,
)
from backend.timeline_engine import (
    ActionBlockedError,
    Expedition,
    PhaseOrderError,
    SEED_CASES,
    TimelineEngine,
)


class TimelineEngineTests(unittest.TestCase):
    """Verify the supplied case facts and core expedition behavior."""

    def setUp(self):
        """Create an engine for each test."""
        self.engine = TimelineEngine()

    def test_verified_cases_and_unpublished_pillar_scores(self):
        """Keep verified figures and missing scores distinct."""
        self.assertEqual(set(SEED_CASES), {
            "michael-carter", "samantha-lewis", "timothy-melanie-weah",
            "daniel-emily-johnson",
        })
        michael = self.engine.load_case("michael-carter")
        self.assertEqual(michael["score"]["value"], 26)
        michael_scores = [
            pillar["score"] for pillar in michael["score"]["pillars"]
        ]
        self.assertEqual(michael_scores, [0, 8, 11, 4, 4])
        self.assertIn("23.9%", michael["reframing"]["plain"])
        samantha = self.engine.load_case("samantha-lewis")
        self.assertTrue(all(pillar["score"] is None
                            for pillar in samantha["score"]["pillars"]))
        weah = self.engine.load_case("timothy-melanie-weah")
        self.assertTrue(all(pillar["score"] is None
                            for pillar in weah["score"]["pillars"]))
        johnson = self.engine.load_case("daniel-emily-johnson")
        johnson_scores = [
            pillar["score"] for pillar in johnson["score"]["pillars"]
        ]
        self.assertEqual(johnson_scores, [None, None, None, None, 0])

    def test_yearly_keeps_liquid_assets_separate_from_net_worth(self):
        """Retain sparse annual data without interpolating values."""
        michael = self.engine.load_case("michael-carter")
        point = next(
            item for item in michael["yearly"] if item["year"] == 2075
        )
        self.assertEqual(point["investable_assets"], -38276)
        self.assertEqual(point["net_worth"], 2570000)
        self.assertEqual(len(michael["yearly"]), 12)
        self.assertEqual(
            next(item for item in michael["yearly"] if item["year"] == 2032),
            {"year": 2032, "age": 43, "investable_assets": 279056},
        )

    def test_plain_and_math_case_overview(self):
        """Switch between a readable view and exact case values."""
        plain = self.engine.overview("michael-carter", "plain")
        math_view = self.engine.overview("michael-carter", "math")
        self.assertEqual(plain["display_text"], plain["views"]["plain"])
        self.assertEqual(math_view["display_text"], math_view["views"]["math"])
        self.assertIn("178717", math_view["display_text"])

    def test_case_source_priority_and_json_normalization(self):
        """Load custom and directory JSON with source provenance intact."""
        raw = {
            "financial_health": {
                "score": {"value": 82, "status": "strong", "pillars": [
                    {"name": "Debt", "score": 7, "max": 10},
                ]},
                "projections": {"yearly": [{"year": 2053,
                                             "investable_assets": -227414}]},
            },
            "investment_analysis": {"analysis": {"events": [{"id": "storm"}]}},
            "persona": "# Tensions\nT1\n## Concerns\nO1",
        }
        case = TimelineEngine(custom_cases={"samantha-lewis": raw}).load_case(
            "samantha-lewis")
        self.assertEqual(case["data_source"], "custom_cases")
        self.assertEqual(case["score"]["value"], 82)
        self.assertEqual(len(case["score"]["pillars"]), 1)
        self.assertEqual(case["score"]["pillars"][0]["score"], 7)
        self.assertEqual(case["yearly"][0]["investable_assets"], -227414)
        self.assertEqual(case["events"][0]["id"], "storm")
        self.assertIn("O1", case["subjective_concerns"])
        with tempfile.TemporaryDirectory() as directory:
            case_dir = Path(directory) / "samantha-lewis"
            case_dir.mkdir()
            (case_dir / "financial-health.json").write_text(
                json.dumps(raw["financial_health"]), encoding="utf-8")
            loaded = TimelineEngine(cases_dir=directory).load_case(
                "samantha-lewis"
            )
            self.assertEqual(loaded["data_source"], "cases_dir")
            self.assertEqual(loaded["score"]["value"], 82)
            self.assertEqual(len(loaded["score"]["pillars"]), 5)

    def test_namespace_package_and_utf8_bom_handling(self):
        """Remove the package marker and read BOM files from env paths."""
        project_root = Path(__file__).resolve().parents[1]
        self.assertFalse((project_root / "backend" / "__init__.py").exists())
        for filename in (
            "backend/timeline_engine.py", "backend/api.py",
            "tests/test_timeline_engine.py",
        ):
            source = project_root / filename
            self.assertFalse(source.read_bytes().startswith(b"\xef\xbb\xbf"))
        financial = {
            "score": {"overall": 71, "status": "strong", "pillars": [
                {"name": "Debt", "score": 7, "max": 10},
            ]},
            "projections": {"yearly": [{"year": 2026,
                                         "investable_assets": 1000}]},
        }
        for environment_key in ("SHERPAS_CASES_DIR", "CASES_DIR"):
            with tempfile.TemporaryDirectory() as directory:
                case_dir = Path(directory) / "samantha-lewis"
                case_dir.mkdir()
                json_path = case_dir / "financial-health.json"
                json_path.write_bytes(
                    b"\xef\xbb\xbf" + json.dumps(financial).encode("utf-8")
                )
                persona_path = case_dir / "persona.md"
                persona_path.write_bytes(
                    b"\xef\xbb\xbf" +
                    "# Concerns\nO1: retirement\n".encode("utf-8")
                )
                with patch.dict(os.environ, {environment_key: directory},
                                clear=False):
                    engine = TimelineEngine()
                    loaded = engine.load_case("samantha-lewis")
                self.assertEqual(loaded["data_source"], "cases_dir")
                self.assertEqual(loaded["score"]["value"], 71)
                debt = next(
                    pillar for pillar in loaded["score"]["pillars"]
                    if pillar["name"] == "Debt"
                )
                self.assertEqual(debt["max_score"], 10)
                self.assertEqual(debt["score"], 7)
                self.assertIn("O1: retirement", loaded["subjective_concerns"])

    def test_real_score_shape_and_cases_directory_expedition(self):
        """Normalize MCP score fields and retain seed expedition structure."""
        raw = {
            "financial_health": {
                "score": {"overall": 73, "status": "strong", "pillars": [
                    {"name": "Debt", "score": 8, "max": 10},
                ]},
                "projections": {"yearly": [{"year": 2026,
                                             "investable_assets": 1234}]},
                "key_metrics": {"verified": True},
            },
            "investment_analysis": {"analysis": {"events": [{"year": 2025}]}},
            "persona": "# Tensions\nT1\n# Subjective concerns\nNone recorded",
        }
        import_path = "backend.timeline_engine.importlib.import_module"
        with patch(import_path) as loader:
            loader.return_value.get_case.return_value = raw
            loaded = TimelineEngine().load_case("michael-carter")
        self.assertEqual(loaded["score"]["value"], 73)
        pillars = loaded["score"]["pillars"]
        canonical = SEED_CASES["michael-carter"]["score"]["pillars"]
        self.assertEqual(len(pillars), 5)
        self.assertEqual(
            [(pillar["name"], pillar["score"], pillar["max_score"])
             for pillar in pillars],
            [(pillar["name"], pillar["score"], pillar["max_score"])
             for pillar in canonical],
        )
        debt = next(pillar for pillar in pillars
                     if pillar["name"] == "Debt")
        self.assertEqual(debt["max_score"], 10)
        self.assertEqual(debt["score"], 8)
        self.assertIn("camps", loaded)
        self.assertIn("block", loaded)
        expedition = Expedition(loaded)
        expedition.submit_quest([])
        self.assertEqual(expedition.state()["active_camp"]["id"], "camp_2026")
        self.assertTrue(loaded["key_metrics"]["verified"])
        self.assertEqual(loaded["yearly"][0]["investable_assets"], 1234)
        self.assertEqual(loaded["events"][0]["year"], 2025)
        self.assertEqual(loaded["data_source"], "backend.mcp_client")

    def test_case_provider_mcp_seed_format_normalizes_all_cases(self):
        """Normalize the MCP _SEED financial, investment, and persona shape."""
        _SEED = {}
        for case_id, seed in SEED_CASES.items():
            pillars = []
            if case_id == "michael-carter":
                pillars = [{"name": "Debt", "score": 8, "max": 10}]
            _SEED[case_id] = {
                "financial-health": {
                    "score": {
                        "overall": seed["score"]["value"],
                        "status": seed["score"]["status"],
                        "pillars": pillars,
                    },
                    "projections": {
                        "yearly": copy.deepcopy(seed["yearly"]),
                    },
                },
                "investment-analysis": {"analysis": {"events": []}},
                "persona": "# Concerns\nNone recorded",
            }
        engine = TimelineEngine(
            case_provider=lambda case_id: copy.deepcopy(_SEED[case_id])
        )
        loaded_cases = {
            case_id: engine.load_case(case_id) for case_id in SEED_CASES
        }
        for case_id, loaded in loaded_cases.items():
            self.assertEqual(loaded["data_source"], "case_provider")
            self.assertEqual(len(loaded["score"]["pillars"]), 5)
            self.assertEqual(
                [(pillar["name"], pillar["score"], pillar["max_score"])
                 for pillar in loaded["score"]["pillars"]],
                [(pillar["name"], pillar["score"], pillar["max_score"])
                 for pillar in SEED_CASES[case_id]["score"]["pillars"]],
            )
        for case_id, expected in (
                ("timothy-melanie-weah", 78),
                ("daniel-emily-johnson", 60)):
            self.assertEqual(
                loaded_cases[case_id]["score"]["combined_target_score"],
                expected,
            )
            self.assertEqual(
                loaded_cases[case_id]["combined_target_score"], expected
            )
        self.assertEqual(len(loaded_cases["michael-carter"]["yearly"]), 12)

    def test_michael_complete_score_route(self):
        """Carry Michael's score from 26 through 31 to 62."""
        expedition = Expedition(self.engine.load_case("michael-carter"))
        expedition.submit_quest([])
        first = expedition.preview("umbrella", "camp_2026")
        score_change = (first["score_before"], first["score_after"])
        self.assertEqual(score_change, (26, 31))
        expedition.decide("umbrella", "camp_2026")
        expedition.decide("buy_as_planned", "camp_2027_home")
        last = expedition.preview("cut_withdrawals", "camp_2047_retire")
        self.assertEqual((last["score_before"], last["score_after"]), (31, 62))
        result = expedition.decide("cut_withdrawals", "camp_2047_retire")
        self.assertEqual((result["score_before"], result["score_after"]),
                         (31, 62))
        self.assertEqual(expedition.current_score, 62)

    def test_cordada_common_anchor_frictions_and_cashflow(self):
        """Show ordered D6, case frictions, and verified midpoint figures."""
        for case_id, choices, friction_prefix in (
            ("timothy-melanie-weah", ("pay_card_18k", "rebalance_upro_401k"),
             ("D4:", "T1:")),
            ("daniel-emily-johnson", ("life_insurance", "umbrella"),
             ("D4:", "T5:")),
        ):
            expedition = Expedition(self.engine.load_case(case_id))
            expedition.submit_quest([])
            expedition.submit_vote(
                "A", ranked_concerns=["O1"], camp_choices=[choices[0]],
                subjective_concern="Primera preocupación",
            )
            result = expedition.submit_vote(
                "B", ranked_concerns=["O1"], choices=[choices[1]],
                subjective_concern="Segunda preocupación",
            )
            self.assertEqual(result["shared_100_common"][0],
                             expedition.case["d6_anchor"])
            self.assertEqual(result["shared_100_common"][1], "O1")
            self.assertTrue(result["mountain_preload"]["aligned_on_trunk"])
            diverged = result["mountain_preload"]["diverged_partners"]
            self.assertEqual(diverged, [])
            self.assertEqual(tuple(item[:3] for item in result["frictions"]),
                             friction_prefix)
            self.assertEqual(
                result["cashflow_midpoint"]["free_cashflow_yearly"], 15032
            )
            self.assertEqual(len(result["frictions"]), 2)
            self.assertEqual(
                expedition.advisor_brief()["subjective_concerns"],
                {"Timothy" if "weah" in case_id else "Daniel":
                 "Primera preocupación",
                 "Melanie" if "weah" in case_id else "Emily":
                 "Segunda preocupación"},
            )

    def test_cordada_failed_partner_choice_keeps_its_color(self):
        """Split only the partner who voted for an invalid route."""
        expedition = Expedition(self.engine.load_case("timothy-melanie-weah"))
        expedition.submit_quest([])
        expedition.submit_vote("A", camp_choices=["pay_card_18k"])
        result = expedition.submit_vote("B", choices=["keep_inertia"])
        self.assertFalse(result["mountain_preload"]["aligned_on_trunk"])
        self.assertEqual(result["mountain_preload"]["diverged_partners"], [
            {"partner": "B", "color": "#0D9488"},
        ])
        failed = expedition.decide(
            None, partner_choices={"A": "pay_card_18k",
                                   "Melanie": "keep_inertia"}
        )
        self.assertEqual(failed["failed_branch"]["color"], "#0D9488")

    def test_phase_order_and_blind_cordada_votes(self):
        """Protect partner votes until both have responded."""
        case = self.engine.load_case("timothy-melanie-weah")
        expedition = Expedition(case)
        with self.assertRaises(PhaseOrderError):
            expedition.preview("pay_card_18k")
        expedition.submit_quest(["O1"], "Cash flow concern")
        pending = expedition.submit_vote(
            "Timothy", ranked_concerns=["O1"], choices=["pay_card_18k"])
        self.assertTrue(pending["blind_pending"])
        self.assertFalse(pending["partner_visible"])
        self.assertEqual(expedition.state()["votes_submitted"], ["A"])
        self.assertIsNone(expedition.state()["votes"])
        self.assertTrue(expedition.state()["blind_votes_hidden"])
        result = expedition.submit_vote(
            "B", ranked_concerns=["O1"], choices=["pay_card_18k"])
        self.assertFalse(result["blind_pending"])
        self.assertEqual(result["shared_100_common"][1], "O1")
        self.assertEqual(len(result["frictions"]), 2)
        self.assertTrue(result["frictions"][0].startswith("D4:"))
        self.assertTrue(result["frictions"][1].startswith("T1:"))
        preload = result["mountain_preload"]
        self.assertEqual(preload["partner_a_color"], "#2563EB")
        self.assertEqual(preload["partner_b_color"], "#0D9488")

    def test_previews_reflect_only_published_score_changes(self):
        """Preview the score movement documented for each decision."""
        expected = {
            "michael-carter": ("umbrella", 26, 31),
            "samantha-lewis": ("home_insurance", 82, 84),
            "timothy-melanie-weah": ("shield_life_umbrella", 60, 78),
            "daniel-emily-johnson": ("life_insurance", 52, 57),
        }
        for case_id, (option_id, before, after) in expected.items():
            with self.subTest(case_id=case_id):
                expedition = Expedition(self.engine.load_case(case_id))
                expedition.submit_quest([])
                if expedition.case["dual"]:
                    expedition.submit_vote("A", choices=[option_id])
                    expedition.submit_vote("B", choices=[option_id])
                preview = expedition.preview(option_id)
                score_change = (preview["score_before"],
                                preview["score_after"])
                self.assertEqual(score_change, (before, after))
                if expedition.case["dual"]:
                    self.assertEqual(preview["combined_score_after"],
                                     expedition.case["combined_target_score"])

    def test_all_case_blocks_require_rewind_before_continuing(self):
        """Open each case's verified block and require a rewind."""
        for case_id, case in SEED_CASES.items():
            expedition = Expedition(case)
            expedition.submit_quest([])
            if case["dual"]:
                expedition.submit_vote("A", choices=[])
                expedition.submit_vote("B", choices=[])
            camp = expedition.case["camps"][0]
            failed = next(
                item for item in camp["options"] if item.get("fails")
            )
            result = expedition.decide(failed["id"])
            self.assertTrue(result["blocked"])
            self.assertEqual(result["block_type"], case["block"]["type"])
            self.assertEqual(result["failed_branch"]["block"], case["block"])
            with self.assertRaises(ActionBlockedError):
                expedition.preview(camp["options"][0]["id"])
            with self.assertRaises(ActionBlockedError):
                expedition.decide(camp["options"][0]["id"])
            expedition.rewind()
            self.assertFalse(expedition.blocked)
            self.assertEqual(len(expedition.overview()["failed_branches"]), 1)
            expedition.decide(camp["options"][0]["id"])
            for next_camp in expedition.case["camps"][1:]:
                expedition.decide(next_camp["options"][0]["id"])
            self.assertTrue(expedition.completed)
            self.assertEqual(expedition.phase, "summit")
            self.assertEqual(len(expedition.overview()["failed_branches"]), 1)
            expedition.restart()
            self.assertFalse(expedition.completed)
            self.assertEqual(expedition.phase, "quest")
            self.assertEqual(expedition.overview()["failed_branches"], [])

    def test_transition_events_never_create_score_deltas(self):
        """Record housing questions without inventing counterfactual scores."""
        cases = (("michael-carter", "camp_2027_home", "ask_advisor_delay"),
                 ("samantha-lewis", "camp_2027_2030_transitions",
                  "ask_advisor_plan"))
        for case_id, camp_id, option_id in cases:
            expedition = Expedition(self.engine.load_case(case_id))
            expedition.submit_quest([])
            first_option = expedition.case["camps"][0]["options"][0]
            expedition.decide(first_option["id"])
            expedition.decide(
                option_id, camp_id=camp_id, send_to_advisor_brief=True,
                advisor_question="¿Conviene retrasar?")
            self.assertIsNone(expedition.decisions[-1]["score_delta"])
            self.assertIn("¿Conviene retrasar?",
                          expedition.advisor_brief()["uncalculated_questions"])

    def test_transition_event_accepts_missing_option_id(self):
        """Allow an event without a selection and reject invalid option IDs."""
        expedition = Expedition(self.engine.load_case("samantha-lewis"))
        expedition.submit_quest([])
        expedition.decide("home_insurance", "camp_2026_shield")
        with self.assertRaises(ValueError):
            expedition.decide("missing", "camp_2027_2030_transitions")
        result = expedition.decide(
            None, "camp_2027_2030_transitions",
            send_to_advisor_brief=True,
            advisor_question="¿Qué debemos planificar?",
        )
        self.assertFalse(result["blocked"])
        self.assertIsNone(expedition.decisions[-1]["option_id"])
        self.assertIn(
            "¿Qué debemos planificar?",
            result["uncalculated_questions"],
        )


class ApiTests(unittest.TestCase):
    """Verify dispatcher and real HTTP and WSGI adapters."""

    def test_dispatch_query_options_and_wsgi(self):
        """Dispatch query modes and serve WSGI responses."""
        store = SessionStore()
        status, overview = dispatch_request(
            "GET", "/api/cases/michael-carter?mode=math", store=store)
        self.assertEqual(status, 200)
        self.assertEqual(overview["mode"], "math")
        options_status, _ = dispatch_request(
            "OPTIONS", "/api/cases", store=store
        )
        self.assertEqual(options_status, 204)
        status, session = dispatch_request(
            "POST", "/api/sessions", {"case_id": "michael-carter"},
            store=store,
        )
        self.assertEqual(status, 201)
        self.assertEqual(dispatch_request(
            "GET", f"/api/sessions/{session['session_id']}/mountain",
            store=store)[0], 409)
        app = create_wsgi_app(store)
        captured = {}

        def start_response(status_line, headers):
            """Capture WSGI response status."""
            captured["status"] = status_line
            captured["headers"] = headers

        response = app({"REQUEST_METHOD": "GET", "PATH_INFO": "/health",
                        "CONTENT_LENGTH": "0", "wsgi.input": io.BytesIO()},
                       start_response)
        self.assertTrue(response[0])
        self.assertTrue(captured["status"].startswith("200"))
        options_response = app({
            "REQUEST_METHOD": "OPTIONS", "PATH_INFO": "/api/cases",
            "CONTENT_LENGTH": "0", "wsgi.input": io.BytesIO(),
        }, start_response)
        self.assertTrue(captured["status"].startswith("204"))
        self.assertEqual(options_response, [b""])
        self.assertIn(("Content-Length", "0"), captured["headers"])

    def test_threaded_http_server(self):
        """Exercise the actual HTTP handler using urllib."""
        server = create_http_server(port=0, store=SessionStore())
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/health"
            with urllib.request.urlopen(url) as response:
                self.assertEqual(json.load(response)["status"], "ok")
            options_request = urllib.request.Request(
                url, method="OPTIONS"
            )
            with urllib.request.urlopen(options_request) as response:
                self.assertEqual(response.status, 204)
                self.assertEqual(response.read(), b"")
                self.assertEqual(response.headers["Content-Length"], "0")
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_invalid_modes_and_missing_session_fields_are_bad_requests(self):
        """Return HTTP 400 for unsupported modes and missing fields."""
        status, _ = dispatch_request(
            "GET", "/api/cases/michael-carter?mode=invalid",
            store=SessionStore(),
        )
        self.assertEqual(status, 400)
        status, _ = dispatch_request(
            "POST", "/api/sessions", {}, store=SessionStore()
        )
        self.assertEqual(status, 400)
        store = SessionStore()
        _, session = dispatch_request(
            "POST", "/api/sessions", {"case_id": "michael-carter"},
            store=store,
        )
        status, _ = dispatch_request(
            "POST",
            f"/api/sessions/{session['session_id']}/mountain/preview",
            {}, store=store,
        )
        self.assertEqual(status, 400)

    def test_http_expedition_from_quest_to_advisor_brief(self):
        """Run the full DUAL expedition through the real HTTP server."""
        server = create_http_server(port=0, store=SessionStore())
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base_url = f"http://127.0.0.1:{server.server_port}"

        def request(method, path, payload=None):
            """Send JSON to the local server and return status and data."""
            data = None if payload is None else json.dumps(payload).encode()
            req = urllib.request.Request(
                f"{base_url}{path}", data=data, method=method,
                headers={"Content-Type": "application/json"},
            )
            try:
                with urllib.request.urlopen(req) as response:
                    return response.status, json.load(response)
            except urllib.error.HTTPError as error:
                return error.code, json.load(error)

        try:
            status, session = request(
                "POST", "/api/sessions", {"case_id": "timothy-melanie-weah"}
            )
            self.assertEqual(status, 201)
            session_id = session["session_id"]
            prefix = f"/api/sessions/{session_id}"
            self.assertEqual(request(
                "POST", f"{prefix}/quest", {"ranked_concerns": ["O1"]}
            )[0], 200)
            self.assertTrue(request(
                "POST", f"{prefix}/cordada",
                {"partner": "Timothy", "choices": ["pay_card_18k"]},
            )[1]["blind_pending"])
            cordada_status, cordada = request(
                "POST", f"{prefix}/cordada",
                {"partner": "Melanie", "choices": ["pay_card_18k"]},
            )
            self.assertEqual(cordada_status, 200)
            self.assertTrue(cordada["partner_visible"])
            preview_status, preview = request(
                "POST", f"{prefix}/mountain/preview",
                {"option_id": "keep_inertia"},
            )
            self.assertEqual(preview_status, 200)
            self.assertTrue(preview["will_block"])
            blocked_status, blocked = request(
                "POST", f"{prefix}/mountain/decide",
                {"option_id": "keep_inertia"},
            )
            self.assertEqual(blocked_status, 200)
            self.assertTrue(blocked["blocked"])
            blocked_preview, _ = request(
                "POST", f"{prefix}/mountain/preview",
                {"option_id": "pay_card_18k"},
            )
            self.assertEqual(blocked_preview, 409)
            self.assertEqual(request(
                "POST", f"{prefix}/mountain/rewind"
            )[0], 200)
            summit_status, summit = request(
                "POST", f"{prefix}/mountain/decide",
                {"option_id": "pay_card_18k"},
            )
            self.assertEqual(summit_status, 200)
            self.assertTrue(summit["completed"])
            brief_status, brief = request("GET", f"{prefix}/advisor-brief")
            self.assertEqual(brief_status, 200)
            self.assertEqual(brief["step_1"], SEED_CASES[
                "timothy-melanie-weah"]["step_1"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_session_get_endpoints_accept_non_mutating_mode_query(self):
        """Apply URL display mode to all requested session GET routes."""
        store = SessionStore()
        _, session = dispatch_request(
            "POST", "/api/sessions", {"case_id": "michael-carter"},
            store=store,
        )
        session_id = session["session_id"]
        dispatch_request("POST", f"/api/sessions/{session_id}/quest",
                         {"ranked_concerns": ["O1"]}, store=store)
        paths = (
            f"/api/sessions/{session_id}",
            f"/api/sessions/{session_id}/mountain",
            f"/api/sessions/{session_id}/mountain/overview",
            f"/api/sessions/{session_id}/advisor-brief",
        )
        for path in paths:
            with self.subTest(path=path):
                status, data = dispatch_request(
                    "GET", f"{path}?mode=math", store=store
                )
                self.assertEqual(status, 200)
                self.assertEqual(data["mode"], "math")
        self.assertEqual(store.get(session_id).mode, "plain")


if __name__ == "__main__":
    unittest.main()
