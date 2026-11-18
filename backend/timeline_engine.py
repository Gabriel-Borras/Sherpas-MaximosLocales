"""Verified case data and expedition state machine."""

from __future__ import annotations

import copy
import importlib
import json
import os
from pathlib import Path


CASE_IDS = (
    "michael-carter",
    "samantha-lewis",
    "timothy-melanie-weah",
    "daniel-emily-johnson",
)
PILLAR_NAMES = (
    "Savings & cash flow",
    "Debt",
    "Investments",
    "Liquidity",
    "Protection",
)
PILLAR_MAXIMA = (25, 10, 25, 20, 20)


def _validate_mode(mode):
    """Return a supported display mode or raise ValueError."""
    if mode not in ("plain", "math"):
        raise ValueError("mode debe ser plain o math")
    return mode


def _pillars(scores):
    """Return pillar records without filling unpublished scores."""
    return [
        {"name": name, "score": score, "max_score": maximum}
        for name, score, maximum in zip(PILLAR_NAMES, scores, PILLAR_MAXIMA)
    ]


def _option(option_id, label, from_score, to_score, **details):
    """Create a camp decision using verified score deltas."""
    return {
        "id": option_id,
        "label": label,
        "from_score": from_score,
        "to_score": to_score,
        **details,
    }


def _camp(camp_id, year, age, kind, options, **details):
    """Create a camp record."""
    return {
        "id": camp_id,
        "year": year,
        "age": age,
        "kind": kind,
        "options": options,
        **details,
    }


