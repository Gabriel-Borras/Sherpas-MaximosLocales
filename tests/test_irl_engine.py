"""Suite de pruebas para backend/irl_engine.py y backend/notifications.py (Issue #5)."""

from __future__ import annotations

from datetime import date
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest import mock

from backend.irl_engine import (
    DEFAULT_FALLBACK_CASES_DIR,
    SUPPORTED_CASES,
    IRLEngine,
    create_irl_run,
    list_available_cases,
    load_case_data,
)
from backend.notifications import NotificationEngine


class TestCaseResolution(unittest.TestCase):
    def test_all_four_real_cases_available_and_loaded(self) -> None:
        cases = list_available_cases()
        for case_id in SUPPORTED_CASES:
            self.assertIn(case_id, cases)
            data = load_case_data(case_id)
            self.assertEqual(data["case_id"], case_id)
            self.assertEqual(len(data["investment_analysis"]["analysis"]["events"]), 11)
            self.assertGreaterEqual(
                len(
                    data["investment_analysis"]["key_metrics"][
                        "savingsAndContributions"
                    ]["savingsWaterfall"]
                ),
                16,
            )

    def test_env_var_cases_dir_resolution(self) -> None:
        src = Path(load_case_data("michael-carter")["case_dir"])
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "michael-carter"
            target.mkdir()
            for fname in ("financial-health.json", "investment-analysis.json", "persona.md"):
                (target / fname).write_text((src / fname).read_text(encoding="utf-8"), encoding="utf-8")

            prev = os.environ.get("SHERPAS_CASES_DIR")
            try:
                os.environ["SHERPAS_CASES_DIR"] = tmp
                resolved = load_case_data("michael-carter")
                self.assertEqual(Path(resolved["case_dir"]).resolve(), target.resolve())
            finally:
                if prev is None:
                    os.environ.pop("SHERPAS_CASES_DIR", None)
                else:
                    os.environ["SHERPAS_CASES_DIR"] = prev

    def test_cases_dir_env_var_and_utf8_bom_and_portable_fallback(self) -> None:
        repo_root = Path(__file__).resolve().parent.parent
        self.assertEqual(DEFAULT_FALLBACK_CASES_DIR, repo_root / "cases")
        for rel in ("backend/irl_engine.py", "backend/notifications.py"):
            src_text = (repo_root / rel).read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"[A-Za-z]:\\\\Users\\\\|/Users/[^/]+/|/home/[^/]+/", src_text))
        src = Path(load_case_data("michael-carter")["case_dir"])
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "michael-carter"
            target.mkdir()
            for fname in ("financial-health.json", "investment-analysis.json", "persona.md"):
                content = (src / fname).read_text(encoding="utf-8-sig")
                (target / fname).write_text("\ufeff" + content, encoding="utf-8")

            prev_sherpas = os.environ.pop("SHERPAS_CASES_DIR", None)
            prev_cases = os.environ.get("CASES_DIR")
            try:
                os.environ["CASES_DIR"] = tmp
                resolved = load_case_data("michael-carter")
                self.assertEqual(Path(resolved["case_dir"]).resolve(), target.resolve())
                self.assertEqual(resolved["financial_health"]["score"]["published_score"], 26)
            finally:
                if prev_sherpas is not None:
                    os.environ["SHERPAS_CASES_DIR"] = prev_sherpas
                if prev_cases is None:
                    os.environ.pop("CASES_DIR", None)
                else:
                    os.environ["CASES_DIR"] = prev_cases

    def test_unknown_case_raises_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            load_case_data("non-existent-case")

    def test_embedded_fallback_works_without_cases_dir_on_disk(self) -> None:
        with tempfile.TemporaryDirectory() as empty_workspace, tempfile.TemporaryDirectory() as isolated_tmp:
            empty_repo = Path(empty_workspace) / "repo"
            empty_repo.mkdir()
            empty_cwd = Path(empty_workspace) / "cwd"
            empty_cwd.mkdir()

            clean_env = {
                k: v
                for k, v in os.environ.items()
                if k not in ("SHERPAS_CASES_DIR", "CASES_DIR")
            }
            with (
                mock.patch.dict(os.environ, clean_env, clear=True),
                mock.patch("backend.irl_engine._repo_root", return_value=empty_repo),
                mock.patch("backend.irl_engine.DEFAULT_FALLBACK_CASES_DIR", empty_repo / "missing_cases"),
                mock.patch("pathlib.Path.cwd", return_value=empty_cwd),
                mock.patch("tempfile.gettempdir", return_value=isolated_tmp),
            ):
                available = list_available_cases()
                self.assertEqual(available, list(SUPPORTED_CASES))

                for cid in SUPPORTED_CASES:
                    data = load_case_data(cid)
                    self.assertTrue(
                        Path(data["case_dir"]).is_relative_to(Path(isolated_tmp) / "sherpas_canonical_cases_v1")
                    )
                    eng = IRLEngine(cid)
                    ne = NotificationEngine(cid)
                    self.assertEqual(len(ne.list_historical_shocks()), 11)
                    self.assertIsNotNone(eng.get_focus_mode_view(0)["focus_step"])

                mc_eng = IRLEngine("michael-carter")
                mc10 = mc_eng.advance_day(10)
                levers = {lv["key"]: lv for lv in mc10["inertia_cost"]["active_levers"]}
                self.assertEqual(levers["high_apr_card"]["annual_cost_usd"], 700.0)
                self.assertEqual(levers["401k_tax_delay"]["annual_cost_usd"], 1800.0)

                with self.assertRaises(FileNotFoundError):
                    load_case_data("non-existent-case")


