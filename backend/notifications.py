"""Sistema de Notificaciones (Fase 5 / La Radio del Sherpa) para Sherpas.

Implementa los dos canales proactivos definidos en ``docs/IDEA_BITLIFE.md`` y
``docs/BIBLIA_FINAL_V1.md`` con 100% de datos reales de ``cases/<case_id>/``:

1. **Tipo 1 — Notificaciones de Hito e Insistencia IRL**:
   Se disparan en ``Dia 0``, ``Dia 3``, ``Dia 14``, ``Dia 30`` y fechas hito
   reales (``chartGoals`` / *Transition alerts*), y de forma recurrente por cada
   paso ``overdue`` mostrando el coste real de inercia acumulado hasta el dia
   actual y, en parejas, dirigiendo la alerta al miembro exacto (``Owner A`` u
   ``Owner B``) que falta por completar.

2. **Tipo 2 — Notificaciones de Gran Evento Economico IRL (Shocks Macro / Radio del Sherpa)**:
   Cruza alertas de mercado actuales (caida bursatil, tipos de interes,
   aranceles/inflacion, volatilidad VIX, tech/AI, geopolitica) con los
   **11 eventos historicos reales (2023-2026)** de ``investment-analysis.json``
   (``analysis.events`` y ``key_metrics.performanceAnalysis.perEventDrawdowns``),
   mostrando caida exacta de la cartera vs. benchmark, dias/fechas de
   recuperacion (ej. ``-10.2%`` en ``62 dias`` en Michael; exposicion ``3x`` en
   ``UPRO`` en Weah; ``39%`` en ``VTI`` en Samantha) y mensaje conductual
   anti-panico apoyado en el colchon de liquidez real.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from backend.irl_engine import IRLEngine, load_case_data


def _fmt_pct(ratio: float | None, *, signed: bool = True) -> str:
    if ratio is None:
        return "N/D"
    pct = ratio * 100.0
    if signed:
        return f"{pct:+.2f}%"
    return f"{pct:.2f}%"


def _fmt_usd(amount: float) -> str:
    sign = "-" if amount < 0 else ""
    val = abs(amount)
    if abs(val - round(val)) < 0.005:
        return f"{sign}${round(val):,.0f}"
    return f"{sign}${val:,.2f}"


# Keyword mapping for matching live market alerts against the 11 historical events (2023-2026).
_ALERT_SYNONYMS: dict[str, tuple[str, ...]] = {
    "equity_drop": (
        "caida", "bursatil", "bolsa", "selloff", "crash", "correction", "correccion",
        "drop", "equity", "equities", "vix", "tariff", "tariffs", "arancel", "aranceles",
        "market", "panic", "panico", "sp500", "s&p",
    ),
    "tariffs": (
        "tariff", "tariffs", "arancel", "aranceles", "liberation", "trade",
        "comercio", "china", "geneva", "supreme court", "inflacion", "inflation",
    ),
    "inflation": (
        "inflation", "inflacion", "tariff", "tariffs", "arancel", "aranceles",
        "cpi", "oil", "crude", "petroleo", "hike", "rates", "tipos",
    ),
    "rates": (
        "rate", "rates", "tipo", "tipos", "fed", "fomc", "hike", "cut",
        "subida", "recorte", "pivot", "dot plot", "treasury", "bonos",
    ),
    "volatility": (
        "volatility", "volatilidad", "vix", "selloff", "shock", "spike",
        "panico", "panic", "carry trade", "recession", "recesion",
    ),
    "tech_ai": (
        "tech", "ai", "ia", "deepseek", "nasdaq", "semiconductor", "nvidia",
        "tecnologia",
    ),
    "geopolitical": (
        "geopolitical", "geopolitica", "war", "guerra", "iran", "israel",
        "oil", "crude", "petroleo", "epic fury", "hormuz", "conflict",
    ),
}


def merge_historical_shocks(case_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Combine the 11 ``analysis.events`` with ``perEventDrawdowns`` for ``case_data``."""
    ia = case_data["investment_analysis"]
    events = ia.get("analysis", {}).get("events", [])
    drawdowns = ia.get("key_metrics", {}).get("performanceAnalysis", {}).get("perEventDrawdowns", [])

    dd_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for dd in drawdowns:
        dd_by_key[(str(dd.get("eventDate", "")), str(dd.get("eventTitle", "")))] = dd

    merged: list[dict[str, Any]] = []
    for idx, ev in enumerate(events):
        date_label = str(ev.get("dateLabel", ""))
        name = str(ev.get("name", ""))
        dd = dd_by_key.get((date_label, name))
        if dd is None and idx < len(drawdowns):
            dd = drawdowns[idx]
        dd = dd or {}

        hh = dd.get("household", {})
        bm = dd.get("sameRiskBenchmark", {})
        merged.append(
            {
                "index": idx,
                "name": name,
                "date_label": date_label,
                "start_date": ev.get("startDate") or dd.get("windowStart"),
                "end_date": ev.get("endDate") or dd.get("windowEnd"),
                "type": ev.get("type"),
                "severity": ev.get("severity") or dd.get("severity"),
                "duration": ev.get("duration"),
                "impact_direction": ev.get("impactDirection"),
                "portfolio_impact": ev.get("portfolioImpact"),
                "asset_classes_affected": list(ev.get("assetClassesAffected", [])),
                "description": ev.get("description", ""),
                "household_drawdown_pct": hh.get("drawdownPct"),
                "household_return_during_pct": hh.get("returnDuringPct"),
                "household_recovery_days": hh.get("recoveryDays"),
                "benchmark_drawdown_pct": bm.get("drawdownPct"),
                "benchmark_return_during_pct": bm.get("returnDuringPct"),
                "benchmark_recovery_days": bm.get("recoveryDays"),
                "divergence_pp": dd.get("divergencePp"),
            }
        )
    return merged