SEED_CASES = {
    "michael-carter": {
        "id": "michael-carter",
        "name": "Michael Carter",
        "age": 37,
        "d5_mode": "SINGLE",
        "location": "Austin, TX",
        "income": 180000,
        "savings_per_year": 43000,
        "savings_rate_pct": 23.9,
        "goal": "Retire at 58",
        "score": {
            "value": 26,
            "status": "critical",
            "pillars": _pillars((0, 8, 11, 4, 4)),
            "top_moves": [
                _option("umbrella", "Add $1M umbrella cover", 26, 31),
                _option("growth", "Increase growth allocation", 26, 31,
                        before_pct=74, after_pct=88, impact_approx=19900),
                _option("keep_inertia", "Keep current course", 26, 26,
                        fails=True),
                _option("cut_withdrawals", "Cut withdrawals to $10,300/yr",
                        26, 62),
            ],
            "combined_moves": [],
        },
        "fears": [
            {"id": "O1", "label": "Retirement shortfall"},
            {"id": "O2", "label": "Cash for the home purchase"},
            {"id": "O3", "label": "Life insurance gap: $720,000"},
            {"id": "O4", "label": "No umbrella cover"},
        ],
        "step_1": (
            "Liquidar Amex de $3,500 al 20% APR con el efectivo del banco."
        ),
        "reframing": {
            "plain": (
                "Ahorra el 23.9% ($43,000/yr) y tiene una ruta viable de "
                "26 a 62."
            ),
            "math": "Savings rate: 23.9%; verified route: score 26 to 62.",
        },
        "yearly": [
            {"year": 2026, "age": 37, "investable_assets": 178717},
            {"year": 2027, "age": 38, "investable_assets": 81172},
            {"year": 2032, "age": 43, "investable_assets": 279056},
            {"year": 2038, "age": 49, "investable_assets": 763133},
            {"year": 2044, "age": 55, "investable_assets": 1550861},
            {"year": 2050, "age": 61, "investable_assets": 1823675},
            {"year": 2056, "age": 67, "investable_assets": 1125478},
            {"year": 2062, "age": 73, "investable_assets": 717522},
            {"year": 2068, "age": 79, "investable_assets": 316843},
            {"year": 2074, "age": 85, "investable_assets": 3288},
            {"year": 2075, "age": 86, "investable_assets": -38276,
             "net_worth": 2570000},
            {"year": 2080, "age": 91, "investable_assets": -160752},
        ],
        "camps": [
            _camp("camp_2026", 2026, 37, "decision", [
                _option("umbrella", "Add $1M umbrella", 26, 31),
                _option("growth", "Increase growth 74% to 88%", 26, 31),
                _option("keep_inertia", "Keep current course", 26, 26,
                        fails=True),
            ]),
            _camp("camp_2027_home", 2027, 38, "transition_event", [
                _option("buy_as_planned", "Buy home as planned", None, None),
                _option("ask_advisor_delay", "Ask advisor about delaying",
                        None, None, advisor=True),
            ], has_counterfactual=False, event={
                "home_price": 550000,
                "month": "January",
                "investable_assets_before": 178717,
                "investable_assets_after": 81172,
                "cash_months": 0,
                "down_payment": 113300,
                "mortgage_monthly": 3015,
                "rent_monthly": 2800,
                "property_tax_yearly": 5665,
                "insurance_yearly": 2832.5,
                "closing_costs": 9464,
            }),
            _camp("camp_2047_retire", 2047, 58, "decision", [
                _option("cut_withdrawals", "Cut withdrawals to $10,300/yr",
                        26, 62, draw_pct=1.0),
                _option("keep_draw", "Keep 5.6% draw", 26, 26,
                        fails=True, draw_pct=5.6),
            ], withdrawal_yearly=59613, draw_pct=5.6,
               retirement_gap=1177586),
        ],
        "block": {
            "type": "crevasse", "year": 2075, "age": 86,
            "investable_assets": -38276, "net_worth": 2570000,
            "tensions": ["T1", "O1", "O2"],
            "behavioral_biases": ["Ilusion Inmobiliaria",
                                  "Descuento Hiperbolico", "Efecto Avestruz"],
            "facts": {
                "amex_balance": 3500, "amex_apr_pct": 20,
                "bank_balance": 27000, "401k_increase": 7500,
                "tax_savings_yearly": 1800, "jnk_tax_drag_yearly": 527,
                "shock_pct": -10.2, "recovery_days": 62,
            },
            "diagnostic_question": (
                "¿Qué prioridad pesa más que tu liquidez futura?"
            ),
        },
        "metrics": {"cash_balance": 27000, "amex_balance": 3500},
        "dual": False,
    },
    "samantha-lewis": {
        "id": "samantha-lewis", "name": "Samantha Lewis", "age": 47,
        "d5_mode": "SINGLE",
        "children": [{"age": 18}, {"age": 16}],
        "score": {
            "value": 82, "status": "strong",
            "pillars": _pillars((None, None, None, None, None)),
            "top_moves": [
                _option("home_insurance", "Review home insurance", 82, 84),
                _option("reduce_vti", "Reduce VTI from 39% to 25%", 82, 83),
                _option(
                    "adjust_growth", "Adjust growth from 85% to 80%", 82, 83
                ),
                _option("keep_inertia", "Keep current course", 82, 82,
                        fails=True),
            ], "combined_moves": [],
        },
        "fears": [
            {"id": "O1", "label": "Retirement: $0 in 2053"},
            {"id": "O2", "label": "University: $100,000"},
            {"id": "O3", "label": "Home purchase: $500,000 in 2030"},
            {"id": "O4", "label": "VTI 39% and home/Porsche insurance"},
        ],
        "reframing": {
            "plain": (
                "Su patrimonio es $1,390,000; el plan debe iniciar su "
                "ahorro jubilatorio."
            ),
            "math": "Score 82; retirement accounts $0; VTI 39%; growth 85%.",
        },
        "step_1": "Confirmar las pólizas de hogar y del Porsche Cayenne.",
        "facts": {"retirement_accounts": 0, "home_equity": 900000,
                  "net_worth": 1390000, "tax_drag_yearly": 3032,
                  "vti_pct": 39, "growth_pct": 85,
                  "401k_headroom": 24500, "hsa_headroom": 4400},
        "yearly": [
            {"year": 2026, "age": 47, "net_worth": 1390000,
             "home_equity": 900000, "retirement_accounts": 0},
            {"year": 2053, "age": 74, "investable_assets": -227414},
            {"year": 2070, "age": 91, "net_worth_negative": True},
        ],
        "camps": [
            _camp("camp_2026_shield", 2026, 47, "decision", [
                _option("home_insurance", "Review home insurance", 82, 84),
                _option("reduce_vti", "Reduce VTI concentration", 82, 83),
                _option("adjust_growth", "Adjust growth allocation", 82, 83),
                _option("keep_inertia", "Keep current course", 82, 82,
                        fails=True),
            ]),
            _camp("camp_2027_2030_transitions", 2030, 51,
                  "transition_event", [
                _option("proceed_as_planned", "Proceed as planned", None,
                        None),
                _option("ask_advisor_plan", "Ask advisor to plan", None,
                        None, advisor=True),
            ], has_counterfactual=False, event={
                "university_per_child": 50000,
                "university_total": 100000,
                "home_price": 500000,
            }),
        ],
        "block": {
            "type": "crevasse", "year": 2053, "age": 74,
            "investable_assets": -227414, "net_worth_negative_year": 2070,
            "tensions": ["O1", "O2", "O3"],
            "behavioral_biases": ["Efecto Halo", "Ilusion Inmobiliaria",
                                  "Mascarilla de Oxigeno"],
            "diagnostic_question": (
                "¿Cómo protegerás tu jubilación junto a los planes familiares?"
            ),
        },
        "dual": False,
    },
    "timothy-melanie-weah": {
        "id": "timothy-melanie-weah", "name": "Timothy & Melanie Weah",
        "age": 40, "d5_mode": "DUAL", "d4_status": "MISALIGNED",
        "d6_anchor": (
            "Proteger a sus 2 hijos (6 y 3 anos) y asegurar el futuro familiar"
        ),
        "partners": [
            {"name": "Timothy", "age": 40, "risk": "Growth 4",
             "holding": "UPRO 3x", "color": "#2563EB"},
            {"name": "Melanie", "age": 38, "risk": "Moderate 3",
             "cash": 150800, "cash_apy_pct": 0.09, "color": "#0D9488"},
        ],
        "children": [{"age": 6}, {"age": 3}],
        "score": {"value": 60, "status": "vulnerable",
                  "pillars": _pillars((None, None, None, None, None)),
                  "top_moves": [
                      _option("pay_card_18k", "Pay $18,000 card", 60, 62,
                              owner="Melanie"),
                      _option("shield_life_umbrella", "Add family shields", 60,
                              78, combined=True),
                      _option(
                          "rebalance_upro_401k", "Rebalance UPRO and 401(k)",
                          60, 78, combined=True, owner="Timothy"
                      ),
                      _option("keep_inertia", "Keep current course", 60, 60,
                              fails=True),
                  ],
                  "combined_moves": [{"from_score": 60, "to_score": 78}],
                  "combined_target_score": 78},
        "combined_target_score": 78,
        "fears": [
            {"id": "O1", "label": "Proteger el futuro de sus hijos"},
            {"id": "O2", "label": "Tarjeta de $18,000 al 18% APR"},
            {"id": "O3", "label": "Riesgo de UPRO apalancado 3x"},
            {"id": "O4", "label": "Acordar Growth y Moderate en pareja"},
        ],
        "reframing": {
            "plain": (
                "Tienen $150,800 en efectivo y una ruta conjunta de 60 a 78."
            ),
            "math": (
                "Score 60; combined_moves 60 to 78; card APR 18%; UPRO 3x."
            ),
        },
        "step_1": (
            "Liquidar los $18,000 de tarjeta al 18% APR con efectivo "
            "excedente."
        ),
        "facts": {"card_balance": 18000, "card_apr_pct": 18,
                  "annual_interest_burn": 3240, "cash_balance": 150800,
                  "cash_apy_pct": 0.09, "cash_yield_approx": 135,
                  "net_cash_drag": 3105, "free_cashflow_yearly": 15032,
                  "leveraged_etf": "UPRO",
                  "leverage_multiplier": 3, "401k_tax_savings_yearly": 5760},
        "yearly": [{"year": 2026, "cash": 150800, "card_debt": 18000},
                   {"year": 2079, "investable_assets": 16100000}],
        "camps": [_camp("camp_2026_cordada", 2026, 40, "decision", [
            _option("pay_card_18k", "Pay $18,000 card at 18% APR", 60, 62,
                    owner="Melanie"),
            _option("shield_life_umbrella", "Add $1.1M life and $1M umbrella",
                    60, 78, combined=True),
            _option("rebalance_upro_401k", "Reduce UPRO, add 401(k) and 529",
                    60, 78, combined=True, owner="Timothy"),
            _option("keep_inertia", "Keep current course", 60, 60,
                    fails=True),
        ], supports_combined=True, combined_to_score=78)],
        "block": {
            "type": "wall", "year": 2026, "annual_interest_burn": 3240,
            "card_balance": 18000, "card_apr_pct": 18.0,
            "cash_balance": 150800, "cash_apy_pct": 0.09,
            "cash_yield_approx": 135, "net_cash_drag": 3105,
            "leveraged_etf": "UPRO", "leverage_multiplier": 3,
            "yearly_terminal_2079": 16100000, "score_stagnant": 60,
            "score_potential": 78, "tensions": ["T1", "D4"],
            "behavioral_biases": ["Contabilidad Mental",
                                  "Aversion a la Perdida y Sesgo de Recencia",
                                  "Veto Silencioso"],
            "diagnostic_question": (
                "¿Cómo acordar prioridades entre deuda y riesgo?"
            ),
        },
        "dual": True,
    },
    "daniel-emily-johnson": {
        "id": "daniel-emily-johnson", "name": "Daniel & Emily Johnson",
        "age": 44, "d5_mode": "DUAL", "d4_status": "MISALIGNED",
        "d6_anchor": (
            "Proteger a Oliver (11) y Sophia (9) y blindar su hogar ($750,000)"
        ),
        "partners": [
            {"name": "Daniel", "age": 44, "risk": "Growth 4",
             "card_balance": 18000, "card_apr_pct": 24.9,
             "color": "#2563EB"},
            {"name": "Emily", "age": 42, "risk": "Moderate 3",
             "annual_savings": 26000, "annual_529": 8000,
             "annual_401k": 0, "color": "#0D9488"},
        ],
        "children": [{"name": "Oliver", "age": 11},
                     {"name": "Sophia", "age": 9}],
        "score": {"value": 52, "status": "vulnerable",
                  "pillars": _pillars((None, None, None, None, 0)),
                  "top_moves": [
                      _option("life_insurance", "Add $1.166M life cover", 52,
                              57),
                      _option("umbrella", "Add $1M umbrella", 52, 56),
                      _option("redirect_cashflow", "Redirect $15,032 yearly",
                              52, 55),
                      _option("keep_inertia", "Keep current course", 52, 52,
                              fails=True),
                  ],
                  "combined_moves": [{"from_score": 52, "to_score": 60}],
                  "combined_target_score": 60},
        "combined_target_score": 60,
        "fears": [
            {"id": "O1", "label": "Proteger a Oliver y Sophia"},
            {"id": "O2", "label": "Brecha de seguro de vida de $2.35M"},
            {"id": "O3", "label": "Tarjeta de $18,000 al 24.9% APR"},
            {"id": "O4", "label": "Solo 1.4 meses de efectivo"},
        ],
        "reframing": {
            "plain": (
                "Ahorran $26,000 al año y pueden fortalecer la protección "
                "familiar."
            ),
            "math": "Score 52; protection 0/20; combined_moves 52 to 60.",
        },
        "step_1": (
            "Solicitar cotización de vida y redirigir flujo para la tarjeta "
            "al 24.9%."
        ),
        "facts": {"cash_months": 1.4, "home_value": 750000,
                  "home_equity": 190000, "card_balance": 18000,
                  "card_apr_pct": 24.9, "annual_savings": 26000,
                  "free_cashflow_yearly": 15032,
                  "annual_529": 8000, "annual_401k": 0,
                  "foregone_tax_savings": 11760,
                  "life_insurance_gap": -2350000},
        "yearly": [{"year": 2026, "cash_months": 1.4,
                    "home_value": 750000, "home_equity": 190000,
                    "card_debt": 18000, "card_apr": 24.9,
                    "contribution_401k": 0, "contribution_529": 8000,
                    "annual_savings": 26000, "life_gap": -2350000}],
        "camps": [_camp("camp_2026_shield", 2026, 44, "decision", [
            _option("life_insurance", "Add $1.166M life cover", 52, 57),
            _option("umbrella", "Add $1M umbrella", 52, 56),
            _option("redirect_cashflow", "Redirect $15,032 and fund 401(k)",
                    52, 55),
            _option("keep_inertia", "Keep current course", 52, 52,
                    fails=True),
        ], supports_combined=True, combined_to_score=60)],
        "block": {
            "type": "wall", "year": 2026, "life_insurance_gap": -2350000,
            "protection_score": 0, "protection_max": 20,
            "card_balance": 18000, "card_apr_pct": 24.9,
            "annual_savings": 26000, "annual_529": 8000,
            "annual_401k": 0, "foregone_tax_savings": 11760,
            "cash_months": 1.4, "home_value": 750000, "home_equity": 190000,
            "score_stagnant": 52, "score_potential": 60,
            "tensions": ["T1", "T5", "D4"],
            "behavioral_biases": ["Sesgo de Optimismo e Invulnerabilidad",
                                  "Contabilidad Mental",
                                  "Priorizacion Emocional Invertida "
                                  "(Mascarilla de Oxigeno)",
                                  "Veto Silencioso y Silos en Pareja"],
            "diagnostic_question": (
                "¿Cómo proteger a Emily y a los hijos ante un imprevisto?"
            ),
        },
        "dual": True,
    },
}