class TestIRLEngineTimelineAndFocus(unittest.TestCase):
    def test_focus_mode_day_0_exposes_single_3min_step_for_all_cases(self) -> None:
        expected_day0 = {
            "michael-carter": ("step_0_pay_amex", "Michael"),
            "samantha-lewis": ("step_0_confirm_home_auto_policies", "Samantha"),
            "timothy-melanie-weah": ("step_0_melanie_schedule_card_payoff", "Owner B (Melanie)"),
            "daniel-emily-johnson": (
                "step_0_joint_halt_diversion_and_quote",
                "Conjunto 2/2 (Daniel & Emily)",
            ),
        }
        for case_id, (step_id, owner_label) in expected_day0.items():
            eng = create_irl_run(case_id)
            focus = eng.get_focus_mode_view(0)
            self.assertEqual(focus["mode"], "focus_mode")
            self.assertIsNotNone(focus["focus_step"])
            self.assertEqual(focus["focus_step"]["step_id"], step_id)
            self.assertEqual(focus["focus_step"]["owner_label"], owner_label)
            self.assertEqual(focus["focus_step"]["estimated_minutes"], 3)
            self.assertEqual(eng.focus_step(0)["focus_step"]["step_id"], step_id)

    def test_nodes_sequence_and_real_milestones(self) -> None:
        mc = IRLEngine("michael-carter")
        mc_days = [n["day"] for n in mc.get_timeline_view(0)["nodes"]]
        for req in (0, 3, 14, 30):
            self.assertIn(req, mc_days)
        mc_dates = {s.due_date.isoformat()[:7] for s in mc.steps if s.phase == "milestone"}
        self.assertIn("2027-01", mc_dates)
        self.assertIn("2047-04", mc_dates)
        self.assertIn("2075-01", mc_dates)

        sl = IRLEngine("samantha-lewis")
        sl_dates = {s.due_date.isoformat()[:7] for s in sl.steps if s.phase == "milestone"}
        self.assertIn("2027-08", sl_dates)  # Ethan college Aug 2027
        self.assertIn("2030-01", sl_dates)  # Home purchase 2030
        self.assertIn("2053-02", sl_dates)  # Liquid depletion age 74

    def test_bidirectional_navigation_preserves_progress(self) -> None:
        eng = IRLEngine("michael-carter")
        eng.check_step("step_0_pay_amex", completed_day=0)
        v30 = eng.advance_day(30)
        self.assertEqual(v30["current_day"], 30)
        self.assertTrue(v30["navigation"]["can_go_prev"])
        self.assertTrue(v30["navigation"]["can_go_next"])
        self.assertEqual(v30["navigation"]["prev_node_day"], 14)

        # Navigate backward to Day 3 without losing Day 0 check
        v3 = eng.get_timeline_view(3)
        self.assertEqual(v3["current_day"], 3)
        self.assertIn("step_0_pay_amex", [s["step_id"] for s in v3["completed_steps"]])
        self.assertEqual(v3["navigation"]["prev_node_day"], 0)
        self.assertEqual(v3["navigation"]["next_node_day"], 14)

    def test_mountain_overview_vs_repeat_expedition_separated(self) -> None:
        eng = IRLEngine("samantha-lewis")
        eng.check_step("step_0_confirm_home_auto_policies", completed_day=0)
        eng.advance_day(14)

        overview = eng.get_mountain_overview()
        self.assertEqual(overview["mode"], "mountain_overview")
        self.assertTrue(overview["irl_progress_preserved"])
        self.assertFalse(overview["expedition_reset"])
        self.assertEqual(overview["irl_completed_steps"], 1)
        self.assertEqual(overview["irl_current_day"], 14)
        self.assertEqual(overview["good_path"]["score_before"], 82)
        self.assertEqual(overview["good_path"]["score_after_optimal"], 84)
        self.assertTrue(
            any(
                b.get("year") == 2053 and b.get("investable_assets") == -227414
                for b in overview["failed_branches"]
            )
        )

        # Explicitly repeating the simulated expedition resets simulation, NOT IRL progress
        replay = eng.repeat_expedition()
        self.assertTrue(replay["expedition_reset"])
        self.assertFalse(replay["irl_reset"])
        self.assertEqual(replay["simulation_run_count"], 2)
        self.assertEqual(replay["irl_completed_steps"], 1)

        # Resetting with reset_irl=True resets both
        full_reset = eng.reset_expedition(reset_irl=True)
        self.assertTrue(full_reset["irl_reset"])
        self.assertEqual(full_reset["irl_completed_steps"], 0)
        self.assertEqual(full_reset["irl_current_day"], 0)

    def test_focus_mode_couples_by_owner_and_completion(self) -> None:
        eng = IRLEngine("timothy-melanie-weah")
        eng.advance_day(30)
        fm = eng.get_focus_mode_view()
        self.assertEqual(fm["by_owner"]["owner_a"]["label"], "Owner A (Timothy)")
        self.assertEqual(fm["by_owner"]["owner_b"]["label"], "Owner B (Melanie)")
        self.assertIsNotNone(fm["by_owner"]["owner_a"]["next_step"])
        self.assertIsNotNone(fm["by_owner"]["owner_b"]["next_step"])

        # Complete all due steps through Day 30
        for s in eng.steps:
            if s.day <= 30:
                for member in s.required_members:
                    eng.check_step(s.step_id, member=member)
        fm_done = eng.get_focus_mode_view(30)
        self.assertTrue(fm_done["all_due_steps_completed"])
        self.assertEqual(fm_done["pending_due_count"], 0)

        # Uncheck one half of a joint step reverts completion to 1/2
        reverted = eng.uncheck_step("step_3_joint_life_and_umbrella", member="B")
        self.assertFalse(reverted["is_completed"])
        self.assertEqual(reverted["completion_ratio"], "1/2")
        self.assertEqual(reverted["missing_members"], ["B"])


