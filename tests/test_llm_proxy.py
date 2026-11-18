"""Unit tests for backend.llm_proxy and backend.behavioral_narrator."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import urllib.error

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import backend.behavioral_narrator as narrator_mod
import backend.llm_proxy as llm_proxy_mod

from backend.behavioral_narrator import (
    ALL_BIAS_IDS,
    FALLBACK_CASES_DIR,
    SECTION_4_BIAS_IDS,
    SUPPORTED_CASES,
    BehavioralNarrator,
    build_cordada_pact,
    detect_behavioral_biases,
    explain_bias,
    extract_case_allowed_numbers,
    generate_advisor_brief,
    load_case,
    resolve_cases_dir,
    synthesize_cordada_pact,
    translate_dual_lens,
    verify_text_numbers_against_case,
)
from backend.llm_proxy import (
    BudgetExhaustedError,
    DEFAULT_MODEL,
    DEFAULT_PROXY_URL,
    GPT5_MINI_MIN_MAX_TOKENS,
    LLMProxyClient,
    RateLimitExceededError,
    build_chat_payload,
)


class _FakeHTTPResponse:
    def __init__(self, payload: dict) -> None:
        self._body = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> "_FakeHTTPResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class LLMProxyClientTests(unittest.TestCase):
    def test_dotenv_loading_and_secret_masking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env_file = Path(tmp) / ".env"
            env_file.write_text(
                'TEAM_KEY="sk-sherpas-secret-9876"\nLLM_PROXY_URL=https://custom-proxy.example.com/\n',
                encoding="utf-8",
            )
            with patch.dict(os.environ, {}, clear=True):
                client = LLMProxyClient(dotenv_path=env_file)

        self.assertTrue(client.has_team_key)
        self.assertEqual(client.base_url, "https://custom-proxy.example.com")
        self.assertEqual(client.default_model, DEFAULT_MODEL)
        self.assertNotIn("sk-sherpas-secret-9876", repr(client))
        self.assertIn("****9876", repr(client))

    def test_gpt5_mini_max_tokens_rule_and_model_validation(self) -> None:
        msgs = [{"role": "user", "content": "Resume el plan"}]
        omitted = build_chat_payload(msgs, model="gpt-5-mini")
        self.assertNotIn("max_tokens", omitted)
        self.assertNotIn("max_completion_tokens", omitted)

        clamped = build_chat_payload(msgs, model="gpt-5-mini", max_tokens=200, max_completion_tokens=400)
        self.assertEqual(clamped["max_tokens"], GPT5_MINI_MIN_MAX_TOKENS)
        self.assertEqual(clamped["max_completion_tokens"], GPT5_MINI_MIN_MAX_TOKENS)

        kept = build_chat_payload(msgs, model="gpt-5-mini", max_tokens=1600)
        self.assertEqual(kept["max_tokens"], 1600)

        deepseek = build_chat_payload(msgs, model="deepseek-flash", max_tokens=300)
        self.assertEqual(deepseek["max_tokens"], 300)

        with self.assertRaises(ValueError):
            build_chat_payload(msgs, model="unknown-model")

    def test_key_info_parses_budget_and_blocks_exhausted_calls(self) -> None:
        seen_requests: list[tuple[str, str, str]] = []

        def fake_urlopen(req, timeout=30):
            url = req.full_url
            auth = req.headers.get("Authorization", "")
            seen_requests.append((req.get_method(), url, auth))
            if url.endswith("/key/info"):
                return _FakeHTTPResponse(
                    {
                        "key": "sk-team-secret-should-be-stripped",
                        "info": {"spend": 12.5, "max_budget": 50.0, "team_id": "maximos-locales"},
                    }
                )
            return _FakeHTTPResponse(
                {
                    "id": "chatcmpl-1",
                    "model": "gpt-5-mini",
                    "choices": [{"message": {"role": "assistant", "content": "OK proxy"}}],
                    "usage": {"total_tokens": 42},
                }
            )

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            client = LLMProxyClient(team_key="sk-team-secret", transport="urllib")
            info = client.get_key_info()
            self.assertEqual(info.spend, 12.5)
            self.assertEqual(info.max_budget, 50.0)
            self.assertEqual(info.remaining_budget, 37.5)
            self.assertTrue(info.budget_available)
            self.assertNotIn("key", info.to_dict()["info"])

            resp = client.chat_completion(
                messages=[{"role": "user", "content": "Hola"}],
                model="gpt-5-mini",
                max_tokens=150,
            )
            self.assertFalse(resp.used_fallback)
            self.assertEqual(resp.content, "OK proxy")

        self.assertEqual(seen_requests[0][1], f"{DEFAULT_PROXY_URL}/key/info")
        self.assertEqual(seen_requests[0][2], "Bearer sk-team-secret")
        self.assertEqual(seen_requests[-1][1], f"{DEFAULT_PROXY_URL}/v1/chat/completions")

        # Now simulate exhausted $50 budget: /v1/chat/completions must NOT be called
        completion_calls = 0

        def exhausted_urlopen(req, timeout=30):
            nonlocal completion_calls
            if req.full_url.endswith("/key/info"):
                return _FakeHTTPResponse({"info": {"spend": 50.0, "max_budget": 50.0}})
            completion_calls += 1
            return _FakeHTTPResponse({"choices": [{"message": {"content": "should not run"}}]})

        with patch("urllib.request.urlopen", side_effect=exhausted_urlopen):
            client_fb = LLMProxyClient(team_key="sk-team-secret", fallback_on_error=True, transport="urllib")
            fb_resp = client_fb.chat_completion([{"role": "user", "content": "Test"}])
            self.assertTrue(fb_resp.used_fallback)
            self.assertIn("budget_exhausted", fb_resp.fallback_reason or "")
            self.assertEqual(completion_calls, 0)

            client_strict = LLMProxyClient(team_key="sk-team-secret", fallback_on_error=False, transport="urllib")
            with self.assertRaises(BudgetExhaustedError):
                client_strict.chat_completion([{"role": "user", "content": "Test"}])
            self.assertEqual(completion_calls, 0)

    def test_rate_limit_60_rpm_enforced_deterministically(self) -> None:
        now = [1000.0]

        def fake_clock() -> float:
            return now[0]

        def fake_urlopen(req, timeout=30):
            if req.full_url.endswith("/key/info"):
                return _FakeHTTPResponse({"info": {"spend": 1.0, "max_budget": 50.0}})
            return _FakeHTTPResponse(
                {"choices": [{"message": {"content": "ok"}}], "usage": {"total_tokens": 5}}
            )

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            client = LLMProxyClient(
                team_key="sk-rate-test",
                check_budget_before_call=False,
                fallback_on_error=False,
                block_on_rate_limit=False,
                clock=fake_clock,
                transport="urllib",
            )
            for i in range(60):
                now[0] = 1000.0 + (i * 0.5)
                resp = client.chat_completion([{"role": "user", "content": f"msg {i}"}])
                self.assertEqual(resp.content, "ok")

            # 61st request within the same 60s window must fail
            now[0] = 1045.0
            with self.assertRaises(RateLimitExceededError):
                client.chat_completion([{"role": "user", "content": "msg 61"}])

            # After advancing past 60s from the first request, quota frees up
            now[0] = 1060.1
            resp_after = client.chat_completion([{"role": "user", "content": "msg 61 ok"}])
            self.assertEqual(resp_after.content, "ok")

    def test_max_4_concurrent_requests_enforced(self) -> None:
        active_lock = threading.Lock()
        active_now = 0
        observed_peak = 0

        def slow_urlopen(req, timeout=30):
            nonlocal active_now, observed_peak
            with active_lock:
                active_now += 1
                if active_now > observed_peak:
                    observed_peak = active_now
            try:
                time.sleep(0.03)
                return _FakeHTTPResponse(
                    {"choices": [{"message": {"content": "concurrent ok"}}]}
                )
            finally:
                with active_lock:
                    active_now -= 1

        with patch("urllib.request.urlopen", side_effect=slow_urlopen):
            client = LLMProxyClient(
                team_key="sk-conc-test",
                check_budget_before_call=False,
                max_concurrent=4,
                concurrency_timeout=5.0,
                transport="urllib",
            )
            with ThreadPoolExecutor(max_workers=12) as pool:
                results = list(
                    pool.map(
                        lambda idx: client.chat_completion(
                            [{"role": "user", "content": f"req {idx}"}],
                            model="deepseek-flash",
                        ),
                        range(12),
                    )
                )

        self.assertEqual(len(results), 12)
        self.assertTrue(all(not r.used_fallback and r.content == "concurrent ok" for r in results))
        self.assertLessEqual(observed_peak, 4)
        self.assertLessEqual(client.concurrency_limiter.peak_concurrent_requests, 4)
        self.assertGreaterEqual(client.concurrency_limiter.peak_concurrent_requests, 2)

    def test_offline_missing_key_network_error_and_empty_content_fallback(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            offline_client = LLMProxyClient(team_key="", dotenv_path=Path("/nonexistent/.env"))
        offline_resp = offline_client.chat_completion(
            [{"role": "user", "content": "Explica liquidez"}],
            fallback_context={"deterministic_text": "Tienes 3.2 meses cubiertos."},
        )
        self.assertTrue(offline_resp.used_fallback)
        self.assertEqual(offline_resp.fallback_reason, "missing_team_key")
        self.assertEqual(offline_resp.content, "Tienes 3.2 meses cubiertos.")

        # Network URLError fallback
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("offline")):
            net_client = LLMProxyClient(team_key="sk-net", check_budget_before_call=False, fallback_on_error=True)
            net_resp = net_client.chat_completion([{"role": "user", "content": "Test"}])
            self.assertTrue(net_resp.used_fallback)
            self.assertIn("URLError", net_resp.fallback_reason or "")

        # Empty content returned by proxy triggers deterministic fallback
        def empty_urlopen(req, timeout=30):
            return _FakeHTTPResponse({"choices": [{"message": {"content": "   "}}]})

        with patch("urllib.request.urlopen", side_effect=empty_urlopen):
            empty_client = LLMProxyClient(team_key="sk-empty", check_budget_before_call=False, fallback_on_error=True)
            empty_resp = empty_client.chat_completion([{"role": "user", "content": "Test"}])
            self.assertTrue(empty_resp.used_fallback)
            self.assertIn("Empty completion", empty_resp.fallback_reason or "")

    def test_openai_sdk_compatible_transport_when_available(self) -> None:
        captured: dict = {}

        class _FakeCompletions:
            def create(self, **kwargs):
                captured["payload"] = kwargs
                return SimpleNamespace(
                    model_dump=lambda: {
                        "model": kwargs["model"],
                        "choices": [{"message": {"content": "Respuesta OpenAI SDK"}}],
                        "usage": {"total_tokens": 21},
                    }
                )

        class _FakeOpenAI:
            def __init__(self, api_key: str, base_url: str, timeout: float) -> None:
                captured["api_key"] = api_key
                captured["base_url"] = base_url
                self.chat = SimpleNamespace(completions=_FakeCompletions())

        fake_sdk = SimpleNamespace(OpenAI=_FakeOpenAI)
        with patch.object(llm_proxy_mod, "_openai_sdk", fake_sdk):
            client = LLMProxyClient(
                team_key="sk-sdk-key",
                check_budget_before_call=False,
                transport="openai",
            )
            resp = client.chat_completion(
                messages=[{"role": "user", "content": "Hola SDK"}],
                model="gpt-5-mini",
                max_tokens=300,
            )

        self.assertFalse(resp.used_fallback)
        self.assertEqual(resp.transport, "openai_sdk")
        self.assertEqual(resp.content, "Respuesta OpenAI SDK")
        self.assertEqual(captured["base_url"], f"{DEFAULT_PROXY_URL}/v1")
        self.assertEqual(captured["payload"]["max_tokens"], 1000)


class BehavioralNarratorTests(unittest.TestCase):
    def test_loads_all_four_real_cases_and_persona_sections(self) -> None:
        for case_id in SUPPORTED_CASES:
            case = load_case(case_id)
            self.assertGreater(case.published_score, 0)
            self.assertEqual(len(case.pillars), 5)
            self.assertGreaterEqual(len(case.persona.objective_concerns), 7)
            self.assertGreaterEqual(len(case.persona.tensions), 3)
            self.assertFalse(case.persona.has_subjective_concerns)
            self.assertEqual(len(case.analysis_events), 11)
            self.assertEqual(len(case.per_event_drawdowns), 11)
            self.assertGreaterEqual(len(case.savings_waterfall), 16)

    def test_cases_dir_resolution_via_env_var_and_utf8_bom(self) -> None:
        real_dir = load_case("michael-carter").case_dir.parent
        self.assertEqual(FALLBACK_CASES_DIR, _ROOT / "cases")
        narrator_src = (_ROOT / "backend" / "behavioral_narrator.py").read_text(encoding="utf-8")
        self.assertNotIn("C:\\Users\\", narrator_src)
        with patch.dict(os.environ, {"SHERPAS_CASES_DIR": str(real_dir)}):
            c = load_case("samantha-lewis")
            self.assertEqual(c.case_id, "samantha-lewis")

        with tempfile.TemporaryDirectory() as tmp:
            bom_root = Path(tmp) / "cases"
            src = real_dir / "michael-carter"
            dst = bom_root / "michael-carter"
            dst.mkdir(parents=True)
            for fname in ("financial-health.json", "investment-analysis.json", "persona.md"):
                raw = (src / fname).read_text(encoding="utf-8")
                (dst / fname).write_bytes(b"\xef\xbb\xbf" + raw.encode("utf-8"))
            with patch.dict(os.environ, {"SHERPAS_CASES_DIR": "", "CASES_DIR": str(bom_root)}, clear=False):
                loaded = load_case("michael-carter")
                self.assertEqual(loaded.case_dir.parent, bom_root)
                self.assertEqual(loaded.published_score, 26)

    def test_embedded_cases_fallback_when_no_cases_on_disk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            empty_cwd = tmp_path / "empty_cwd"
            empty_cwd.mkdir()
            fake_repo_file = tmp_path / "isolated_repo" / "backend" / "behavioral_narrator.py"
            fake_repo_file.parent.mkdir(parents=True)
            isolated_temp = tmp_path / "tmp_cache"
            isolated_temp.mkdir()

            with (
                patch.object(narrator_mod, "__file__", str(fake_repo_file)),
                patch.object(Path, "cwd", return_value=empty_cwd),
                patch.object(tempfile, "gettempdir", return_value=str(isolated_temp)),
                patch.dict(os.environ, {"SHERPAS_CASES_DIR": "", "CASES_DIR": "", "MCP_TOKEN": ""}, clear=False),
            ):
                resolved = resolve_cases_dir()
                self.assertTrue(resolved.is_dir())
                self.assertEqual(resolved.parent, isolated_temp)

                michael = load_case("michael-carter")
                self.assertEqual(michael.published_score, 26)
                self.assertEqual(len(michael.analysis_events), 11)

                narrator = BehavioralNarrator()
                self.assertEqual(sorted(narrator.list_cases()), sorted(SUPPORTED_CASES))
                dl = narrator.translate_dual_lens("michael-carter", topic="home_purchase")
                self.assertIn("$81,172", dl["plain"]["summary"])
                biases = {b["bias_id"]: b for b in narrator.detect_behavioral_biases("samantha-lewis")}
                self.assertTrue(biases["halo_effect"]["triggered"])
                brief = narrator.generate_advisor_brief("daniel-emily-johnson")
                self.assertTrue(brief["couple_disagreements"]["is_couple"])

                with self.assertRaises(FileNotFoundError):
                    resolve_cases_dir(cases_dir=tmp_path / "nonexistent_cases")

    def test_env_vars_override_existing_project_root_cases_dir(self) -> None:
        real_dir = load_case("michael-carter").case_dir.parent
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake_repo_root = tmp_path / "repo"
            fake_repo_file = fake_repo_root / "backend" / "behavioral_narrator.py"
            fake_repo_file.parent.mkdir(parents=True)

            # Populate project_root/cases AND two distinct env override folders
            root_cases = fake_repo_root / "cases"
            env_sherpas = tmp_path / "override_sherpas"
            env_cases = tmp_path / "override_cases"
            for target_root in (root_cases, env_sherpas, env_cases):
                src = real_dir / "michael-carter"
                dst = target_root / "michael-carter"
                dst.mkdir(parents=True)
                for fname in ("financial-health.json", "investment-analysis.json", "persona.md"):
                    (dst / fname).write_bytes((src / fname).read_bytes())

            with (
                patch.object(narrator_mod, "__file__", str(fake_repo_file)),
                patch.object(Path, "cwd", return_value=fake_repo_root),
            ):
                with patch.dict(
                    os.environ,
                    {"SHERPAS_CASES_DIR": str(env_sherpas), "CASES_DIR": str(env_cases)},
                    clear=False,
                ):
                    self.assertEqual(resolve_cases_dir(), env_sherpas)

                with patch.dict(
                    os.environ,
                    {"SHERPAS_CASES_DIR": "", "CASES_DIR": str(env_cases)},
                    clear=False,
                ):
                    self.assertEqual(resolve_cases_dir(), env_cases)

                with patch.dict(
                    os.environ,
                    {"SHERPAS_CASES_DIR": "", "CASES_DIR": ""},
                    clear=False,
                ):
                    self.assertEqual(resolve_cases_dir(), root_cases)

                # Explicit cases_dir always wins over env vars and project_root/cases
                with patch.dict(
                    os.environ,
                    {"SHERPAS_CASES_DIR": str(env_sherpas), "CASES_DIR": str(env_cases)},
                    clear=False,
                ):
                    self.assertEqual(resolve_cases_dir(cases_dir=root_cases), root_cases)

    def test_dual_lens_plain_and_math_no_invented_numbers(self) -> None:
        topics = ("overview", "liquidity", "debt", "retirement", "protection", "investments", "home_purchase")
        for case_id in SUPPORTED_CASES:
            case = load_case(case_id)
            allowed = extract_case_allowed_numbers(case)
            for topic in topics:
                dl = translate_dual_lens(case_id, topic=topic, lens="both", use_llm=False)
                self.assertIn("plain", dl)
                self.assertIn("math", dl)
                self.assertTrue(dl["plain"]["months_of_life_covered"])
                self.assertTrue(dl["plain"]["family_peace_of_mind"])
                self.assertTrue(dl["plain"]["bias_unlock"])
                self.assertTrue(dl["math"]["json_sources"])
                combined_text = (
                    dl["plain"]["headline"]
                    + " "
                    + dl["plain"]["summary"]
                    + " "
                    + dl["math"]["summary"]
                )
                ok, bad = verify_text_numbers_against_case(combined_text, allowed)
                self.assertTrue(ok, f"Unverified numbers in {case_id}/{topic}: {bad}")

    def test_dual_lens_llm_enrichment_rejects_invented_numbers_and_accepts_grounded(self) -> None:
        # 1. Hallucinated number $987,654 must be rejected -> fallback to deterministic
        def hallucinating_urlopen(req, timeout=30):
            return _FakeHTTPResponse(
                {
                    "choices": [
                        {
                            "message": {
                                "content": json.dumps(
                                    {
                                        "plain_summary": "Debes ahorrar $987,654 extra al 19.75% anual.",
                                        "math_summary": "Meta $987,654.",
                                    }
                                )
                            }
                        }
                    ]
                }
            )

        with patch("urllib.request.urlopen", side_effect=hallucinating_urlopen):
            client = LLMProxyClient(team_key="sk-test", check_budget_before_call=False, transport="urllib")
            dl_rejected = translate_dual_lens("michael-carter", topic="overview", use_llm=True, llm_client=client)
            self.assertFalse(dl_rejected["used_llm"])
            self.assertTrue(dl_rejected["llm_fallback_used"])
            self.assertIn("unverified_numbers_detected", dl_rejected["fallback_reason"] or "")

        # 2. Grounded numbers ($178,717 and $81,172 from 2026->2027) must be accepted
        def grounded_urlopen(req, timeout=30):
            return _FakeHTTPResponse(
                {
                    "choices": [
                        {
                            "message": {
                                "content": json.dumps(
                                    {
                                        "plain_summary": "La compra de $550,000 en 2027 baja la liquidez a $81,172.",
                                        "math_summary": "investable_assets pasa de $178,717 en 2026 a $81,172 en 2027.",
                                    }
                                )
                            }
                        }
                    ]
                }
            )

        with patch("urllib.request.urlopen", side_effect=grounded_urlopen):
            client = LLMProxyClient(team_key="sk-test", check_budget_before_call=False, transport="urllib")
            dl_ok = translate_dual_lens("michael-carter", topic="home_purchase", use_llm=True, llm_client=client)
            self.assertTrue(dl_ok["used_llm"])
            self.assertFalse(dl_ok["llm_fallback_used"])
            self.assertIn("$81,172", dl_ok["plain"]["enriched_summary"])

    def test_all_section_4_and_appendix_a_biases_across_cases(self) -> None:
        self.assertEqual(len(SECTION_4_BIAS_IDS), 13)
        self.assertIn("ikea_effect", ALL_BIAS_IDS)

        # Verify every bias can be explained cleanly with zero invented numbers across all 4 cases
        for case_id in SUPPORTED_CASES:
            case = load_case(case_id)
            allowed = extract_case_allowed_numbers(case)
            for bias_id in ALL_BIAS_IDS:
                ex = explain_bias(case_id, bias_id)
                ok, bad = verify_text_numbers_against_case(ex["plain"] + " " + ex["math"], allowed)
                self.assertTrue(ok, f"Unverified numbers in {case_id}/{bias_id}: {bad}")

        # Specific Section 4 / Appendix B behavioral checks
        weah_biases = {b["bias_id"]: b for b in detect_behavioral_biases("timothy-melanie-weah")}
        self.assertTrue(weah_biases["mental_accounting"]["triggered"])
        self.assertIn("$150,800", weah_biases["mental_accounting"]["math"])
        self.assertIn("$3,240", weah_biases["mental_accounting"]["math"])
        self.assertTrue(weah_biases["loss_aversion_recency"]["triggered"])
        self.assertIn("UPRO", weah_biases["loss_aversion_recency"]["math"])
        self.assertTrue(weah_biases["couples_veto"]["triggered"])

        samantha_biases = {b["bias_id"]: b for b in detect_behavioral_biases("samantha-lewis")}
        self.assertTrue(samantha_biases["halo_effect"]["triggered"])
        self.assertIn("2053", samantha_biases["halo_effect"]["math"])
        self.assertIn("-$227,414", samantha_biases["halo_effect"]["math"])
        self.assertTrue(samantha_biases["oxygen_mask_syndrome"]["triggered"])

        michael_biases = {b["bias_id"]: b for b in detect_behavioral_biases("michael-carter")}
        self.assertTrue(michael_biases["house_rich_cash_poor"]["triggered"])
        self.assertIn("-$38,276", michael_biases["house_rich_cash_poor"]["math"])
        self.assertTrue(michael_biases["present_bias"]["triggered"])
        self.assertIn("$81,172", michael_biases["present_bias"]["math"])
        self.assertTrue(michael_biases["planning_fallacy"]["triggered"])
        self.assertIn("$5,665", michael_biases["planning_fallacy"]["math"])
        self.assertIn("$9,464", michael_biases["planning_fallacy"]["math"])
        self.assertTrue(michael_biases["ostrich_effect"]["triggered"])
        self.assertIn("23.9%", michael_biases["ostrich_effect"]["math"])
        self.assertIn("26 -> 62", michael_biases["ostrich_effect"]["math"])

        johnson_biases = {b["bias_id"]: b for b in detect_behavioral_biases("daniel-emily-johnson")}
        self.assertTrue(johnson_biases["mental_accounting"]["triggered"])
        self.assertIn("24.9%", johnson_biases["mental_accounting"]["math"])
        self.assertTrue(johnson_biases["optimism_bias"]["triggered"])
        self.assertIn("0/20", johnson_biases["optimism_bias"]["math"])
        self.assertTrue(johnson_biases["oxygen_mask_syndrome"]["triggered"])
        self.assertIn("$11,760", johnson_biases["oxygen_mask_syndrome"]["math"])
        self.assertTrue(johnson_biases["couples_veto"]["triggered"])

    def test_cordada_asimetrica_pact_synthesis(self) -> None:
        weah_pact = synthesize_cordada_pact(
            "timothy-melanie-weah",
            member_a_votes={"top_fears": ["O1", "O3"], "risk_choice": "Growth", "votes": {"debt": "keep_upro"}},
            member_b_votes={"top_fears": ["O1", "O2"], "risk_choice": "Moderate", "votes": {"debt": "pay_card"}},
        )
        self.assertTrue(weah_pact["is_couple"])
        self.assertTrue(weah_pact["shared_100_percent"])
        self.assertGreaterEqual(len(weah_pact["friction_points"]), 1)
        self.assertIn("60 -> 78", weah_pact["math_summary"])
        self.assertIn("Melanie", weah_pact["midpoint_pact"]["owner_b_action"])

        johnson_pact = build_cordada_pact(
            "daniel-emily-johnson",
            member_a_votes={"top_fears": ["O2", "O1"], "risk_choice": "Growth"},
            member_b_votes={"top_fears": ["O2", "O4"], "risk_choice": "Moderate"},
        )
        self.assertTrue(johnson_pact["is_couple"])
        self.assertIn("52 -> 60", johnson_pact["math_summary"])

        single_pact = synthesize_cordada_pact("michael-carter")
        self.assertFalse(single_pact["is_couple"])

    def test_advisor_brief_compiles_fears_tensions_couples_and_unmodeled_questions(self) -> None:
        narrator = BehavioralNarrator()

        m_brief = narrator.generate_advisor_brief(
            "michael-carter",
            fear_ranking=["O2", "O1"],
            subjective_concerns=["Miedo a comprar la casa en 2027 y quedarme sin liquidez"],
            skipped_moves=["Lower the withdrawal rate"],
        )
        self.assertEqual(m_brief["fear_ranking"][0]["id"], "O2")
        self.assertEqual(m_brief["fear_ranking"][1]["id"], "O1")
        self.assertEqual(len(m_brief["tensions"]), 5)
        self.assertFalse(m_brief["couple_disagreements"]["is_couple"])
        self.assertIn("None detected", m_brief["subjective_concerns"]["persona_md_status"])
        self.assertEqual(len(m_brief["subjective_concerns"]["captured_from_user"]), 1)
        self.assertTrue(
            any("2027" in q["question"] and "$550,000" in q["question"] for q in m_brief["unmodeled_goal_questions"])
        )

        j_brief = generate_advisor_brief(
            "daniel-emily-johnson",
            fear_ranking=["O2"],
            couple_votes={
                "member_a": {"top_fears": ["O2"], "risk_choice": "Growth"},
                "member_b": {"top_fears": ["O2", "O4"], "risk_choice": "Moderate"},
                "nodes": [{"node": "2026_cash", "vote_a": "brokerage", "vote_b": "emergency_fund"}],
            },
        )
        self.assertTrue(j_brief["couple_disagreements"]["is_couple"])
        self.assertGreaterEqual(len(j_brief["couple_disagreements"]["disagreements"]), 2)
        self.assertEqual(len(j_brief["tensions"]), 5)
        self.assertTrue(any("$15,032" in q for q in j_brief["advisor_questions"]))

        s_brief = narrator.generate_advisor_brief("samantha-lewis")
        self.assertTrue(any("2030" in q["question"] and "$500,000" in q["question"] for q in s_brief["unmodeled_goal_questions"]))
        self.assertEqual(len(s_brief["tensions"]), 3)

        w_brief = narrator.generate_advisor_brief("timothy-melanie-weah")
        self.assertTrue(any("2030" in q["question"] and "$600,000" in q["question"] for q in w_brief["unmodeled_goal_questions"]))
        self.assertTrue(w_brief["couple_disagreements"]["is_couple"])


if __name__ == "__main__":
    unittest.main()