class PhaseOrderError(Exception):
    """Raised when an expedition action occurs in the wrong phase."""


class ActionBlockedError(Exception):
    """Raised when an action is attempted before rewinding a failure."""


def _parse_json_file(path):
    """Read a JSON document from disk."""
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _normalize_yearly_rows(yearly):
    """Fill the canonical age field from age_client when it is missing."""
    rows = copy.deepcopy(yearly)
    if not isinstance(rows, list):
        return rows
    for row in rows:
        if (isinstance(row, dict) and "age_client" in row and
                row.get("age") is None):
            row["age"] = row["age_client"]
    return rows


def _normalize_loaded_case(case_id, raw, source):
    """Normalize Sherpas JSON while preserving all published source fields."""
    if not isinstance(raw, dict):
        return {"id": case_id, "raw": raw, "data_source": source}
    result = copy.deepcopy(raw)
    seed = SEED_CASES[case_id]
    base_score = seed.get("score", {})
    financial = (result.get("financial_health") or
                 result.get("financial-health"))
    investment = (result.get("investment_analysis") or
                  result.get("investment-analysis"))
    persona = result.get("persona")
    if isinstance(financial, dict):
        score = financial.get("score", {})
        if isinstance(score, dict):
            normalized_score = {**result.get("score", {}), **score}
            score_value = None
            for key in (
                    "value", "overall", "published_score", "publishedScore"):
                candidate = score.get(key)
                if candidate is not None:
                    score_value = candidate
                    break
            if score_value is None:
                score_value = base_score.get("value")
            normalized_score["value"] = score_value
            normalized_score["status"] = (
                score.get("status") or score.get("band") or
                base_score.get("status")
            )
            normalized_pillars = []
            canonical_names = {
                "Savings and cash flow": "Savings & cash flow",
                "Liquidity and emergency fund": "Liquidity",
                "Insurance and protection": "Protection",
            }
            for pillar in score.get("pillars", []):
                if not isinstance(pillar, dict):
                    normalized_pillars.append(copy.deepcopy(pillar))
                    continue
                normalized_pillar = copy.deepcopy(pillar)
                pillar_name = (pillar.get("name") or
                               pillar.get("pillar"))
                if pillar_name is not None:
                    normalized_pillar["name"] = canonical_names.get(
                        pillar_name, pillar_name
                    )
                points = pillar.get("points_shown_in_app")
                earned = maximum = None
                if isinstance(points, str) and "/" in points:
                    earned_text, maximum_text = points.split("/", 1)
                    try:
                        earned = int(earned_text.strip())
                    except ValueError:
                        pass
                    try:
                        maximum = int(maximum_text.strip())
                    except ValueError:
                        pass
                max_score = pillar.get("max_score")
                if max_score is None:
                    max_score = pillar.get("max")
                if max_score is None and maximum is not None:
                    max_score = maximum
                normalized_pillar["max_score"] = max_score
                if case_id == "michael-carter" and maximum is not None:
                    normalized_pillar["score"] = earned
                    normalized_pillar["max_score"] = maximum
                normalized_pillars.append(normalized_pillar)
            if "pillars" in score:
                normalized_score["pillars"] = normalized_pillars
            result["score"] = normalized_score
        source_keys = (
            "projections", "yearly", "analysis", "key_metrics", "metrics"
        )
        for key in source_keys:
            if key in financial:
                value = copy.deepcopy(financial[key])
                if key == "yearly":
                    value = _normalize_yearly_rows(value)
                elif key == "projections" and isinstance(value, dict):
                    if "yearly" in value:
                        value["yearly"] = _normalize_yearly_rows(
                            value["yearly"]
                        )
                result[key] = value
        projections = financial.get("projections", {})
        if isinstance(projections, dict) and "yearly" in projections:
            result["yearly"] = _normalize_yearly_rows(
                projections["yearly"]
            )
    if isinstance(investment, dict):
        analysis = investment.get("analysis", {})
        if isinstance(analysis, dict) and "events" in analysis:
            result["events"] = copy.deepcopy(analysis["events"])
        result["investment_analysis"] = copy.deepcopy(investment)
    if isinstance(persona, str):
        result["persona_text"] = persona
        result["subjective_concerns"] = _extract_persona_concerns(persona)
    result.setdefault("id", case_id)
    result["data_source"] = source
    normalized_score = result.get("score")
    if not isinstance(normalized_score, dict):
        normalized_score = {}
    for key in (
        "status", "top_moves", "combined_moves", "combined_target_score"
    ):
        if key not in normalized_score and key in base_score:
            normalized_score[key] = copy.deepcopy(base_score[key])
    result["score"] = normalized_score
    if "combined_target_score" not in result:
        if "combined_target_score" in normalized_score:
            result["combined_target_score"] = copy.deepcopy(
                normalized_score["combined_target_score"]
            )
        elif "combined_target_score" in seed:
            result["combined_target_score"] = copy.deepcopy(
                seed["combined_target_score"]
            )
    if source in ("cases_dir", "backend.mcp_client", "case_provider"):
        source_pillars = normalized_score.get("pillars") or []
        if not isinstance(source_pillars, list):
            source_pillars = []
        base_pillars = base_score.get("pillars", [])
        if case_id in SEED_CASES and len(source_pillars) < len(base_pillars):
            published_by_name = {
                pillar.get("name"): pillar
                for pillar in source_pillars
                if isinstance(pillar, dict) and pillar.get("name")
            }
            filled_pillars = []
            for base_pillar in base_pillars:
                pillar = copy.deepcopy(base_pillar)
                published = published_by_name.get(base_pillar["name"])
                if published is not None:
                    pillar.update(copy.deepcopy(published))
                    if "score" not in published:
                        pillar["score"] = base_pillar.get("score")
                    max_score = published.get(
                        "max_score", published.get("max")
                    )
                    if max_score is not None:
                        pillar["max_score"] = max_score
                filled_pillars.append(pillar)
            normalized_score["pillars"] = filled_pillars
    structural_fields = ("camps", "block", "dual", "partners", "d6_anchor")
    if any(key not in result for key in structural_fields):
        for key in structural_fields:
            result.setdefault(key, copy.deepcopy(seed.get(key)))
    if "financial_health" in result or "financial-health" in result:
        for key in ("name", "age", "fears", "reframing", "step_1", "facts"):
            if key not in result and key in seed:
                result[key] = copy.deepcopy(seed[key])
    return result