class TestCouplesAndInertiaCosts(unittest.TestCase):
    def test_weah_couple_assignment_joint_2_of_2_and_inertia(self) -> None:
        eng = IRLEngine("timothy-melanie-weah")
        self.assertTrue(eng.is_couple)

        # Wrong member on Owner B step raises ValueError
        with self.assertRaises(ValueError):
            eng.check_step("step_0_melanie_schedule_card_payoff", member="A")

        # Joint step requires explicit member A or B
        with self.assertRaises(ValueError):
            eng.check_step("step_3_joint_life_and_umbrella")

        # Only A checks joint step -> 1/2 incomplete
        half = eng.check_step("step_3_joint_life_and_umbrella", member="A")
        self.assertEqual(half["completion_ratio"], "1/2")
        self.assertFalse(half["is_completed"])
        self.assertEqual(half["missing_members"], ["B"])

        # Advance to Day 14: 1/2 step is still dragged as overdue, plus Melanie's unpaid card
        tl14 = eng.advance_day(14)
        overdue_ids = {s["step_id"] for s in tl14["overdue_steps"]}
        self.assertIn("step_3_joint_life_and_umbrella", overdue_ids)
        self.assertIn("step_3_melanie_confirm_card_paid", overdue_ids)

        levers = {lv["key"]: lv for lv in tl14["inertia_cost"]["active_levers"]}
        self.assertEqual(levers["high_apr_card"]["annual_cost_usd"], 3240.0)
        self.assertAlmostEqual(levers["high_apr_card"]["daily_cost_usd"], 8.88, places=2)
        self.assertEqual(levers["high_apr_card"]["cash_earned_annual_usd"], 150.0)
        self.assertEqual(levers["401k_tax_delay"]["annual_cost_usd"], 5760.0)

        # B completes second half -> 2/2 completed!
        done = eng.check_step("step_3_joint_life_and_umbrella", member="B")
        self.assertEqual(done["completion_ratio"], "2/2")
        self.assertTrue(done["is_completed"])
        self.assertEqual(done["missing_members"], [])

        # Melanie liquidates card on Day 3 -> stops high_apr_card bleed
        eng.check_step("step_3_melanie_confirm_card_paid", member="Melanie")
        after_cost = eng.compute_inertia_cost(14)
        after_keys = {lv["key"] for lv in after_cost["active_levers"]}
        self.assertNotIn("high_apr_card", after_keys)

    def test_johnson_couple_inertia_costs_and_uninsured_days(self) -> None:
        eng = IRLEngine("daniel-emily-johnson")
        tl10 = eng.advance_day(10)
        levers = {lv["key"]: lv for lv in tl10["inertia_cost"]["active_levers"]}

        self.assertEqual(levers["high_apr_card"]["annual_cost_usd"], 4482.0)
        self.assertAlmostEqual(levers["high_apr_card"]["daily_cost_usd"], 12.28, places=2)
        self.assertEqual(levers["401k_tax_delay"]["annual_cost_usd"], 11760.0)
        self.assertEqual(levers["life_protection_gap"]["shortfall_usd"], 2350000.0)
        self.assertEqual(tl10["inertia_cost"]["days_uninsured"], 10)

        # Binding life + umbrella (2/2) resolves days_uninsured
        eng.check_step("step_0_joint_halt_diversion_and_quote", member="Daniel")
        eng.check_step("step_0_joint_halt_diversion_and_quote", member="Emily")
        eng.check_step("step_3_joint_life_and_umbrella_quotes", member="A")
        eng.check_step("step_3_joint_life_and_umbrella_quotes", member="B")
        eng.check_step("step_14_joint_bind_life_umbrella", member="A")
        eng.check_step("step_14_joint_bind_life_umbrella", member="B")
        self.assertEqual(eng.compute_inertia_cost(14)["days_uninsured"], 0)

    def test_michael_and_samantha_inertia_costs(self) -> None:
        mc = IRLEngine("michael-carter")
        mc10 = mc.advance_day(10)
        mc_levers = {lv["key"]: lv for lv in mc10["inertia_cost"]["active_levers"]}
        self.assertEqual(mc_levers["high_apr_card"]["annual_cost_usd"], 700.0)
        self.assertAlmostEqual(mc_levers["high_apr_card"]["daily_cost_usd"], 1.92, places=2)
        self.assertEqual(mc_levers["401k_tax_delay"]["annual_cost_usd"], 1800.0)
        self.assertAlmostEqual(mc_levers["tax_drag"]["annual_cost_usd"], 526.93, places=2)

        # Completing Day 0 Amex payment removes card drag
        mc.check_step("step_0_pay_amex", completed_day=0)
        mc_after = mc.compute_inertia_cost(10)
        self.assertNotIn("high_apr_card", {lv["key"] for lv in mc_after["active_levers"]})

        sl = IRLEngine("samantha-lewis")
        sl10 = sl.advance_day(10)
        sl_levers = {lv["key"]: lv for lv in sl10["inertia_cost"]["active_levers"]}
        self.assertAlmostEqual(sl_levers["tax_drag"]["annual_cost_usd"], 3032.2, places=2)
        self.assertAlmostEqual(sl_levers["tax_drag"]["daily_cost_usd"], 8.31, places=2)
        self.assertEqual(sl_levers["hsa_tax_delay"]["annual_cost_usd"], 1408.0)
        self.assertEqual(sl_levers["401k_tax_delay"]["unused_room_usd"], 24500.0)
        self.assertEqual(sl10["inertia_cost"]["days_uninsured"], 10)
        self.assertIn(
            "Primary home ($900,000)",
            sl_levers["unconfirmed_property_policy"]["unconfirmed_assets"],
        )

    def test_ics_calendar_export(self) -> None:
        eng = IRLEngine("samantha-lewis", start_date=date(2026, 11, 1))
        ics = eng.export_ics()
        self.assertIn("BEGIN:VCALENDAR\r\n", ics)
        self.assertIn("END:VCALENDAR\r\n", ics)
        self.assertIn("DTSTART;VALUE=DATE:20261101", ics)  # Dia 0
        self.assertIn("DTSTART;VALUE=DATE:20261104", ics)  # Dia 3
        self.assertIn("DTSTART;VALUE=DATE:20261201", ics)  # Dia 30
        self.assertIn("DTSTART;VALUE=DATE:20270801", ics)  # Ethan college Aug 2027
        self.assertIn("DTSTART;VALUE=DATE:20300101", ics)  # Home purchase 2030


