import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from backend.mcp_client import (SherpasMCPClient, CaseNotFoundError, InvalidSectionError,
                                MCPAuthError, MCPTransportError, load_env_file)

ROOT = Path(__file__).resolve().parents[1]


def patch_env(**values):
    return patch.dict(os.environ, values, clear=False)


class MCPHandler(BaseHTTPRequestHandler):
    mode = "json"
    calls = []

    def log_message(self, *args): pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))))
        self.calls.append((body, dict(self.headers)))
        if self.mode == "timeout":
            time.sleep(.3)
            return
        if self.mode in ("401", "403"):
            self.send_response(int(self.mode))
            self.end_headers()
            return
        method = body["method"]
        if method == "notifications/initialized":
            self.send_response(202)
            self.end_headers()
            return
        if method == "initialize": result = {"protocolVersion":"2025-03-26","capabilities":{}}
        elif method == "tools/call":
            name, args = body["params"]["name"], body["params"]["arguments"]
            if name == "list_cases" and self.mode == "expired_once" and not getattr(self, "expired", False):
                self.expired = True
                self._reply(body, error={"code": -32000, "message": "session expired"})
                return
            if name == "list_cases":
                cases = ["demo"] if self.mode == "strings" else [{"id":"demo", "source":"mcp"}]
                result = {"content":[{"type":"text","text":json.dumps(cases)}]}
            elif self.mode == "requires_section" and "section" not in args:
                self._reply(body, error={"code":-32602,"message":"section required"})
                return
            elif self.mode == "section_error" and ("section" not in args or args.get("section") == "investment-analysis"):
                self._reply(body, error={"code":-32602,"message":"section call failed"})
                return
            elif "section" in args:
                value = ({"section":args["section"]} if self.mode == "requires_section" else
                         {"financial-health":{"score":9},"investment-analysis":{"x":1},"persona":"hello"}[args["section"]])
                result = {"content":[{"type":"text","text":json.dumps(value)}]}
            else: result = {"case_id":args["case_id"],"financial-health":{"score":9},"investment-analysis":{"x":1},"persona":"hello"}
        else: result = {}
        if self.mode == "sse":
            payload = json.dumps({"jsonrpc":"2.0","id":body.get("id"),"result":result})
            left, right = payload.split(', "result":', 1)
            raw = (": comment\n" + "data: " + left + ",\ndata: " + '"result": ' + right + "\n\n").encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        else: self._reply(body, result=result)

    def _reply(self, body, result=None, error=None):
        value = {"jsonrpc":"2.0","id":body.get("id")}
        value["error" if error else "result"] = error if error else result
        raw = json.dumps(value).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        if body.get("method") == "initialize": self.send_header("Mcp-Session-Id","session-123")
        self.end_headers()
        self.wfile.write(raw)


class MCPClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), MCPHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = "http://127.0.0.1:%d/mcp" % cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        MCPHandler.mode = "json"
        MCPHandler.calls = []
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cases = Path(self.tmp.name) / "cases"
        self.cases.mkdir()

    def client(self, token="secret", **kwargs):
        return SherpasMCPClient(self.url, token, cases_dir=self.cases, **kwargs)

    def make_case(self, cid="demo"):
        folder = self.cases / cid
        folder.mkdir()
        (folder / "financial-health.json").write_text(json.dumps({"name":"Demo","score":42,"status":"strong","household_type":"single"}), encoding="utf-8")
        (folder / "investment-analysis.json").write_text('{"assets":[]}', encoding="utf-8")
        (folder / "persona.md").write_text("persona text", encoding="utf-8")

    def test_namespace_package_and_utf8_files_have_no_bom(self):
        self.assertFalse((ROOT / "backend" / "__init__.py").exists())
        for path in (ROOT / ".env.example", ROOT / "backend" / "mcp_client.py", Path(__file__)):
            self.assertFalse(path.read_bytes().startswith(b"\xef\xbb\xbf"), str(path))

    def test_cases_dir_environment_resolution(self):
        sherpas_dir = Path(self.tmp.name) / "sherpas-cases"
        cases_dir = Path(self.tmp.name) / "cases-env"
        with patch_env(SHERPAS_CASES_DIR=str(sherpas_dir), CASES_DIR=str(cases_dir)):
            self.assertEqual(SherpasMCPClient(self.url, "secret").cases_dir, sherpas_dir)
        with patch_env(SHERPAS_CASES_DIR="", CASES_DIR=str(cases_dir)):
            self.assertEqual(SherpasMCPClient(self.url, "secret").cases_dir, cases_dir)

    def test_local_files_and_env_file_read_utf8_bom(self):
        folder = self.cases / "demo"
        folder.mkdir()
        (folder / "financial-health.json").write_bytes(b"\xef\xbb\xbf" + b'{"name":"BOM","score":3}')
        (folder / "investment-analysis.json").write_bytes(b"\xef\xbb\xbf" + b'{"assets":[]}')
        (folder / "persona.md").write_bytes(b"\xef\xbb\xbfpersona")
        result = self.client(token="").get_case("demo")
        self.assertEqual(result["financial-health"]["name"], "BOM")
        self.assertEqual(result["investment-analysis"], {"assets": []})
        self.assertEqual(result["persona"], "persona")
        envfile = Path(self.tmp.name) / "bom.env"
        envfile.write_bytes(b"\xef\xbb\xbf" + b"MCP_TOKEN=bom-token\n")
        with patch.dict(os.environ, {}, clear=True):
            load_env_file(envfile)
            self.assertEqual(os.environ["MCP_TOKEN"], "bom-token")

    def test_env_example_exact_keys_no_secret(self):
        lines = (ROOT / ".env.example").read_text().splitlines()
        self.assertEqual(lines, ["MCP_URL=https://mcp-hackathon.sherpaswealth.com/mcp","MCP_TOKEN=","LLM_PROXY_URL=https://llm-hackathon.sherpaswealth.com/v1","TEAM_KEY=","N8N_WEBHOOK_URL=","N8N_WEBHOOK_SECRET=","TELEGRAM_BOT_USERNAME=SherpasRadioBot","# Avisos automaticos (ver docs/TELEGRAM_N8N.md)","SHERPAS_SCHEDULER_INTERVAL=0","SHERPAS_DAY_SECONDS=86400","SHERPAS_MAX_DAY=90","SHERPAS_OUTBOX_DIR=","SHERPAS_ENABLE_TELEGRAM_TEST=","SHERPAS_NOTIFY_DAYS=","SHERPAS_DEMO_CASES="])

    def test_json_initialize_auth_headers_session_and_tools(self):
        c = self.client()
        self.assertEqual(c.list_cases(), [{"id":"demo", "source":"mcp"}])
        self.assertEqual(c.last_source, "mcp")
        full = c.get_case("demo")
        self.assertEqual(full["financial-health"], {"score":9})
        fresh = self.client()
        fresh.get_case("demo")
        self.assertEqual(fresh.last_source, "mcp")
        self.assertIsNone(fresh.last_fallback_reason)
        self.assertEqual(c.get_case("demo", "financial_health"), {"score":9})
        self.assertEqual(c.get_case("demo", "investment_analysis"), {"x":1})
        self.assertEqual(c.get_case("demo", "persona"), "hello")
        calls = MCPHandler.calls
        self.assertTrue(any(x[0]["method"] == "initialize" and x[0]["params"]["protocolVersion"] == "2025-03-26" for x in calls))
        self.assertTrue(any(x[0]["method"] == "notifications/initialized" for x in calls))
        tool_headers = [headers for body,headers in calls if body["method"] == "tools/call"]
        self.assertTrue(all(h["Authorization"] == "Bearer secret" for h in tool_headers))
        self.assertTrue(any(h.get("Mcp-Session-Id") == "session-123" for h in tool_headers))
        self.assertTrue(any(body["method"] == "tools/call" and body["params"]["arguments"].get("section") == "financial-health" for body, _ in calls))

    def test_server_requires_section_combines_three_sections(self):
        MCPHandler.mode = "requires_section"
        result = self.client().get_case("demo")
        self.assertEqual(result["financial-health"], {"section":"financial-health"})
        self.assertEqual(result["investment-analysis"], {"section":"investment-analysis"})
        self.assertEqual(result["persona"], '{"section": "persona"}')

    def test_section_rpc_error_falls_back_to_local_or_seed(self):
        MCPHandler.mode = "section_error"
        self.make_case()
        local_client = self.client()
        local = local_client.get_case("demo")
        self.assertEqual(local["persona"], "persona text")
        self.assertEqual(local_client.last_source, "local")
        seed_client = self.client()
        seed = seed_client.get_case("michael-carter")
        self.assertEqual(seed["financial-health"]["score"]["overall"], 26)
        self.assertEqual(seed_client.last_source, "seed")

    def test_sse(self):
        MCPHandler.mode = "sse"
        self.assertEqual(self.client().list_cases(), [{"id":"demo", "source":"mcp"}])

    def test_local_fallback_token_401_403_timeout_and_metadata(self):
        self.make_case()
        c = self.client(token="")
        self.assertEqual(c.get_case("demo", "persona"), "persona text")
        self.assertEqual((c.last_source,c.last_fallback_reason), ("local","missing_token"))
        for mode, reason in (("401","http_401"),("403","http_403"),("timeout","timeout")):
            MCPHandler.mode = mode
            c = self.client(timeout=.05)
            cases = c.list_cases()
            self.assertEqual(c.last_source, "local")
            self.assertEqual(c.last_fallback_reason, reason)
            self.assertEqual(cases[0]["score"], 42)
            self.assertEqual(cases[0]["household_type"], "single")

    def test_seed_fallback_all_four_cases_and_deepcopy(self):
        c = self.client(token="")
        ids = ["michael-carter", "samantha-lewis", "timothy-melanie-weah", "daniel-emily-johnson"]
        self.assertEqual({x["id"] for x in c.list_cases()}, set(ids))

        names = ["Savings & cash flow", "Debt", "Investments", "Liquidity", "Protection"]
        maxima = [25, 10, 25, 20, 20]
        expected_scores = [[0, 8, 11, 4, 4], [None] * 5, [None] * 5, [None, None, None, None, 0]]
        cases = [c.get_case(case_id) for case_id in ids]
        for case, scores in zip(cases, expected_scores):
            with self.subTest(case=case["financial-health"]["case_id"]):
                pillars = case["financial-health"]["score"]["pillars"]
                self.assertEqual([pillar["name"] for pillar in pillars], names)
                self.assertEqual([pillar["max"] for pillar in pillars], maxima)
                self.assertEqual([pillar["score"] for pillar in pillars], scores)

        michael, samantha, weah, johnson = cases
        michael_score = michael["financial-health"]["score"]
        self.assertEqual(michael_score["overall"], 26)
        yearly = michael["financial-health"]["projections"]["yearly"]
        self.assertEqual(len(yearly), 12)
        self.assertEqual([row["year"] for row in yearly], [2026, 2027, 2032, 2038, 2044, 2050, 2056, 2062, 2068, 2074, 2075, 2080])
        self.assertEqual(next(row for row in yearly if row["year"] == 2075)["investable_assets"], -38276)
        self.assertEqual(michael["investment-analysis"]["analysis"]["recovery_days"], 62)
        self.assertIn("Subjective concerns: None recorded", michael["persona"])
        michael_score["overall"] = 0
        self.assertEqual(c.get_case(ids[0])["financial-health"]["score"]["overall"], 26)
        self.assertEqual(next(row for row in samantha["financial-health"]["projections"]["yearly"] if row["year"] == 2053)["investable_assets"], -227414)
        self.assertEqual(weah["financial-health"]["score"]["combined_moves"][0]["score_after"], 78)
        self.assertEqual(weah["financial-health"]["score"]["combined_target_score"], 78)
        self.assertEqual(johnson["financial-health"]["score"]["combined_target_score"], 60)
        self.assertEqual(c.last_source, "seed")

    def test_validation_not_found_and_no_fallback(self):
        c = self.client(token="")
        with self.assertRaises(CaseNotFoundError): c.get_case("not-a-case")
        for section in ("bad","../x"):
            with self.assertRaises(InvalidSectionError): c.get_case("demo",section)
        for case_id in ("../x","a/b","a\\b"):
            with self.assertRaises(ValueError): c.get_case(case_id)
        with self.assertRaises(MCPAuthError): self.client(token="",allow_fallback=False).list_cases()
        MCPHandler.mode = "401"
        with self.assertRaises(MCPAuthError): self.client(allow_fallback=False).list_cases()
        MCPHandler.mode = "timeout"
        with self.assertRaises(MCPTransportError): self.client(allow_fallback=False,timeout=.05).list_cases()

    def test_explicit_empty_token_does_not_load_env_file(self):
        envfile = Path(self.tmp.name) / ".env"
        envfile.write_text("MCP_TOKEN=should-not-load\n",encoding="utf-8")
        c = SherpasMCPClient(self.url, "", cases_dir=self.cases, env_file=envfile)
        self.assertEqual(c.token, "")

    def test_module_functions_list_and_get_case(self):
        from backend.mcp_client import get_case, list_cases
        self.assertEqual(list_cases(self.url, "secret", cases_dir=self.cases)[0]["id"], "demo")
        self.assertEqual(get_case("demo", "financial-health", self.url, "secret", cases_dir=self.cases), {"score": 9})

    def test_partial_local_case_fills_missing_sections_from_seed(self):
        folder = self.cases / "michael-carter"
        folder.mkdir()
        (folder / "financial-health.json").write_text(json.dumps({"name": "Local Michael"}), encoding="utf-8")
        result = self.client(token="").get_case("michael-carter")
        self.assertEqual(result["financial-health"], {"name": "Local Michael"})
        self.assertEqual(result["investment-analysis"]["analysis"]["recovery_days"], 62)
        self.assertIn("D5: SINGLE", result["persona"])

    def test_list_cases_normalizes_mcp_strings_and_local_score_dict(self):
        MCPHandler.mode = "strings"
        self.assertEqual(self.client().list_cases()[0]["id"], "demo")
        self.make_case()
        path = self.cases / "demo" / "financial-health.json"
        path.write_text(json.dumps({"name": "Demo", "score": {"overall": 42, "status": "strong"}, "household_type": "SINGLE"}), encoding="utf-8")
        MCPHandler.mode = "401"
        local_case = self.client().list_cases()[0]
        self.assertEqual((local_case["score"], local_case["status"]), (42, "strong"))

    def test_expired_session_reinitializes(self):
        MCPHandler.mode = "expired_once"
        MCPHandler.expired = False
        self.client().list_cases()
        self.assertEqual(sum(body["method"] == "initialize" for body, _ in MCPHandler.calls), 2)


if __name__ == "__main__": unittest.main()