def _extract_persona_concerns(persona):
    """Extract concern and tension sections from persona markdown."""
    lines = persona.splitlines()
    found = []
    collecting = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            collecting = any(term in stripped.lower() for term in
                             ("concern", "tension", "transition", "alert"))
        if collecting and stripped:
            found.append(stripped)
    return found


class TimelineEngine:
    """Load verified cases and create plain or mathematical overviews."""

    def __init__(self, custom_cases=None, case_provider=None, cases_dir=None,
                 mode="plain"):
        self.custom_cases = custom_cases or {}
        self.case_provider = case_provider
        configured_dir = (
            cases_dir or os.environ.get("SHERPAS_CASES_DIR") or
            os.environ.get("CASES_DIR") or "cases"
        )
        self.cases_dir = Path(configured_dir)
        self.mode = _validate_mode(mode)

    def _load_external(self, case_id):
        """Resolve a case following the configured source priority."""
        if case_id in self.custom_cases:
            return self.custom_cases[case_id], "custom_cases"
        if self.case_provider:
            provider = self.case_provider
            if callable(provider):
                value = provider(case_id)
            else:
                value = provider.get_case(case_id)
            if value is not None:
                return value, "case_provider"
        case_path = self.cases_dir / case_id
        if case_path.is_dir():
            data = {"id": case_id}
            filenames = (
                ("financial-health.json", "financial_health"),
                ("investment-analysis.json", "investment_analysis"),
                ("persona.md", "persona"),
            )
            present = False
            for filename, key in filenames:
                path = case_path / filename
                if path.exists():
                    present = True
                    if path.suffix == ".md":
                        data[key] = path.read_text(encoding="utf-8-sig")
                    else:
                        data[key] = _parse_json_file(path)
            if present:
                return data, "cases_dir"
        try:
            client = importlib.import_module("backend.mcp_client")
            if hasattr(client, "get_case"):
                value = client.get_case(case_id)
            elif hasattr(client, "load_case"):
                value = client.load_case(case_id)
            else:
                value = None
            if value is not None:
                return value, "backend.mcp_client"
        except (ImportError, AttributeError, TypeError, ValueError):
            pass
        return copy.deepcopy(SEED_CASES[case_id]), "verified_biblia_seed"

    def load_case(self, case_id):
        """Load one case from the highest priority available source."""
        if case_id not in CASE_IDS:
            raise KeyError(case_id)
        raw, source = self._load_external(case_id)
        return _normalize_loaded_case(case_id, raw, source)

    def list_cases(self):
        """Return all supported cases in stable order."""
        return [self.load_case(case_id) for case_id in CASE_IDS]

    def overview(self, case_id, mode=None):
        """Return a case overview with the requested display mode."""
        case = self.load_case(case_id)
        selected_mode = _validate_mode(
            self.mode if mode is None else mode
        )
        score = case.get("score", {})
        default_text = (
            f"{case.get('name', case_id)}: {score.get('value')} "
            f"({score.get('status')})."
        )
        plain = case.get("reframing", {}).get("plain", default_text)
        math_text = json.dumps(
            {"score": score, "facts": case.get("facts", case.get("metrics")),
             "yearly": case.get("yearly")}, ensure_ascii=False, default=str)
        case["mode"] = selected_mode
        case["views"] = {"plain": plain, "math": math_text}
        case["display_text"] = case["views"][selected_mode]
        return case