class TestNotificationsAndMacroShocks(unittest.TestCase):
    def test_type1_milestone_and_couple_missing_member_insistence(self) -> None:
        eng = IRLEngine("timothy-melanie-weah")
        ne = NotificationEngine("timothy-melanie-weah")

        # Day 0 milestone notification
        n0 = ne.generate_milestone_notifications(eng, current_day=0)
        self.assertTrue(any(n["kind"] == "milestone" and n["target_node_id"] == "day_0" for n in n0))

        # On Day 3 Timothy checks his half of joint insurance (1/2); Melanie doesn't
        eng.check_step("step_3_joint_life_and_umbrella", member="A", completed_day=3)
        eng.advance_day(14)
        n14 = ne.generate_milestone_notifications(eng)

        joint_nag = next(
            n for n in n14 if n["target_step_id"] == "step_3_joint_life_and_umbrella"
        )
        self.assertEqual(joint_nag["kind"], "overdue_insistence")
        self.assertEqual(joint_nag["completion_ratio"], "1/2")
        self.assertEqual(joint_nag["missing_members"], ["B"])
        self.assertEqual(joint_nag["target_owner"], "Owner B (Melanie)")
        self.assertIn("Owner B (Melanie)", joint_nag["message_plain"])

        card_nag = next(
            n for n in n14 if n["target_step_id"] == "step_3_melanie_confirm_card_paid"
        )
        self.assertGreater(card_nag["inertia_cost_accrued_usd"], 0)
        self.assertAlmostEqual(card_nag["daily_cost_usd"], 8.88, places=2)

    def test_type2_macro_shocks_all_11_events_and_case_specifics(self) -> None:
        # 1. Michael Carter: max 3Y drawdown -10.21% recovered in 62 days
        mc_ne = NotificationEngine("michael-carter")
        self.assertEqual(len(mc_ne.list_historical_shocks()), 11)
        mc_alert = mc_ne.generate_macro_shock_notification(
            alert_type="tariffs",
            headline="Aranceles y caida bursatil",
        )
        self.assertEqual(mc_alert["matched_event"]["date_label"], "2025-04-02")
        self.assertAlmostEqual(
            mc_alert["portfolio_vs_benchmark"]["household_drawdown_pct"], -0.0841, places=4
        )
        self.assertEqual(
            mc_alert["portfolio_vs_benchmark"]["household_max_drawdown_recovery_days"], 62
        )
        self.assertIn("62 dias", mc_alert["anti_panic_message_plain"])

        # 2. Timothy & Melanie Weah: UPRO 3x exposure warning + August 2024 VIX > 60
        weah_ne = NotificationEngine("timothy-melanie-weah")
        weah_alert = weah_ne.generate_macro_shock_notification(
            alert_type="volatility",
            headline="VIX por encima de 60 y selloff global",
        )
        self.assertEqual(weah_alert["matched_event"]["date_label"], "2024-08-05")
        self.assertIn("UPRO", weah_alert["anti_panic_message_plain"])
        self.assertTrue(
            any(a["code"] == "leveraged_etf_3x" for a in weah_alert["portfolio_exposure_alerts"])
        )

        # 3. Samantha Lewis: VTI 39% concentration + 78 recovery days
        sl_ne = NotificationEngine("samantha-lewis")
        sl_alert = sl_ne.generate_macro_shock_notification(
            alert_type="rates",
            headline="Subida de tipos de interes Fed",
        )
        self.assertEqual(sl_alert["matched_event"]["date_label"], "2023-07-26")
        self.assertEqual(
            sl_alert["portfolio_vs_benchmark"]["household_max_drawdown_recovery_days"], 78
        )
        self.assertTrue(
            any(
                a["code"] == "single_etf_concentration" and a["ticker"] == "VTI"
                for a in sl_alert["portfolio_exposure_alerts"]
            )
        )

        # 4. Daniel & Emily Johnson: 1.4 months liquidity cushion + 61 recovery days
        j_ne = NotificationEngine("daniel-emily-johnson")
        j_alert = j_ne.generate_macro_shock_notification(
            alert_type="geopolitical",
            headline="Crisis en Iran y subida del petroleo",
        )
        self.assertEqual(j_alert["matched_event"]["date_label"], "2026-02-28")
        self.assertEqual(j_alert["liquidity_cushion"]["months_covered"], "1.4")

        # 5. Tech/AI shock + explicit event lookup + upcoming milestone alerts
        ai_alert = j_ne.generate_macro_shock_notification(
            alert_type="tech_ai",
            headline="Selloff tecnologico DeepSeek",
        )
        self.assertEqual(ai_alert["matched_event"]["date_label"], "2025-01-27")

        explicit = mc_ne.generate_macro_shock_notification(event_name="Fed pivot")
        self.assertEqual(explicit["matched_event"]["date_label"], "2023-12-13")
        with self.assertRaises(KeyError):
            mc_ne.generate_macro_shock_notification(event_name="Evento inexistente")

        mc_eng = IRLEngine("michael-carter")
        upcoming_notifs = mc_ne.generate_milestone_notifications(mc_eng, current_day=30)
        self.assertTrue(
            any(n["kind"] == "upcoming_milestone" and "2027-01" in n["title"] for n in upcoming_notifs)
        )

    def test_no_backend_init_file_created(self) -> None:
        repo_root = Path(__file__).resolve().parent.parent
        self.assertFalse((repo_root / "backend" / "__init__.py").exists())


if __name__ == "__main__":
    unittest.main()