class NotificationEngine:
    """Generator for Type 1 (Milestone / Overdue) and Type 2 (Macro Shock) alerts."""

    def __init__(
        self,
        case_id: str,
        *,
        cases_dir: str | Path | None = None,
    ) -> None:
        self.case_id = case_id
        self.cases_dir = cases_dir
        self.case_data = load_case_data(case_id, cases_dir=cases_dir)
        self.historical_shocks = merge_historical_shocks(self.case_data)

    # ------------------------------------------------------------------
    # Tipo 1: Notificaciones de Hito / Insistencia IRL
    # ------------------------------------------------------------------
    def generate_milestone_notifications(
        self,
        engine: IRLEngine,
        current_day: int | None = None,
    ) -> list[dict[str, Any]]:
        """Build Type 1 milestone and recurring overdue notifications for ``engine``."""
        if engine.case_id != self.case_id:
            raise ValueError(
                f"IRLEngine pertenece a '{engine.case_id}', esperado '{self.case_id}'."
            )

        day = engine.current_day if current_day is None else int(current_day)
        timeline = engine.get_timeline_view(day)
        inertia = timeline["inertia_cost"]
        notifications: list[dict[str, Any]] = []

        # 1. Recurring insistence alerts for EVERY overdue step (or 1/2 incomplete couple step).
        for step in timeline["overdue_steps"]:
            step_inertia = step.get("inertia_cost", {})
            daily_cost = float(step_inertia.get("daily_cost_usd", 0.0))
            accrued_step = float(step_inertia.get("accrued_cost_usd", 0.0))
            days_overdue = int(step.get("days_overdue", 0))

            missing_labels = step.get("missing_member_labels", [])
            if engine.is_couple and missing_labels:
                target_owner = ", ".join(missing_labels)
                owner_notice = f"Falta confirmacion de {target_owner} ({step['completion_ratio']})."
            else:
                target_owner = step["owner_label"]
                owner_notice = f"Responsable: {target_owner}."

            cost_clause = (
                f"Coste acumulado de inercia: {_fmt_usd(accrued_step)} en {days_overdue} dias vencidos "
                f"({_fmt_usd(daily_cost)}/dia). Coste total acumulado del hogar desde Dia 0: "
                f"{_fmt_usd(inertia['accrued_since_day0_usd'])}."
                if daily_cost > 0
                else (
                    f"{days_overdue} dias vencidos sin completar "
                    f"(riesgo abierto: {step_inertia.get('label', step['title'])})."
                )
            )

            notifications.append(
                {
                    "notification_id": f"notif_overdue_{day}_{step['step_id']}",
                    "kind": "overdue_insistence",
                    "type": "milestone_insistence",
                    "day": day,
                    "due_day": step["day"],
                    "days_overdue": days_overdue,
                    "severity": "critical" if days_overdue >= 7 or daily_cost >= 5 else "warning",
                    "case_id": self.case_id,
                    "target_node_id": step["node_id"],
                    "target_step_id": step["step_id"],
                    "target_owner": target_owner,
                    "missing_members": step["missing_members"],
                    "completion_ratio": step["completion_ratio"],
                    "title": f"Recordatorio urgente (Dia {day}): sigue pendiente '{step['title']}'",
                    "message_plain": f"{owner_notice} {step['action_plain']} {cost_clause}",
                    "message_math": f"{owner_notice} {step['action_math']} | {cost_clause}",
                    "inertia_cost_accrued_usd": accrued_step,
                    "household_accrued_inertia_usd": inertia["accrued_since_day0_usd"],
                    "daily_cost_usd": daily_cost,
                    "days_uninsured": inertia["days_uninsured"],
                    "deep_link": f"irl://node/{step['node_id']}#step={step['step_id']}",
                }
            )

        # 2. Current-day milestone / checkpoint alerts (Dia 0, Dia 3, Dia 14, Dia 30, or exact milestone day).
        for step in timeline["active_steps"]:
            missing_labels = step.get("missing_member_labels", [])
            target_owner = ", ".join(missing_labels) if (engine.is_couple and missing_labels) else step["owner_label"]
            notifications.append(
                {
                    "notification_id": f"notif_milestone_{day}_{step['step_id']}",
                    "kind": "milestone",
                    "type": "milestone_insistence",
                    "day": day,
                    "due_day": step["day"],
                    "days_overdue": 0,
                    "severity": "info" if day == 0 else "warning",
                    "case_id": self.case_id,
                    "target_node_id": step["node_id"],
                    "target_step_id": step["step_id"],
                    "target_owner": target_owner,
                    "missing_members": step["missing_members"],
                    "completion_ratio": step["completion_ratio"],
                    "title": f"Hito Dia {day}: {step['title']}",
                    "message_plain": f"Para {target_owner}: {step['action_plain']}",
                    "message_math": f"Para {target_owner}: {step['action_math']}",
                    "inertia_cost_accrued_usd": inertia["accrued_since_day0_usd"],
                    "household_accrued_inertia_usd": inertia["accrued_since_day0_usd"],
                    "daily_cost_usd": inertia["daily_cost_usd"],
                    "days_uninsured": inertia["days_uninsured"],
                    "deep_link": f"irl://node/{step['node_id']}#step={step['step_id']}",
                }
            )

        # 3. Upcoming milestone preview within 30 days (or next key transition date).
        for step in timeline["upcoming_steps"]:
            days_until = step["day"] - day
            if step["phase"] == "milestone" and 0 < days_until <= 65:
                notifications.append(
                    {
                        "notification_id": f"notif_upcoming_{day}_{step['step_id']}",
                        "kind": "upcoming_milestone",
                        "type": "milestone_insistence",
                        "day": day,
                        "due_day": step["day"],
                        "days_until": days_until,
                        "severity": "info",
                        "case_id": self.case_id,
                        "target_node_id": step["node_id"],
                        "target_step_id": step["step_id"],
                        "target_owner": step["owner_label"],
                        "missing_members": step["missing_members"],
                        "completion_ratio": step["completion_ratio"],
                        "title": f"Proximo hito en {days_until} dias ({step['due_date']}): {step['title']}",
                        "message_plain": step["action_plain"],
                        "message_math": step["action_math"],
                        "inertia_cost_accrued_usd": inertia["accrued_since_day0_usd"],
                        "household_accrued_inertia_usd": inertia["accrued_since_day0_usd"],
                        "daily_cost_usd": inertia["daily_cost_usd"],
                        "days_uninsured": inertia["days_uninsured"],
                        "deep_link": f"irl://node/{step['node_id']}#step={step['step_id']}",
                    }
                )

        return notifications

    # ------------------------------------------------------------------
    # Tipo 2: Shocks Macro / La Radio del Sherpa
    # ------------------------------------------------------------------
    def list_historical_shocks(self) -> list[dict[str, Any]]:
        """Return all 11 historical events (2023-2026) merged with case drawdowns."""
        return list(self.historical_shocks)

    def match_macro_shock(
        self,
        *,
        alert_type: str | None = None,
        headline: str = "",
        market_drop_pct: float | None = None,
    ) -> dict[str, Any]:
        """Match a real-world market alert to the closest historical event among the 11 shocks."""
        tokens = set(re.findall(r"[a-z0-9]+", headline.lower()))
        if alert_type:
            norm_type = alert_type.strip().lower()
            tokens.update(_ALERT_SYNONYMS.get(norm_type, ()))
            tokens.add(norm_type)

        # If caller indicates a negative market drop without specific topic, bias toward risk-off drawdowns.
        prefer_negative = (market_drop_pct is not None and market_drop_pct < 0) or bool(
            tokens & {"caida", "bursatil", "bolsa", "selloff", "crash", "drop", "vix", "panico", "panic", "arancel", "aranceles", "tariff", "tariffs"}
        )

        best_score = -10_000.0
        best_event = self.historical_shocks[0]
        for ev in self.historical_shocks:
            haystack = " ".join(
                [
                    str(ev["name"]),
                    str(ev["type"]),
                    str(ev["description"]),
                    " ".join(ev["asset_classes_affected"]),
                ]
            ).lower()
            ev_tokens = set(re.findall(r"[a-z0-9]+", haystack))
            overlap = len(tokens & ev_tokens)
            score = overlap * 10.0

            # Domain-specific boosts for accurate matching across Spanish/English inputs
            ev_name_l = ev["name"].lower()
            if tokens & {"vix", "volatility", "volatilidad", "recession", "recesion"} and "vix" in ev_name_l:
                score += 25.0
            if tokens & {"tariff", "tariffs", "arancel", "aranceles", "inflation", "inflacion"} and "liberation day tariffs" in ev_name_l:
                score += 25.0
            if tokens & {"rate", "rates", "tipo", "tipos", "fed", "hike", "subida"} and "fed final hike" in ev_name_l:
                score += 22.0
            if tokens & {"cut", "recorte", "pivot"} and "fed" in ev_name_l:
                score += 18.0
            if tokens & {"deepseek", "ai", "ia", "tech", "tecnologia"} and "deepseek" in ev_name_l:
                score += 25.0
            if tokens & {"iran", "oil", "crude", "petroleo", "geopolitical", "geopolitica", "war", "guerra"} and "iran" in ev_name_l:
                score += 25.0

            dd_pct = float(ev.get("household_drawdown_pct") or 0.0)
            if prefer_negative:
                if ev.get("portfolio_impact") == "Negative" or ev.get("impact_direction") == "Risk-off equity":
                    score += 8.0
                score += abs(dd_pct) * 40.0
                if market_drop_pct is not None:
                    # Prefer drawdown magnitude close to the incoming drop
                    score -= abs(abs(market_drop_pct) - abs(dd_pct)) * 30.0

            if score > best_score:
                best_score = score
                best_event = ev

        return best_event

    def _portfolio_exposure_notes(self) -> list[dict[str, Any]]:
        """Extract real holding/concentration alerts relevant during a macro shock."""
        ia = self.case_data["investment_analysis"]
        fh = self.case_data["financial_health"]
        positions = ia.get("positions", [])
        perf_hh = ia.get("key_metrics", {}).get("performanceAnalysis", {}).get("household", {})
        aum = float(perf_hh.get("aum") or 0.0)
        notes: list[dict[str, Any]] = []

        # Leveraged ETF (e.g. UPRO 3x in Timothy Weah)
        for pos in positions:
            cat = str(pos.get("category", ""))
            ticker = str(pos.get("ticker", ""))
            if "leveraged" in cat.lower() or ticker == "UPRO":
                val = float(pos.get("value", 0))
                notes.append(
                    {
                        "code": "leveraged_etf_3x",
                        "ticker": ticker,
                        "account": pos.get("account"),
                        "value_usd": val,
                        "weight_in_account": pos.get("weight_in_account"),
                        "summary": (
                            f"Exposicion apalancada 3x en {ticker} ({_fmt_usd(val)} en {pos.get('account')}): "
                            "una caida bursatil se amplifica ~3x en esa posicion frente al perfil Moderate del hogar."
                        ),
                    }
                )

        # Single-ETF concentration (e.g. VTI 39% in Samantha Lewis)
        vti_total = sum(float(p.get("value", 0)) for p in positions if p.get("ticker") == "VTI")
        if vti_total > 0 and aum > 0:
            vti_share = vti_total / aum
            if vti_share >= 0.30:
                notes.append(
                    {
                        "code": "single_etf_concentration",
                        "ticker": "VTI",
                        "value_usd": vti_total,
                        "share_of_aum": round(vti_share, 4),
                        "summary": (
                            f"Concentracion en VTI: {_fmt_usd(vti_total)} ({vti_share * 100:.1f}% de cartera+caja "
                            f"de {_fmt_usd(aum)}); el plan sugiere reducirla hacia 25%."
                        ),
                    }
                )

        # Sector concentration (e.g. Technology >30%)
        sectors = ia.get("key_metrics", {}).get("concentrationAndDiversification", {}).get("sectorConcentration", [])
        for row in sectors[1:]:
            if isinstance(row, list) and len(row) >= 4 and row[0] == "Technology" and float(row[1]) >= 0.30:
                notes.append(
                    {
                        "code": "sector_concentration_tech",
                        "sector": "Technology",
                        "weight_pct": round(float(row[1]) * 100, 2),
                        "severity": row[3],
                        "summary": f"Sector Technology en {float(row[1]) * 100:.1f}% de renta variable ({row[3]}).",
                    }
                )

        # Short-term cash collision (e.g. Michael Carter Jan 2027 home down payment)
        facts_cash = fh.get("key_metrics", {}).get("facts", {}).get("cash", {})
        months_cov = facts_cash.get("monthsCovered", {}).get("value")
        months_after = facts_cash.get("monthsCoveredAfterNearTermGoals", {}).get("value")
        accessible_cash = facts_cash.get("accessibleCash", {}).get("value")
        notes.append(
            {
                "code": "liquidity_buffer",
                "accessible_cash_usd": accessible_cash,
                "months_covered": months_cov,
                "months_covered_after_goals": months_after,
                "summary": (
                    f"Colchon liquido actual: {_fmt_usd(float(accessible_cash or 0))} "
                    f"({months_cov} meses de gastos esenciales; {months_after} meses tras metas a corto plazo)."
                ),
            }
        )
        return notes

    def generate_macro_shock_notification(
        self,
        *,
        alert_type: str | None = None,
        headline: str = "Caida bursatil y pico de volatilidad",
        market_drop_pct: float | None = None,
        event_name: str | None = None,
    ) -> dict[str, Any]:
        """Create a Type 2 *Radio del Sherpa* alert crossing market news with the 11 real shocks."""
        if event_name:
            matched = next(
                (e for e in self.historical_shocks if event_name.lower() in e["name"].lower()),
                None,
            )
            if matched is None:
                raise KeyError(f"Evento historico no encontrado: '{event_name}'")
        else:
            matched = self.match_macro_shock(
                alert_type=alert_type,
                headline=headline,
                market_drop_pct=market_drop_pct,
            )

        ia = self.case_data["investment_analysis"]
        fh = self.case_data["financial_health"]
        perf_hh = ia.get("key_metrics", {}).get("performanceAnalysis", {}).get("household", {})
        perf_bm = ia.get("key_metrics", {}).get("performanceAnalysis", {}).get("sameRiskBenchmark", {})
        facts_cash = fh.get("key_metrics", {}).get("facts", {}).get("cash", {})

        max_dd_3y = perf_hh.get("maxDrawdown3y")
        max_rec_days = perf_hh.get("maxDrawdownRecoveryDays")
        accessible_cash = float(facts_cash.get("accessibleCash", {}).get("value") or 0.0)
        months_cov = str(facts_cash.get("monthsCovered", {}).get("value") or "0")

        ev_dd = matched.get("household_drawdown_pct")
        bm_dd = matched.get("benchmark_drawdown_pct")
        ev_ret = matched.get("household_return_during_pct")
        bm_ret = matched.get("benchmark_return_during_pct")
        ev_rec = matched.get("household_recovery_days")
        exposures = self._portfolio_exposure_notes()

        rec_phrase = (
            f"y se recupero en {ev_rec} dias en ese episodio (peor caida 3 anos: "
            f"{_fmt_pct(max_dd_3y)} recuperada en {max_rec_days} dias)"
            if ev_rec is not None
            else (
                f"y tu peor caida historica de los ultimos 3 anos ({_fmt_pct(max_dd_3y)}) "
                f"se recupero completamente en {max_rec_days} dias"
            )
        )

        special_caution = ""
        for exp in exposures:
            if exp["code"] in ("leveraged_etf_3x", "single_etf_concentration"):
                special_caution = f" Ojo puntual: {exp['summary']}"
                break

        plain_msg = (
            f"La Radio del Sherpa — Calma ante '{headline}': esto se parece a "
            f"'{matched['name']}' ({matched['date_label']}). Con tus mismos activos, "
            f"tu cartera cayo {_fmt_pct(ev_dd)} (vs {_fmt_pct(bm_dd)} del benchmark) "
            f"{rec_phrase}. Tu colchon de {_fmt_usd(accessible_cash)} ({months_cov} meses) "
            f"evita malvender en el suelo del mercado.{special_caution}"
        )
        math_msg = (
            f"analysis.events + perEventDrawdowns[{matched['index']}] ({matched['date_label']}..{matched['end_date']}): "
            f"household drawdown={_fmt_pct(ev_dd)}, returnDuring={_fmt_pct(ev_ret)} vs "
            f"sameRiskBenchmark drawdown={_fmt_pct(bm_dd)}, returnDuring={_fmt_pct(bm_ret)}, "
            f"divergence={_fmt_pct(matched.get('divergence_pp'))}; "
            f"3Y maxDrawdown={_fmt_pct(max_dd_3y)}, maxDrawdownRecoveryDays={max_rec_days}, "
            f"benchmark3YMaxDD={_fmt_pct(perf_bm.get('maxDrawdown3y'))}."
        )

        return {
            "notification_id": f"notif_macro_{self.case_id}_{matched['date_label']}",
            "kind": "macro_shock",
            "type": "macro_shock_radio",
            "case_id": self.case_id,
            "headline": headline,
            "alert_type": alert_type,
            "matched_event": matched,
            "portfolio_vs_benchmark": {
                "household_drawdown_pct": ev_dd,
                "benchmark_drawdown_pct": bm_dd,
                "household_return_during_pct": ev_ret,
                "benchmark_return_during_pct": bm_ret,
                "divergence_pp": matched.get("divergence_pp"),
                "event_recovery_days": ev_rec,
                "household_max_drawdown_3y_pct": max_dd_3y,
                "household_max_drawdown_recovery_days": max_rec_days,
                "benchmark_max_drawdown_3y_pct": perf_bm.get("maxDrawdown3y"),
            },
            "liquidity_cushion": {
                "accessible_cash_usd": accessible_cash,
                "months_covered": months_cov,
            },
            "portfolio_exposure_alerts": exposures,
            "anti_panic_message_plain": plain_msg,
            "anti_panic_message_math": math_msg,
            "historical_events_count": len(self.historical_shocks),
        }