class Expedition:
    """Track quest, blind partner votes, mountain decisions, and rewind."""

    def __init__(self, case, mode="plain"):
        self.case = copy.deepcopy(case)
        self.mode = _validate_mode(mode)
        self.phase = "quest"
        self.quest = None
        self.votes = {}
        self.blocked = False
        self.block_type = None
        self.failed_branches = []
        self.decisions = []
        self.uncalculated_questions = []
        self.camp_index = 0
        self.completed = False
        self.mountain_preload = None
        self.cordada_resolution = None
        self.current_score = self.case.get("score", {}).get("value")

    def _require_mountain(self):
        """Require the mountain phase and an unblocked route."""
        if self.phase != "mountain":
            raise PhaseOrderError(
                "Completa Quest y Cordada antes de entrar a la Montaña."
            )
        if self.blocked:
            raise ActionBlockedError(
                "La expedición está bloqueada; ejecuta rewind()."
            )

    def submit_quest(self, ranked_concerns, subjective_concern=""):
        """Record concerns and advance to Cordada or the mountain."""
        if self.phase != "quest":
            raise PhaseOrderError("Quest ya fue completada.")
        self.quest = {"ranked_concerns": ranked_concerns,
                      "subjective_concern": subjective_concern}
        self.phase = "cordada" if self.case.get("dual") else "mountain"
        return self.state()

    def _partner_key(self, partner):
        """Normalize a partner label to its A/B identity."""
        partners = self.case.get("partners", [])
        if partner in ("A", "B"):
            return partner
        for index, person in enumerate(partners[:2]):
            if person.get("name", "").lower() == str(partner).lower():
                return "A" if index == 0 else "B"
        raise ValueError(f"Titular desconocido: {partner}")

    def submit_vote(self, partner, **vote):
        """Record a private vote and reveal the match after both votes."""
        if self.phase != "cordada":
            raise PhaseOrderError(
                "Cordada ocurre después de Quest y antes de la Montaña."
            )
        key = self._partner_key(partner)
        self.votes[key] = copy.deepcopy(vote)
        if len(self.votes) < 2:
            return {"blind_pending": True, "partner_visible": False,
                    "votes_submitted": [key], "phase": "cordada"}
        partners = self.case.get("partners", [])
        choices_a = self.votes["A"].get(
            "choices", self.votes["A"].get("camp_choices", [])
        )
        choices_b = self.votes["B"].get(
            "choices", self.votes["B"].get("camp_choices", [])
        )
        if isinstance(choices_a, str):
            choices_a = [choices_a]
        if isinstance(choices_b, str):
            choices_b = [choices_b]
        camps = self.case.get("camps", [])
        options = camps[0].get("options", []) if camps else []
        valid = {item["id"] for item in options if not item.get("fails")}
        valid_a = [choice for choice in choices_a if choice in valid]
        valid_b = [choice for choice in choices_b if choice in valid]
        failed_a = any(choice not in valid for choice in choices_a)
        failed_b = any(choice not in valid for choice in choices_b)
        both_aligned = bool(
            valid_a and valid_b and not failed_a and not failed_b
        )
        preload = {
            "partner_a_color": partners[0].get("color") if partners else None,
            "partner_b_color": (
                partners[1].get("color") if len(partners) > 1 else None
            ),
            "aligned_on_trunk": both_aligned,
            "partner_decisions": {"A": choices_a, "B": choices_b},
            "diverged_partners": [
                {"partner": key, "color": color}
                for key, failed, color in (
                    ("A", failed_a, partners[0].get("color")
                     if partners else None),
                    ("B", failed_b, partners[1].get("color")
                     if len(partners) > 1 else None),
                )
                if failed
            ],
        }
        ranked_a = self.votes["A"].get("ranked_concerns", [])
        ranked_b = self.votes["B"].get("ranked_concerns", [])
        common_ids = set(ranked_a) & set(ranked_b)
        ordered_common = [
            fear["id"] for fear in self.case.get("fears", [])
            if fear.get("id") in common_ids
        ]
        shared = [self.case.get("d6_anchor"), *ordered_common]
        if self.case["id"] == "timothy-melanie-weah":
            frictions = [
                "D4: Timothy, Growth 4 con UPRO 3x; Melanie, Moderate 3 "
                "con $150,800 en efectivo al 0.09%.",
                "T1: $18,000 al 18% ($3,240/yr) frente a $15,032/yr libres.",
            ]
        else:
            frictions = [
                "D4: Emily ahorra $26,000/yr; Daniel carga $18,000 al 24.9% "
                "APR y tienen 1.4 meses de caja.",
                "T5: $8,000/yr al 529 y $0 al 401(k), con brecha de vida "
                "de -$2.35M.",
            ]
        if valid_a and valid_b and valid_a[0] != valid_b[0]:
            frictions[-1] += (
                f" Divergencia de voto: A eligió {valid_a[0]}, "
                f"B eligió {valid_b[0]}."
            )
        facts = self.case.get("facts", {})
        midpoint = {
            "free_cashflow_yearly": facts.get("free_cashflow_yearly", 15032),
            "card_balance": facts.get("card_balance"),
            "card_apr_pct": facts.get("card_apr_pct"),
            "cash_balance": facts.get("cash_balance"),
            "annual_401k": facts.get("annual_401k"),
        }
        self.phase = "mountain"
        self.mountain_preload = preload
        self.cordada_resolution = {
            "blind_pending": False, "partner_visible": True,
            "shared_100_common": shared,
            "frictions": frictions,
            "cashflow_midpoint": midpoint,
            "mountain_preload": copy.deepcopy(preload),
        }
        return copy.deepcopy(self.cordada_resolution)

    def state(self, mode=None):
        """Return session state without revealing a partner's pending vote."""
        votes_submitted = list(self.votes)
        visible_votes = (
            copy.deepcopy(self.votes) if len(self.votes) == 2 else None
        )
        facts = self.case.get("facts", self.case.get("metrics", {}))
        math_text = json.dumps(facts, ensure_ascii=False, default=str)
        camp_count = len(self.case.get("camps", []))
        selected_mode = _validate_mode(
            self.mode if mode is None else mode
        )
        active_camp = self._current_camp()
        plain_text = f"Campamento {self.camp_index + 1} de {camp_count}"
        hud = {
            "score": self.current_score,
            "status": self.case.get("score", {}).get("status"),
            "pillars": copy.deepcopy(
                self.case.get("score", {}).get("pillars", [])
            ),
        }
        return {
            "phase": self.phase, "blocked": self.blocked,
            "block_type": self.block_type, "mode": selected_mode,
            "case": copy.deepcopy(self.case), "camp_index": self.camp_index,
            "decisions": copy.deepcopy(self.decisions),
            "failed_branches": copy.deepcopy(self.failed_branches),
            "completed": self.completed, "votes_submitted": votes_submitted,
            "blind_votes_hidden": len(self.votes) == 1,
            "votes": visible_votes, "mountain_preload": self.mountain_preload,
            "hud": hud,
            "yearly": copy.deepcopy(self.case.get("yearly", [])),
            "active_camp": copy.deepcopy(active_camp),
            "views": {"plain": plain_text, "math": math_text},
            "display_text": (
                plain_text if selected_mode == "plain" else math_text
            ),
        }

    def _current_camp(self, camp_id=None):
        """Return the active camp, checking an optional camp identifier."""
        camps = self.case.get("camps", [])
        if self.camp_index >= len(camps):
            return None
        camp = camps[self.camp_index]
        if camp_id and camp["id"] != camp_id:
            raise ValueError(f"Campamento activo: {camp['id']}")
        return camp

    def _choice(self, camp, option_id):
        """Find a camp option by identifier."""
        return next((item for item in camp.get("options", [])
                     if item["id"] == option_id), None)

    def preview(self, option_id, camp_id=None):
        """Preview route direction and verified yearly impact."""
        self._require_mountain()
        camp = self._current_camp(camp_id)
        if camp is None:
            raise ValueError("No hay campamentos pendientes.")
        option = self._choice(camp, option_id)
        if option is None:
            raise ValueError(f"Opción desconocida: {option_id}")
        if camp["kind"] == "transition_event":
            trend = "transition_impact"
            yearly_impact = copy.deepcopy(camp.get("event"))
        elif option.get("fails"):
            if self.case["block"]["type"] == "wall":
                trend = "diverge_wall"
            else:
                trend = "diverge_crevasse"
            yearly_impact = self.case["block"]
        else:
            if option.get("to_score", 0) > option.get("from_score", 0):
                trend = "up_summit"
            else:
                trend = "flat_stagnant"
            yearly_impact = None
        before = self.current_score
        if before is None:
            before = option.get("from_score", self.case["score"].get("value"))
        after = option.get("to_score")
        math_text = f"score {before} -> {after}; trend={trend}"
        if camp["kind"] == "transition_event":
            plain_text = "El evento muestra el impacto publicado."
        else:
            plain_text = f"La ruta {option['label']} apunta a {trend}."
        return {
            "option_id": option_id, "camp_id": camp["id"],
            "trend_direction": trend, "score_before": before,
            "score_after": after,
            "combined_score_after": (
                camp.get("combined_to_score")
                if camp.get("supports_combined") else None
            ),
            "will_block": bool(option.get("fails")),
            "yearly_impact": yearly_impact, "plain": plain_text,
            "math": math_text,
            "display_text": plain_text if self.mode == "plain" else math_text,
        }

    def decide(self, option_id=None, camp_id=None, partner_choices=None,
               send_to_advisor_brief=False, advisor_question=None):
        """Apply a camp choice, or open a failed branch requiring rewind."""
        self._require_mountain()
        camp = self._current_camp(camp_id)
        if camp is None:
            self.completed = True
            self.phase = "summit"
            return {"completed": True, "phase": self.phase}
        option = (self._choice(camp, option_id)
                  if option_id is not None else None)
        if camp["kind"] == "transition_event":
            if option_id is not None and option is None:
                raise ValueError(f"Opción desconocida: {option_id}")
            question = advisor_question or (
                option.get("label") if option is not None else None
            )
            if ((option is not None and option.get("advisor")) or
                    send_to_advisor_brief) and question:
                self.uncalculated_questions.append(question)
            self.decisions.append({
                "camp_id": camp["id"], "option_id": option_id,
                "score_delta": None, "yearly_impact": camp.get("event"),
            })
            self.camp_index += 1
            self._finish_if_done()
            return {"blocked": False, "completed": self.completed,
                    "score_delta": None,
                    "yearly_impact": copy.deepcopy(camp.get("event")),
                    "uncalculated_questions": list(
                        self.uncalculated_questions
                    )}
        if option is None and not partner_choices:
            raise ValueError(f"Opción desconocida: {option_id}")
        if isinstance(partner_choices, dict):
            choices = [
                (self._partner_key(partner), choice)
                for partner, choice in partner_choices.items()
            ]
        elif partner_choices is not None:
            choices = [(None, choice) for choice in partner_choices]
        else:
            choices = [(None, option_id)]
        selected = [
            (partner, choice, self._choice(camp, choice))
            for partner, choice in choices
        ]
        failed_choice = next(
            (item for item in selected
             if item[2] is None or item[2].get("fails")), None
        )
        if failed_choice:
            failed_partner, failed_id, failed_option = failed_choice
            block = copy.deepcopy(self.case["block"])
            branch = {
                "camp_id": camp["id"], "option_id": failed_id,
                "color": self._failed_color(failed_option, failed_partner),
                "partner": failed_partner, "block": block,
                "root_cause": {
                    "facts": copy.deepcopy(block.get("facts", block)),
                    "tensions": copy.deepcopy(block.get("tensions", [])),
                    "behavioral_biases": copy.deepcopy(
                        block.get("behavioral_biases", [])
                    ),
                    "diagnostic_question": block.get("diagnostic_question"),
                    "plain": (
                        "Esta decisión mantiene el riesgo verificado del caso."
                    ),
                    "math": json.dumps(block, ensure_ascii=False),
                },
            }
            self.failed_branches.append(branch)
            self.blocked = True
            self.block_type = block["type"]
            return {"blocked": True, "block_type": self.block_type,
                    "failed_branch": copy.deepcopy(branch),
                    "root_cause": copy.deepcopy(branch["root_cause"])}
        if option is None:
            option = next((item[2] for item in selected if item[2]), None)
        before = self.current_score
        after = option.get("to_score") if option else before
        if after is not None:
            self.current_score = after
        self.decisions.append({"camp_id": camp["id"], "option_id": option_id,
                               "score_before": before, "score_after": after,
                               "combined_score_after": camp.get(
                                   "combined_to_score"
                               )})
        self.camp_index += 1
        self._finish_if_done()
        return {
            "blocked": False, "completed": self.completed,
            "score_before": before,
            "score_after": after,
            "combined_score_after": camp.get("combined_to_score"),
        }

    def _failed_color(self, option, partner_key=None):
        """Find the color of a partner whose choice failed."""
        partners = self.case.get("partners", [])
        if partner_key in ("A", "B"):
            index = 0 if partner_key == "A" else 1
            if index < len(partners):
                return partners[index].get("color")
        owner = (option or {}).get("owner")
        for index, partner in enumerate(partners[:2]):
            if partner.get("name") == owner:
                return partner.get("color")
            if index == 0 and owner is None:
                return partner.get("color")
        return None

    def _finish_if_done(self):
        """Advance the expedition to the summit after the final camp."""
        if self.camp_index >= len(self.case.get("camps", [])):
            self.completed = True
            self.phase = "summit"

    def rewind(self):
        """Clear the block and return to the failed camp."""
        if not self.blocked:
            raise PhaseOrderError(
                "Rewind solo está disponible tras un bloqueo."
            )
        self.blocked = False
        self.block_type = None
        self.camp_index = max(0, self.camp_index)
        return self.state()

    def overview(self, mode=None):
        """Show completed route choices and explored failed branches."""
        selected_mode = _validate_mode(
            self.mode if mode is None else mode
        )
        current = self.state(selected_mode)
        return {"decisions": copy.deepcopy(self.decisions),
                "failed_branches": copy.deepcopy(self.failed_branches),
                "camps": copy.deepcopy(self.case.get("camps", [])),
                "completed": self.completed, "phase": self.phase,
                "mode": selected_mode, "views": current["views"],
                "display_text": current["display_text"]}

    def restart(self):
        """Reset the expedition to its initial Quest phase."""
        self.__init__(self.case, self.mode)
        return self.state()

    def advisor_brief(self, mode=None):
        """Compile concerns, partner alignment, questions, and next step."""
        ranked = (self.quest or {}).get("ranked_concerns", [])
        subjective = (self.quest or {}).get("subjective_concern", "")
        if self.case.get("dual"):
            subjective = {
                partner.get("name"): self.votes.get(
                    "A" if index == 0 else "B", {}
                ).get("subjective_concern", "")
                for index, partner in enumerate(
                    self.case.get("partners", [])[:2]
                )
            }
        selected_mode = _validate_mode(
            self.mode if mode is None else mode
        )
        plain_text = f"Temores priorizados: {', '.join(ranked)}"
        math_text = json.dumps({"ranked_concerns": ranked,
                                "subjective_concerns": subjective},
                               ensure_ascii=False)
        return {
            "fears": copy.deepcopy(self.case.get("fears", [])),
            "ranked_concerns": copy.deepcopy(ranked),
            "subjective_concerns": subjective,
            "cordada": copy.deepcopy(self.cordada_resolution),
            "uncalculated_questions": list(self.uncalculated_questions),
            "failed_branches": copy.deepcopy(self.failed_branches),
            "step_1": self.case.get("step_1", ""),
            "mode": selected_mode,
            "views": {"plain": plain_text, "math": math_text},
        }
