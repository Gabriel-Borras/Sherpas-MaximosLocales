"""Motor determinista de la Run IRL (Fase 4 / Post-Cima) para Sherpas.

Implementa la ejecucion paso a paso en la vida real sobre datos verificados de
``cases/<case_id>/`` (``financial-health.json``, ``investment-analysis.json`` y
``persona.md``), sin inventar cifras:

- Secuencia ``Dia 0 -> Dia 3 -> Dia 14 -> Dia 30 -> Fechas hito`` reales
  desde ``savingsWaterfall``, ``score.top_moves``, ``score.combined_moves``,
  ``goals.chartGoals`` y *Transition alerts* de ``persona.md``.
- Modo Enfoque (``get_focus_mode_view`` / ``focus_step``): muestra unicamente
  el proximo objetivo inmediato de 3 minutos (``Step 1``) o la tarea activa/
  vencida prioritaria, separado de ``get_mountain_overview`` vs
  ``repeat_expedition`` / ``reset_expedition``.
- Modo Parejas (``timothy-melanie-weah`` y ``daniel-emily-johnson``): reparto
  por responsable (``Owner A`` / ``Owner B``) y check conjunto ``2/2``
  mediante ``check_step(step_id, member="A"|"B")``.
- Avance implacable del tiempo (``advance_day(current_day)``): arrastra pasos
  no completados (o ``1/2`` en pareja) como ``overdue`` calculando el coste
  real de inercia (APR de tarjetas, ahorro fiscal 401(k)/HSA perdido,
  *tax drag* y dias sin cobertura).
- Navegacion bidireccional (``get_timeline_view(current_day)``) y exportacion
  de calendario RFC 5545 (``export_ics``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
from typing import Any

SUPPORTED_CASES: tuple[str, ...] = (
    "michael-carter",
    "samantha-lewis",
    "timothy-melanie-weah",
    "daniel-emily-johnson",
)

DEFAULT_FALLBACK_CASES_DIR = Path(
    r"C:\Users\Silvia\.gemini\antigravity\scratch\hackathon-upv-2026\cases"
)
DEFAULT_PLAN_START_DATE = date(2026, 11, 1)

_BASE_CHECKIN_DAYS: tuple[int, ...] = (0, 3, 14, 30)


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def resolve_case_dir(case_id: str, cases_dir: str | Path | None = None) -> Path:
    """Resolve the directory holding ``financial-health.json``, ``investment-analysis.json`` and ``persona.md``."""
    candidates: list[Path] = []
    if cases_dir is not None:
        candidates.append(Path(cases_dir) / case_id)
    candidates.append(_repo_root() / "cases" / case_id)
    env_dir = os.environ.get("SHERPAS_CASES_DIR")
    if env_dir:
        candidates.append(Path(env_dir) / case_id)
    candidates.append(DEFAULT_FALLBACK_CASES_DIR / case_id)

    required = ("financial-health.json", "investment-analysis.json", "persona.md")
    for candidate in candidates:
        if candidate.is_dir() and all((candidate / fname).is_file() for fname in required):
            return candidate

    searched = ", ".join(str(p) for p in candidates)
    raise FileNotFoundError(
        f"No se encontraron los archivos del caso '{case_id}' en: {searched}"
    )


def list_available_cases(cases_dir: str | Path | None = None) -> list[str]:
    """Return available case identifiers found across configured case directories."""
    available: list[str] = []
    for case_id in SUPPORTED_CASES:
        try:
            resolve_case_dir(case_id, cases_dir=cases_dir)
            available.append(case_id)
        except FileNotFoundError:
            continue
    return available


def _parse_persona_markdown(markdown_text: str) -> dict[str, Any]:
    """Extract structured sections from ``persona.md`` without inventing facts."""
    sections: dict[str, str] = {}
    current_heading = "_preamble"
    buffer: list[str] = []
    for line in markdown_text.splitlines():
        if line.startswith("## "):
            sections[current_heading] = "\n".join(buffer).strip()
            current_heading = line[3:].strip()
            buffer = []
        else:
            buffer.append(line)
    sections[current_heading] = "\n".join(buffer).strip()

    concerns: dict[str, str] = {}
    for line in sections.get("Objective concerns", "").splitlines():
        cleaned_line = line.strip()
        match = re.match(r"^- \*\*(O\d+)\b(?:[^:*]+)?:\s*(.+)$", cleaned_line)
        if not match:
            match = re.match(r"^- \*\*(O\d+)\s+([^:]+):\*\*\s*(.+)$", cleaned_line)
            if match:
                concerns[match.group(1)] = f"{match.group(2)}: {match.group(3)}".replace("**", "").strip()
                continue
        if match:
            concerns[match.group(1)] = match.group(2).replace("**", "").strip()

    tensions: dict[str, str] = {}
    for line in sections.get("Tensions", "").splitlines():
        match = re.match(r"^- \*\*(T\d+)\b.*?\*\*\s*(.+)$", line.strip())
        if match:
            tensions[match.group(1)] = match.group(2).strip()

    transition_alerts: list[str] = []
    for line in sections.get("Transition alerts", "").splitlines():
        cleaned = line.strip()
        if cleaned.startswith("- "):
            transition_alerts.append(cleaned[2:].strip())
        elif cleaned and not cleaned.lower().startswith("none detected"):
            transition_alerts.append(cleaned)

    return {
        "raw": markdown_text,
        "sections": sections,
        "objective_concerns": concerns,
        "tensions": tensions,
        "transition_alerts_text": sections.get("Transition alerts", ""),
        "transition_alerts": transition_alerts,
        "d3_text": sections.get("D3: Gap severity", ""),
        "d5_text": sections.get("D5: Decision-making style", ""),
        "d6_text": sections.get("D6: Motivational anchor", ""),
    }


def load_case_data(case_id: str, cases_dir: str | Path | None = None) -> dict[str, Any]:
    """Load real JSON and persona markdown files for ``case_id``."""
    case_path = resolve_case_dir(case_id, cases_dir=cases_dir)
    fh = json.loads((case_path / "financial-health.json").read_text(encoding="utf-8"))
    ia = json.loads((case_path / "investment-analysis.json").read_text(encoding="utf-8"))
    persona_md = (case_path / "persona.md").read_text(encoding="utf-8")
    return {
        "case_id": case_id,
        "case_dir": str(case_path),
        "financial_health": fh,
        "investment_analysis": ia,
        "persona": _parse_persona_markdown(persona_md),
    }


def _parse_rate(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip().rstrip("%")
        try:
            return float(stripped) / (100.0 if "%" in value else 1.0)
        except ValueError:
            return 0.0
    return 0.0


def _fmt_usd(amount: float) -> str:
    sign = "-" if amount < 0 else ""
    abs_val = abs(amount)
    if abs(abs_val - round(abs_val)) < 0.005:
        return f"{sign}${round(abs_val):,.0f}"
    return f"{sign}${abs_val:,.2f}"


def _extract_waterfall_rows(ia: dict[str, Any]) -> list[dict[str, Any]]:
    raw = (
        ia.get("key_metrics", {})
        .get("savingsAndContributions", {})
        .get("savingsWaterfall", [])
    )
    if not raw or len(raw) < 2:
        return []
    rows: list[dict[str, Any]] = []
    for row in raw[1:]:
        if not isinstance(row, list) or len(row) < 2:
            continue
        padded = row + [""] * max(0, 8 - len(row))
        rows.append(
            {
                "bucket_number": padded[0],
                "bucket": str(padded[1]),
                "current": padded[2],
                "optimal_target": padded[3],
                "status": str(padded[4]),
                "delta": padded[5],
                "flag": str(padded[6]),
                "notes": str(padded[7]),
            }
        )
    return rows


def _waterfall_by_number(rows: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    mapping: dict[int, dict[str, Any]] = {}
    for row in rows:
        num = row.get("bucket_number")
        if isinstance(num, int):
            mapping[num] = row
    return mapping


def _extract_federal_ordinary_rate(ia: dict[str, Any]) -> float:
    rows = ia.get("key_metrics", {}).get("taxDragAnalysis", {}).get("effectiveTaxMargin", [])
    for row in rows:
        if isinstance(row, list) and len(row) >= 2 and row[0] == "Federal ordinary":
            return _parse_rate(row[1])
    return 0.0


def _extract_tax_drag_annual(ia: dict[str, Any]) -> float:
    rollup = ia.get("key_metrics", {}).get("taxDragAnalysis", {}).get("householdRollup", [])
    for row in rollup:
        if isinstance(row, list) and len(row) >= 2 and "In-scope tax cost" in str(row[0]):
            return float(row[1])
    for row in rollup:
        if isinstance(row, list) and len(row) >= 2 and "Total annual tax cost" in str(row[0]):
            return float(row[1])
    return 0.0


def _extract_cash_earned_annual(ia: dict[str, Any]) -> float:
    summary = ia.get("key_metrics", {}).get("cashNeeds", {}).get("summaryIncome", [])
    for row in summary:
        if isinstance(row, list) and len(row) >= 2 and row[0] == "Total":
            try:
                return float(row[1])
            except (TypeError, ValueError):
                return 0.0
    return 0.0


def _extract_life_shortfall_from_persona(persona: dict[str, Any]) -> float:
    d3 = persona.get("d3_text", "")
    # Sum explicit "shortfall of $X" / "a shortfall of $X" inside Life insurance / Protection bullets.
    total = 0.0
    for line in d3.splitlines():
        lower = line.lower()
        if "life insurance" in lower or ("protection" in lower and "life" in lower):
            for m in re.finditer(r"shortfall of \$([0-9,]+)|\$([0-9,]+)\s+shortfall", line):
                val = m.group(1) or m.group(2)
                total += float(val.replace(",", ""))
    if total > 0:
        return total
    # Fallback: check Objective concerns O1/O2/O3 for "Shortfalls of $X ... and $Y"
    for text in persona.get("objective_concerns", {}).values():
        if "life insurance" in text.lower() or "shortfall" in text.lower():
            matches = re.findall(r"\$([0-9,]+)", text)
            if "shortfalls of" in text.lower() and len(matches) >= 2:
                return sum(float(x.replace(",", "")) for x in matches[:2])
            m = re.search(r"shortfall of \$([0-9,]+)", text.lower())
            if m:
                return float(m.group(1).replace(",", ""))
    return 0.0


def _extract_unconfirmed_assets(persona: dict[str, Any]) -> list[str]:
    text = " ".join(persona.get("objective_concerns", {}).values()) + "\n" + persona.get("d3_text", "")
    assets: list[str] = []
    if re.search(r"home(?:owners)?\s+policy.*?(?:not recorded|uninsured|no homeowners)", text, re.I) or (
        "no homeowners" in text.lower() or "no home or auto insurance recorded" in text.lower()
    ):
        assets.append("Primary home ($900,000)" if "$900,000" in text else "Primary home")
    if "porsche cayenne" in text.lower() and "uninsured" in text.lower():
        assets.append("Porsche Cayenne ($80,000)")
    return assets


def _parse_iso_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def _month_year_label(d: date) -> str:
    months = (
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    )
    return f"{months[d.month - 1]} {d.year}"


@dataclass
class IRLStep:
    """Single actionable step inside the Run IRL timeline."""

    step_id: str
    node_id: str
    day: int
    due_date: date
    phase: str
    title: str
    action_plain: str
    action_math: str
    estimated_minutes: int
    ownership_mode: str  # "single" | "owner_a" | "owner_b" | "joint"
    owner_label: str
    required_members: tuple[str, ...]
    waterfall_buckets: tuple[int, ...] = ()
    json_sources: tuple[str, ...] = ()
    inertia_lever_key: str | None = None
    completed_by: dict[str, int] = field(default_factory=dict)

    @property
    def is_completed(self) -> bool:
        return all(m in self.completed_by for m in self.required_members)

    @property
    def completion_ratio(self) -> str:
        done = sum(1 for m in self.required_members if m in self.completed_by)
        return f"{done}/{len(self.required_members)}"

    @property
    def missing_members(self) -> list[str]:
        return [m for m in self.required_members if m not in self.completed_by]

    def status_at(self, current_day: int) -> str:
        if self.is_completed:
            return "completed"
        if current_day > self.day:
            return "overdue"
        if current_day == self.day:
            return "active"
        return "upcoming"

    def to_dict(
        self,
        current_day: int,
        member_names: dict[str, str],
        step_inertia: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        status = self.status_at(current_day)
        missing_labels = [member_names.get(m, m) for m in self.missing_members]
        return {
            "step_id": self.step_id,
            "node_id": self.node_id,
            "day": self.day,
            "due_date": self.due_date.isoformat(),
            "phase": self.phase,
            "title": self.title,
            "action_plain": self.action_plain,
            "action_math": self.action_math,
            "estimated_minutes": self.estimated_minutes,
            "ownership_mode": self.ownership_mode,
            "owner_label": self.owner_label,
            "required_members": list(self.required_members),
            "completed_by": dict(self.completed_by),
            "is_completed": self.is_completed,
            "completion_ratio": self.completion_ratio,
            "missing_members": list(self.missing_members),
            "missing_member_labels": missing_labels,
            "status": status,
            "days_overdue": max(0, current_day - self.day) if status == "overdue" else 0,
            "waterfall_buckets": list(self.waterfall_buckets),
            "json_sources": list(self.json_sources),
            "inertia_lever_key": self.inertia_lever_key,
            "inertia_cost": step_inertia or {},
        }


class IRLEngine:
    """Stateful deterministic Run IRL engine for a Sherpas household case."""

    def __init__(
        self,
        case_id: str,
        *,
        cases_dir: str | Path | None = None,
        start_date: date | None = None,
    ) -> None:
        self.case_id = case_id
        self.case_data = load_case_data(case_id, cases_dir=cases_dir)
        self.fh: dict[str, Any] = self.case_data["financial_health"]
        self.ia: dict[str, Any] = self.case_data["investment_analysis"]
        self.persona: dict[str, Any] = self.case_data["persona"]

        window_end = (
            self.ia.get("key_metrics", {})
            .get("performanceAnalysis", {})
            .get("window", {})
            .get("endDate")
        )
        inferred_start = _parse_iso_date(window_end) if window_end else None
        self.start_date: date = start_date or inferred_start or DEFAULT_PLAN_START_DATE

        self.household: list[dict[str, Any]] = self.fh.get("case", {}).get("household", [])
        self.adults: list[dict[str, Any]] = [
            p for p in self.household if p.get("role") in ("client", "co-client")
        ]
        self.is_couple: bool = len(self.adults) >= 2
        self.member_names: dict[str, str] = self._build_member_names()
        self.waterfall_rows = _extract_waterfall_rows(self.ia)
        self.waterfall_map = _waterfall_by_number(self.waterfall_rows)

        self.current_day: int = 0
        self.active_view: str = "focus_mode"
        self.simulation_run_count: int = 1
        self.simulation_completed: bool = True
        self.simulation_choices: list[dict[str, Any]] = self._default_summit_choices()

        self.inertia_levers: dict[str, dict[str, Any]] = self._extract_inertia_levers()
        self.steps: list[IRLStep] = self._build_steps()
        self._steps_by_id: dict[str, IRLStep] = {s.step_id: s for s in self.steps}

    def _build_member_names(self) -> dict[str, str]:
        if not self.adults:
            return {"single": "Titular"}
        client = self.adults[0].get("first_name", "Titular")
        if not self.is_couple:
            return {"single": client, "client": client, "A": client}
        co_client = self.adults[1].get("first_name", "Pareja")
        return {
            "A": f"Owner A ({client})",
            "B": f"Owner B ({co_client})",
            "A_first": client,
            "B_first": co_client,
        }

    def _default_summit_choices(self) -> list[dict[str, Any]]:
        score_obj = self.fh.get("score", {})
        top_moves = score_obj.get("top_moves", [])
        return [
            {
                "title": m.get("title"),
                "action": m.get("action"),
                "score_before": m.get("score_before"),
                "score_after": m.get("score_after"),
                "effort": m.get("effort"),
            }
            for m in top_moves
        ]

    def _extract_inertia_levers(self) -> dict[str, dict[str, Any]]:
        """Derive all ongoing inertia cost levers strictly from JSON & persona.md."""
        levers: dict[str, dict[str, Any]] = {}
        fed_ord = _extract_federal_ordinary_rate(self.ia)

        # 1. High-interest revolving card debt (>7% APR)
        liabilities = self.fh.get("profile", {}).get("liabilities", [])
        high_cards = [
            lib
            for lib in liabilities
            if lib.get("type") == "PERSONAL_CREDIT_CARD" and float(lib.get("interest_rate", 0)) > 0.07
        ]
        if high_cards:
            card = max(high_cards, key=lambda x: float(x.get("balance", 0)) * float(x.get("interest_rate", 0)))
            bal = float(card.get("balance", 0))
            apr = float(card.get("interest_rate", 0))
            annual_gross = round(bal * apr, 2)
            daily_gross = round(annual_gross / 365.0, 2)
            cash_earned = _extract_cash_earned_annual(self.ia)
            accessible_cash = float(
                self.ia.get("key_metrics", {}).get("cashNeeds", {}).get("accessibleCash", 0)
            )
            net_annual = round(annual_gross - cash_earned, 2) if cash_earned > 0 else annual_gross
            levers["high_apr_card"] = {
                "key": "high_apr_card",
                "label": f"{card.get('name')} ({_fmt_usd(bal)} al {apr * 100:.1f}% APR)",
                "balance_usd": bal,
                "apr_pct": round(apr * 100, 2),
                "annual_cost_usd": annual_gross,
                "daily_cost_usd": daily_gross,
                "cash_earned_annual_usd": cash_earned,
                "accessible_cash_usd": accessible_cash,
                "net_annual_loss_usd": net_annual,
                "source": "financial-health.json: profile.liabilities + investment-analysis.json: cashNeeds.summaryIncome",
            }

        # 2. Unused 401(k) tax-advantaged room (waterfall #13)
        wf13 = self.waterfall_map.get(13, {})
        wf13_cur = wf13.get("current")
        wf13_tgt = wf13.get("optimal_target")
        if isinstance(wf13_cur, (int, float)) and isinstance(wf13_tgt, (int, float)) and wf13_tgt > wf13_cur:
            room_401k = float(wf13_tgt - wf13_cur)
            tax_saved_401k = round(room_401k * fed_ord, 2)
            levers["401k_tax_delay"] = {
                "key": "401k_tax_delay",
                "label": f"Margen 401(k) sin aportar ({_fmt_usd(room_401k)} al {fed_ord * 100:.0f}%)",
                "unused_room_usd": room_401k,
                "marginal_rate_pct": round(fed_ord * 100, 2),
                "annual_cost_usd": tax_saved_401k,
                "daily_cost_usd": round(tax_saved_401k / 365.0, 2),
                "source": "investment-analysis.json: savingsWaterfall[#13] + effectiveTaxMargin",
            }

        # 3. Unused HSA room (waterfall #11)
        wf11 = self.waterfall_map.get(11, {})
        wf11_cur = wf11.get("current")
        wf11_tgt = wf11.get("optimal_target")
        if isinstance(wf11_cur, (int, float)) and isinstance(wf11_tgt, (int, float)) and wf11_tgt > wf11_cur:
            room_hsa = float(wf11_tgt - wf11_cur)
            tax_saved_hsa = round(room_hsa * fed_ord, 2)
            levers["hsa_tax_delay"] = {
                "key": "hsa_tax_delay",
                "label": f"Margen HSA sin aportar ({_fmt_usd(room_hsa)} al {fed_ord * 100:.0f}%)",
                "unused_room_usd": room_hsa,
                "marginal_rate_pct": round(fed_ord * 100, 2),
                "annual_cost_usd": tax_saved_hsa,
                "daily_cost_usd": round(tax_saved_hsa / 365.0, 2),
                "source": "investment-analysis.json: savingsWaterfall[#11] + effectiveTaxMargin",
            }

        # 4. In-scope taxable investment tax drag
        tax_drag = _extract_tax_drag_annual(self.ia)
        if tax_drag > 0:
            levers["tax_drag"] = {
                "key": "tax_drag",
                "label": f"Fuga fiscal en cuenta sujeta a impuestos ({_fmt_usd(tax_drag)}/ano)",
                "annual_cost_usd": round(tax_drag, 2),
                "daily_cost_usd": round(tax_drag / 365.0, 2),
                "source": "investment-analysis.json: taxDragAnalysis.householdRollup",
            }

        # 5. Life insurance & liability protection gap (risk days)
        life_shortfall = _extract_life_shortfall_from_persona(self.persona)
        pillars = {p.get("pillar"): p for p in self.fh.get("score", {}).get("pillars", [])}
        prot_pillar = pillars.get("Insurance and protection", {})
        if life_shortfall > 0:
            levers["life_protection_gap"] = {
                "key": "life_protection_gap",
                "label": f"Brecha seguro de vida ({_fmt_usd(-life_shortfall)}, Proteccion {prot_pillar.get('points_shown_in_app', '')})",
                "shortfall_usd": life_shortfall,
                "protection_points": prot_pillar.get("points_shown_in_app", ""),
                "annual_cost_usd": 0.0,
                "daily_cost_usd": 0.0,
                "tracks_days_uninsured": True,
                "source": "persona.md: D3 + financial-health.json: score.pillars",
            }

        # 6. Unconfirmed home / vehicle property coverage (e.g. Samantha)
        unconfirmed = _extract_unconfirmed_assets(self.persona)
        if unconfirmed:
            levers["unconfirmed_property_policy"] = {
                "key": "unconfirmed_property_policy",
                "label": "Polizas sin confirmar: " + ", ".join(unconfirmed),
                "unconfirmed_assets": unconfirmed,
                "annual_cost_usd": 0.0,
                "daily_cost_usd": 0.0,
                "tracks_days_uninsured": True,
                "source": "persona.md: O4 + financial-health.json: score.top_moves[0]",
            }

        return levers

    def _add_step(
        self,
        steps: list[IRLStep],
        *,
        step_id: str,
        node_id: str,
        day: int,
        phase: str,
        title: str,
        action_plain: str,
        action_math: str,
        estimated_minutes: int,
        ownership_mode: str,
        waterfall_buckets: tuple[int, ...] = (),
        json_sources: tuple[str, ...] = (),
        inertia_lever_key: str | None = None,
    ) -> None:
        if ownership_mode == "single":
            owner_label = self.member_names["single"]
            required = ("single",)
        elif ownership_mode == "owner_a":
            owner_label = self.member_names["A"]
            required = ("A",)
        elif ownership_mode == "owner_b":
            owner_label = self.member_names["B"]
            required = ("B",)
        elif ownership_mode == "joint":
            a_name = self.member_names.get("A_first", "A")
            b_name = self.member_names.get("B_first", "B")
            owner_label = f"Conjunto 2/2 ({a_name} & {b_name})"
            required = ("A", "B")
        else:
            raise ValueError(f"ownership_mode invalido: {ownership_mode}")

        steps.append(
            IRLStep(
                step_id=step_id,
                node_id=node_id,
                day=day,
                due_date=self.start_date + timedelta(days=day),
                phase=phase,
                title=title,
                action_plain=action_plain,
                action_math=action_math,
                estimated_minutes=estimated_minutes,
                ownership_mode=ownership_mode,
                owner_label=owner_label,
                required_members=required,
                waterfall_buckets=waterfall_buckets,
                json_sources=json_sources,
                inertia_lever_key=inertia_lever_key,
            )
        )

    def _build_steps(self) -> list[IRLStep]:
        """Build the Day 0 -> Day 3 -> Day 14 -> Day 30 -> Milestones step sequence."""
        steps: list[IRLStep] = []
        if self.case_id == "michael-carter":
            self._build_michael_steps(steps)
        elif self.case_id == "samantha-lewis":
            self._build_samantha_steps(steps)
        elif self.case_id == "timothy-melanie-weah":
            self._build_weah_steps(steps)
        elif self.case_id == "daniel-emily-johnson":
            self._build_johnson_steps(steps)
        else:
            self._build_generic_steps(steps)

        self._append_real_milestones(steps)
        steps.sort(key=lambda s: (s.day, s.step_id))
        return steps

    def _build_michael_steps(self, steps: list[IRLStep]) -> None:
        card = self.inertia_levers["high_apr_card"]
        k401 = self.inertia_levers["401k_tax_delay"]
        tdrag = self.inertia_levers["tax_drag"]
        top_moves = self.fh.get("score", {}).get("top_moves", [])
        umb_move = top_moves[0] if top_moves else {}
        glide_move = top_moves[2] if len(top_moves) > 2 else {}

        self._add_step(
            steps,
            step_id="step_0_pay_amex",
            node_id="day_0",
            day=0,
            phase="day_0",
            title="Paso 1 (3 min): Ordenar pago total de Amex Platinum ($3,500)",
            action_plain=(
                "Usa $3,500 de tus $27,000 en banco para liquidar hoy la tarjeta Amex al 20% "
                "y cortar una fuga garantizada de $700/ano ($1.92/dia)."
            ),
            action_math=(
                f"savingsWaterfall #8: Pay high-interest debt (>7%) | {card['label']} -> "
                f"{_fmt_usd(card['annual_cost_usd'])}/yr ({_fmt_usd(card['daily_cost_usd'])}/day)."
            ),
            estimated_minutes=3,
            ownership_mode="single",
            waterfall_buckets=(8,),
            json_sources=("profile.liabilities", "savingsWaterfall[8]"),
            inertia_lever_key="high_apr_card",
        )
        self._add_step(
            steps,
            step_id="step_3_confirm_amex_zero_and_umbrella",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3: Confirmar Amex a $0 y cotizar poliza Umbrella $1M",
            action_plain=(
                "Verifica que el saldo de Amex quedo en $0 y pide presupuesto del escudo "
                "Umbrella de $1M para subir tu score de 26 a 31."
            ),
            action_math=(
                f"top_moves[0]: {umb_move.get('action', 'Add $1M of umbrella')} "
                f"(score {umb_move.get('score_before', 26)} -> {umb_move.get('score_after', 31)}); "
                "savingsWaterfall #2."
            ),
            estimated_minutes=10,
            ownership_mode="single",
            waterfall_buckets=(2, 8),
            json_sources=("score.top_moves[0]", "savingsWaterfall[2]"),
            inertia_lever_key="life_protection_gap",
        )
        self._add_step(
            steps,
            step_id="step_14_review_jnk_and_glide",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14: Revisar bono JNK ($527/ano tax drag) y ajuste growth 74% -> 88%",
            action_plain=(
                "Revisa el fondo JNK ($15,000) en tu cuenta imponible (cuesta ~$527/ano en impuestos) "
                "y planifica mover ~$19,900 hacia tu perfil growth objetivo."
            ),
            action_math=(
                f"taxDragAnalysis: In-scope tax cost {_fmt_usd(tdrag['annual_cost_usd'])}/yr "
                "(JNK $247.20/yr al 24%); top_moves[2]: "
                f"{glide_move.get('action', '74% -> 88% growth')}."
            ),
            estimated_minutes=15,
            ownership_mode="single",
            waterfall_buckets=(14,),
            json_sources=("taxDragAnalysis.householdRollup", "score.top_moves[2]"),
            inertia_lever_key="tax_drag",
        )
        self._add_step(
            steps,
            step_id="step_30_boost_401k_and_hsa",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30: Subir aportacion 401(k) (+$7,500 margen = $1,800/ano ahorro fiscal)",
            action_plain=(
                "Sube en nomina tu aportacion al 401(k) de $17,000 a $24,500 (+$7,500 de margen, "
                "$1,800/ano menos de impuestos) y completa los $400 restantes de tu HSA."
            ),
            action_math=(
                f"savingsWaterfall #13: 401(k) $17,000 -> $24,500 ({_fmt_usd(k401['annual_cost_usd'])}/yr "
                "ahorro fiscal al 24%); savingsWaterfall #11 HSA $4,000 -> $4,400; #10 Roth IRA $4,500."
            ),
            estimated_minutes=10,
            ownership_mode="single",
            waterfall_buckets=(10, 11, 13),
            json_sources=("savingsWaterfall[10,11,13]", "persona.md: O7"),
            inertia_lever_key="401k_tax_delay",
        )

    def _build_samantha_steps(self, steps: list[IRLStep]) -> None:
        tdrag = self.inertia_levers["tax_drag"]
        k401 = self.inertia_levers["401k_tax_delay"]
        hsa = self.inertia_levers["hsa_tax_delay"]
        top_moves = self.fh.get("score", {}).get("top_moves", [])
        cov_move = top_moves[0] if top_moves else {}
        conc_move = top_moves[1] if len(top_moves) > 1 else {}

        self._add_step(
            steps,
            step_id="step_0_confirm_home_auto_policies",
            node_id="day_0",
            day=0,
            phase="day_0",
            title="Paso 1 (3 min): Confirmar polizas de hogar ($900k) y Porsche Cayenne ($80k)",
            action_plain=(
                "Sube o confirma hoy la vigencia de tu seguro de hogar ($4,500/ano presupuestados) "
                "y del Porsche Cayenne; figuran sin poliza registrada pese a tu score 82."
            ),
            action_math=(
                f"top_moves[0]: {cov_move.get('action', 'Add homeowners insurance')} "
                f"(score {cov_move.get('score_before', 82)} -> {cov_move.get('score_after', 84)}); "
                "persona.md O4 ($900,000 home & $80,000 Porsche Cayenne)."
            ),
            estimated_minutes=3,
            ownership_mode="single",
            waterfall_buckets=(2,),
            json_sources=("score.top_moves[0]", "persona.md: O4"),
            inertia_lever_key="unconfirmed_property_policy",
        )
        self._add_step(
            steps,
            step_id="step_3_verify_coverage_and_tax_drag",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3: Verificar polizas activas y auditar $3,032/ano de tax drag",
            action_plain=(
                "Confirma cobertura activa de vivienda/vehiculo y recopila el cost basis de tu "
                "brokerage ($300k) para frenar los ~$3,032/ano de fuga fiscal en dividendos."
            ),
            action_math=(
                f"taxDragAnalysis: In-scope tax cost {_fmt_usd(tdrag['annual_cost_usd'])}/yr "
                f"({_fmt_usd(tdrag['daily_cost_usd'])}/day); JNK $1,229.15/yr + SCHD $852.85/yr "
                "al 35.8%; costBasisBlockingNotes."
            ),
            estimated_minutes=15,
            ownership_mode="single",
            waterfall_buckets=(2, 14),
            json_sources=("taxDragAnalysis", "persona.md: O4, O8"),
            inertia_lever_key="tax_drag",
        )
        self._add_step(
            steps,
            step_id="step_14_hsa_and_vti_concentration",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14: Aportar $4,400 a HSA y bajar concentracion VTI (39% -> 25%)",
            action_plain=(
                "Abre o aporta el maximo de $4,400 al HSA ($1,408/ano ahorro fiscal) y planifica "
                "bajar VTI del 39% al 25% (~$58,300) ajustando tu riesgo de 85% a 80%."
            ),
            action_math=(
                f"savingsWaterfall #11 HSA $0 -> $4,400 ({_fmt_usd(hsa['annual_cost_usd'])}/yr al 32%); "
                f"top_moves[1]: {conc_move.get('action', 'VTI 39% -> 25%')}."
            ),
            estimated_minutes=15,
            ownership_mode="single",
            waterfall_buckets=(11,),
            json_sources=("savingsWaterfall[11]", "score.top_moves[1,2]"),
            inertia_lever_key="hsa_tax_delay",
        )
        self._add_step(
            steps,
            step_id="step_30_activate_retirement_401k",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30: Activar jubilacion ($0 actual -> $24,500 margen 401(k) / $7,500 IRA)",
            action_plain=(
                "Hoy tienes $0 en cuentas de retiro y te quedas sin liquidez a los 74 anos (2053). "
                "Confirma acceso al 401(k) ($24,500) o aporta $7,500 a Traditional IRA deducible."
            ),
            action_math=(
                f"savingsWaterfall #13 401(k) $0 -> $24,500 ({_fmt_usd(k401['annual_cost_usd'])}/yr "
                "potencial al 32%); projections.yearly 2053: -$227,414 investable_assets."
            ),
            estimated_minutes=15,
            ownership_mode="single",
            waterfall_buckets=(13,),
            json_sources=("savingsWaterfall[13]", "persona.md: O1, O7", "projections.yearly"),
            inertia_lever_key="401k_tax_delay",
        )

    def _build_weah_steps(self, steps: list[IRLStep]) -> None:
        card = self.inertia_levers["high_apr_card"]
        k401 = self.inertia_levers["401k_tax_delay"]
        net_loss = card["net_annual_loss_usd"]

        self._add_step(
            steps,
            step_id="step_0_melanie_schedule_card_payoff",
            node_id="day_0",
            day=0,
            phase="day_0",
            title="Paso 1 (3 min) — Owner B (Melanie): Programar pago tarjeta Chase $18,000 (18%)",
            action_plain=(
                "Melanie, programa hoy el pago de los $18,000 de la tarjeta Chase al 18% usando parte "
                "de tus $150,000 en efectivo (que rinden ~$150/ano mientras la tarjeta quema $3,240/ano)."
            ),
            action_math=(
                f"Owner B (Melanie) Cash account $150,000 -> Chase CC $18,000 @ 18% APR: "
                f"{_fmt_usd(card['annual_cost_usd'])}/yr brutos ({_fmt_usd(card['daily_cost_usd'])}/day) "
                f"vs {_fmt_usd(card['cash_earned_annual_usd'])}/yr cash earned "
                f"({_fmt_usd(net_loss)}/yr perdida neta; top_moves[0]: 60 -> 62)."
            ),
            estimated_minutes=3,
            ownership_mode="owner_b",
            waterfall_buckets=(8,),
            json_sources=("profile.liabilities", "profile.accounts", "savingsWaterfall[8]"),
            inertia_lever_key="high_apr_card",
        )
        self._add_step(
            steps,
            step_id="step_3_melanie_confirm_card_paid",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3 — Owner B (Melanie): Liquidar completamente tarjeta $18,000 al 18% APR",
            action_plain=(
                "Melanie, confirma que la tarjeta Chase ($18,000 al 18% APR) quedo liquidada a $0 "
                "con el excedente de efectivo ($60,222.50 sobre la reserva)."
            ),
            action_math=(
                f"savingsWaterfall #8 Pay high-interest debt (>7%): $18,000 -> $0; "
                f"accessibleCash $150,800 (excess $60,222.50); elimina {_fmt_usd(card['daily_cost_usd'])}/day."
            ),
            estimated_minutes=5,
            ownership_mode="owner_b",
            waterfall_buckets=(8,),
            json_sources=("savingsWaterfall[8]", "cashNeeds.accessibleCashExcess"),
            inertia_lever_key="high_apr_card",
        )
        self._add_step(
            steps,
            step_id="step_3_joint_life_and_umbrella",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3 — Check conjunto (2/2): Solicitar seguro de vida +$1.1M y Umbrella $1M",
            action_plain=(
                "Timothy y Melanie deben confirmar ambos (2/2) la solicitud de seguro de vida "
                "($610k Timothy + $490k Melanie) y poliza Umbrella de $1M para proteger a Liam y Josh."
            ),
            action_math=(
                "combined_moves[0]: Pay down revolving card + Add life cover + Add umbrella cover "
                "(score 60 -> 78); savingsWaterfall #2: $250,000 -> $2,350,000."
            ),
            estimated_minutes=15,
            ownership_mode="joint",
            waterfall_buckets=(2,),
            json_sources=("score.combined_moves[0]", "savingsWaterfall[2]", "persona.md: O1, O3"),
            inertia_lever_key="life_protection_gap",
        )
        self._add_step(
            steps,
            step_id="step_14_timothy_reduce_upro",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14 — Owner A (Timothy): Reducir exposicion apalancada UPRO 3x ($12,740)",
            action_plain=(
                "Timothy, reduce el ETF apalancado 3x UPRO ($12,740 en tu Roth IRA, volatilidad 30%) "
                "hacia el objetivo moderado compartido (60% renta variable) para alinear la cordada."
            ),
            action_math=(
                "positions: UPRO (ProShares UltraPro S&P500, 3x leveraged) $12,740 "
                "(50.96% de IRA - Roth Timothy, volatility3y 30.04%); persona.md D4b/O6."
            ),
            estimated_minutes=10,
            ownership_mode="owner_a",
            waterfall_buckets=(10,),
            json_sources=("positions[UPRO]", "performanceAnalysis.goalGroups", "persona.md: O6"),
        )
        self._add_step(
            steps,
            step_id="step_14_joint_bind_protection",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14 — Check conjunto (2/2): Activar polizas de vida (+$1.1M) y Umbrella $1M",
            action_plain=(
                "Timothy y Melanie confirman ambos (2/2) la emision final de los seguros de vida y Umbrella."
            ),
            action_math="savingsWaterfall #2 cierre de brecha -$2,100,000; combined_moves 60 -> 78.",
            estimated_minutes=10,
            ownership_mode="joint",
            waterfall_buckets=(2,),
            json_sources=("score.combined_moves[0]", "savingsWaterfall[2]"),
            inertia_lever_key="life_protection_gap",
        )
        self._add_step(
            steps,
            step_id="step_30_timothy_401k_and_roth",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30 — Owner A (Timothy): Subir 401(k) (+$10,500 margen) y abrir Roth IRA",
            action_plain=(
                "Timothy, sube tu aportacion 401(k) de $14,000 a $24,500 (+$10,500) y programa tu "
                "Roth IRA ($5,250) aprovechando el ahorro fiscal combinado de $5,760/ano."
            ),
            action_math=(
                f"savingsWaterfall #13 (Timothy +$10,500 -> $24,500; ahorro fiscal familiar "
                f"{_fmt_usd(k401['annual_cost_usd'])}/yr al 24%); #10 Roth IRA $5,250.10."
            ),
            estimated_minutes=10,
            ownership_mode="owner_a",
            waterfall_buckets=(10, 13),
            json_sources=("savingsWaterfall[10,13]", "persona.md: O7"),
            inertia_lever_key="401k_tax_delay",
        )
        self._add_step(
            steps,
            step_id="step_30_melanie_401k_and_529",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30 — Owner B (Melanie): Subir 401(k) (+$13,500 margen) y arrancar 529 ($4,609/ano)",
            action_plain=(
                "Melanie, sube tu 401(k) de $11,000 a $24,500 (+$13,500), aporta a Roth IRA ($5,250) "
                "y activa el 529 de Liam y Josh ($4,609/ano)."
            ),
            action_math=(
                "savingsWaterfall #13 (Melanie +$13,500 -> $24,500); #12 Contribute to 529 accounts "
                "$4,609.22/yr; #10 Roth IRA $5,250.10."
            ),
            estimated_minutes=10,
            ownership_mode="owner_b",
            waterfall_buckets=(10, 12, 13),
            json_sources=("savingsWaterfall[10,12,13]", "persona.md: O4, O7"),
            inertia_lever_key="401k_tax_delay",
        )

    def _build_johnson_steps(self, steps: list[IRLStep]) -> None:
        card = self.inertia_levers["high_apr_card"]
        k401 = self.inertia_levers["401k_tax_delay"]

        self._add_step(
            steps,
            step_id="step_0_joint_halt_diversion_and_quote",
            node_id="day_0",
            day=0,
            phase="day_0",
            title="Paso 1 (3 min) — Check conjunto (2/2): Frenar desvio a brokerage/529 y atacar 24.9% + seguro",
            action_plain=(
                "Daniel y Emily confirman juntos (2/2) pausar el envio a brokerage ($12,000/ano) y "
                "exceso de 529 para atacar hoy la Chase Sapphire al 24.9% ($12.28/dia) y pedir seguro de vida."
            ),
            action_math=(
                f"Joint 2/2: {_fmt_usd(card['annual_cost_usd'])}/yr ({_fmt_usd(card['daily_cost_usd'])}/day) "
                "en Chase Sapphire 24.9% + brecha -$2,350,000 vida (Protection 0/20); top_moves[0,2]."
            ),
            estimated_minutes=3,
            ownership_mode="joint",
            waterfall_buckets=(2, 8),
            json_sources=("profile.liabilities", "savingsWaterfall[2,8]", "persona.md: D5, T4"),
            inertia_lever_key="high_apr_card",
        )
        self._add_step(
            steps,
            step_id="step_3_daniel_attack_sapphire_card",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3 — Owner A (Daniel): Atacar Chase Sapphire ($18,000 al 24.9% APR)",
            action_plain=(
                "Daniel, ejecuta el primer abono extraordinario contra la Chase Sapphire ($18,000 al 24.9% APR) "
                "que hoy consume $373.50/mes en intereses ($4,482/ano)."
            ),
            action_math=(
                f"Owner A (Daniel) Chase Sapphire: {_fmt_usd(card['balance_usd'])} @ 24.9% APR = "
                f"{_fmt_usd(card['annual_cost_usd'])}/yr ({_fmt_usd(card['daily_cost_usd'])}/day); "
                "savingsWaterfall #8."
            ),
            estimated_minutes=10,
            ownership_mode="owner_a",
            waterfall_buckets=(8,),
            json_sources=("profile.liabilities[0]", "savingsWaterfall[8]"),
            inertia_lever_key="high_apr_card",
        )
        self._add_step(
            steps,
            step_id="step_3_emily_redirect_cashflow",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3 — Owner B (Emily): Redirigir $15,032/ano libres y ahorro a reserva de 3 meses",
            action_plain=(
                "Emily, redirige los $15,032/ano de flujo libre y el ahorro a brokerage ($12,000/ano) "
                "para subir vuestra caja de 1.4 meses ($19,000) hacia los 3 meses minimos ($40,073)."
            ),
            action_math=(
                "Owner B (Emily) accounts: savingsWaterfall #1 ($19,000 -> $40,073, delta -$21,072); "
                "top_moves[2]: Redirect $15,032/year (score 52 -> 55)."
            ),
            estimated_minutes=10,
            ownership_mode="owner_b",
            waterfall_buckets=(1, 3),
            json_sources=("savingsWaterfall[1]", "score.top_moves[2]", "profile.accounts"),
        )
        self._add_step(
            steps,
            step_id="step_3_joint_life_and_umbrella_quotes",
            node_id="day_3",
            day=3,
            phase="day_3",
            title="Dia 3 — Check conjunto (2/2): Pedir cotizacion seguro vida (+$1.166M / -$2.35M) y Umbrella $1M",
            action_plain=(
                "Daniel y Emily confirman ambos (2/2) las solicitudes de seguro de vida "
                "(Daniel -$1.35M, Emily -$1.00M) y Umbrella $1M para salir de Proteccion 0/20."
            ),
            action_math=(
                "combined_moves[0]: Raise mortality coverage (+$1,166,000 anchor toward -$2.35M gap) + "
                "Add umbrella cover ($1M) -> score 52 -> 60; Protection 0/20."
            ),
            estimated_minutes=15,
            ownership_mode="joint",
            waterfall_buckets=(2,),
            json_sources=("score.combined_moves[0]", "score.top_moves[0,1]", "persona.md: D3, O2, O3"),
            inertia_lever_key="life_protection_gap",
        )
        self._add_step(
            steps,
            step_id="step_14_joint_bind_life_umbrella",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14 — Check conjunto (2/2): Confirmar emision de vida (-$2.35M) y Umbrella $1M",
            action_plain=(
                "Daniel y Emily validan juntos (2/2) las polizas emitidas para dejar de acumular "
                "dias sin escudo familiar."
            ),
            action_math="savingsWaterfall #2: $450,000 -> $3,800,000 (delta -$3,350,000); score 52 -> 60.",
            estimated_minutes=10,
            ownership_mode="joint",
            waterfall_buckets=(2,),
            json_sources=("savingsWaterfall[2]", "score.combined_moves[0]"),
            inertia_lever_key="life_protection_gap",
        )
        self._add_step(
            steps,
            step_id="step_14_emily_review_tax_drag",
            node_id="day_14",
            day=14,
            phase="day_14",
            title="Dia 14 — Owner B (Emily): Revisar tax drag $658.65/ano y concentracion Tech (35.6%)",
            action_plain=(
                "Emily, revisa tu cuenta brokerage ($50,000 con JNK/SCHD/SCHP que generan $658.65/ano "
                "de impuestos) antes de aportar mas capital fuera del 401(k)."
            ),
            action_math=(
                "taxDragAnalysis: In-scope tax cost $658.65/yr (JNK $331.66 + SCHD $191.77 + SCHP $135.22); "
                "sectorConcentration Technology 35.63%."
            ),
            estimated_minutes=10,
            ownership_mode="owner_b",
            waterfall_buckets=(14,),
            json_sources=("taxDragAnalysis", "concentrationAndDiversification"),
            inertia_lever_key="tax_drag",
        )
        self._add_step(
            steps,
            step_id="step_30_daniel_activate_401k",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30 — Owner A (Daniel): Activar 401(k) desde $0 (match est. $6,400 + ahorro fiscal)",
            action_plain=(
                "Daniel, activa hoy tu 401(k) (hoy en $0) para capturar el match estimado ($6,400/ano) "
                "y sumar al ahorro fiscal potencial de $11,760/ano entre ambos."
            ),
            action_math=(
                f"savingsWaterfall #4 match est. $6,400 + #13 limite $24,500; entre ambos ($49,000 al 24%) "
                f"= {_fmt_usd(k401['annual_cost_usd'])}/yr de ahorro fiscal perdido mientras sigan en $0."
            ),
            estimated_minutes=10,
            ownership_mode="owner_a",
            waterfall_buckets=(4, 13),
            json_sources=("savingsWaterfall[4,13]", "persona.md: O1"),
            inertia_lever_key="401k_tax_delay",
        )
        self._add_step(
            steps,
            step_id="step_30_emily_activate_401k_and_rebalance_529",
            node_id="day_30",
            day=30,
            phase="day_30",
            title="Dia 30 — Owner B (Emily): Activar 401(k) desde $0 y ajustar 529 ($8,000 -> $1,928/ano)",
            action_plain=(
                "Emily, activa tu 401(k) (hoy $0, match est. $4,800/ano) y corrige la aportacion al 529 "
                "($8,000 actuales vs $1,928 recomendados) para priorizar tu propia jubilacion."
            ),
            action_math=(
                "savingsWaterfall #5 match est. $4,800 + #13 limite $24,500 + #12 529 $8,000 vs $1,928; "
                "persona.md T5 (mascarilla de oxigeno)."
            ),
            estimated_minutes=10,
            ownership_mode="owner_b",
            waterfall_buckets=(5, 12, 13),
            json_sources=("savingsWaterfall[5,12,13]", "persona.md: O1, T5"),
            inertia_lever_key="401k_tax_delay",
        )

    def _build_generic_steps(self, steps: list[IRLStep]) -> None:
        for idx, row in enumerate(self.waterfall_rows[:4]):
            day = _BASE_CHECKIN_DAYS[idx]
            mode = "joint" if self.is_couple else "single"
            self._add_step(
                steps,
                step_id=f"step_{day}_{row['bucket_number']}",
                node_id=f"day_{day}",
                day=day,
                phase=f"day_{day}",
                title=f"Dia {day}: {row['bucket']}",
                action_plain=f"Ejecutar paso #{row['bucket_number']}: {row['bucket']}.",
                action_math=f"savingsWaterfall[{row['bucket_number']}]: current={row['current']}, target={row['optimal_target']}.",
                estimated_minutes=3 if day == 0 else 10,
                ownership_mode=mode,
                waterfall_buckets=(int(row["bucket_number"]),) if isinstance(row["bucket_number"], int) else (),
                json_sources=("savingsWaterfall",),
            )

    def _append_real_milestones(self, steps: list[IRLStep]) -> None:
        """Append real milestone nodes from ``goals.chartGoals`` and ``persona.md`` Transition alerts."""
        seen_keys: set[tuple[str, str]] = set()
        goal_items: list[tuple[date, str, str, str, str]] = []

        # 1. Include short-term goals from investment-analysis cashNeeds (captures Ethan August 2027!)
        for stg in self.ia.get("key_metrics", {}).get("cashNeeds", {}).get("shortTermGoalsNeeded", []):
            d = _parse_iso_date(str(stg.get("date", "")))
            if d and d > self.start_date:
                name = str(stg.get("goal") or stg.get("description") or "Goal")
                amt = stg.get("amount")
                amt_txt = _fmt_usd(float(amt)) if isinstance(amt, (int, float)) else ""
                key = (d.isoformat(), name.lower())
                if key not in seen_keys:
                    seen_keys.add(key)
                    goal_items.append(
                        (
                            d,
                            name,
                            f"Hito real ({_month_year_label(d)}): {name} ({amt_txt})".strip(),
                            f"cashNeeds.shortTermGoalsNeeded: {name} {amt_txt} ({stg.get('paymentFrequency', '')})",
                            "cashNeeds.shortTermGoalsNeeded",
                        )
                    )

        # 2. Include goals.chartGoals from financial-health.json
        for cg in self.fh.get("goals", {}).get("chartGoals", []):
            d = _parse_iso_date(str(cg.get("date", "")))
            if not d or d <= self.start_date:
                continue
            goal_type = str(cg.get("goalType", "GOAL"))
            name = str(cg.get("name") or goal_type)
            key = (d.isoformat(), name.lower())
            if key in seen_keys:
                continue
            seen_keys.add(key)

            plain, math_txt = self._describe_chart_goal(d, goal_type, name)
            goal_items.append((d, name, plain, math_txt, "goals.chartGoals"))

        # Deduplicate near-identical dates if vacation already represented, keep chronological order
        mode = "joint" if self.is_couple else "single"
        for idx, (m_date, name, plain, math_txt, src) in enumerate(sorted(goal_items, key=lambda x: x[0])):
            day_offset = (m_date - self.start_date).days
            slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or f"goal_{idx}"
            node_id = f"milestone_{m_date.strftime('%Y_%m')}_{slug}"
            self._add_step(
                steps,
                step_id=f"step_{node_id}",
                node_id=node_id,
                day=day_offset,
                phase="milestone",
                title=f"Hito {_month_year_label(m_date)}: {name}",
                action_plain=plain,
                action_math=math_txt,
                estimated_minutes=15,
                ownership_mode=mode,
                json_sources=(src, "persona.md: Transition alerts"),
            )

    def _describe_chart_goal(self, m_date: date, goal_type: str, name: str) -> tuple[str, str]:
        label = _month_year_label(m_date)
        yearly = {r.get("year"): r for r in self.fh.get("projections", {}).get("yearly", [])}
        yr_row = yearly.get(m_date.year, {})
        inv_assets = yr_row.get("investable_assets")

        if goal_type == "PURCHASE" and "home" in name.lower():
            for g in self.fh.get("profile", {}).get("goals", []):
                if g.get("type") == "REAL_ESTATE_PURCHASE":
                    amt = float(g.get("amount", 0))
                    loan = g.get("planned_loan", {})
                    pmt = float(loan.get("monthly_payment", 0))
                    down = next(
                        (float(c["yearly"]) for c in g.get("yearly_costs", []) if "downpayment" in c.get("name", "").lower()),
                        0.0,
                    )
                    closing = next(
                        (float(c["yearly"]) for c in g.get("yearly_costs", []) if "closing" in c.get("name", "").lower()),
                        0.0,
                    )
                    plain = (
                        f"Decision de compra de vivienda en {label} ({_fmt_usd(amt)}): "
                        f"entrada {_fmt_usd(down)}, cierre {_fmt_usd(closing)}, hipoteca {_fmt_usd(pmt)}/mes."
                    )
                    math_txt = (
                        f"chartGoals + profile.goals: {_fmt_usd(amt)} ({label}); "
                        f"investable_assets {m_date.year}: {_fmt_usd(inv_assets) if inv_assets is not None else 'N/A'}."
                    )
                    return plain, math_txt

        if goal_type in ("BANKRUPTCY_ZEROCASH", "BANKRUPTCY"):
            age = yr_row.get("age_client")
            plain = (
                f"Alerta estructural de trayectoria en {label} (edad {age}): "
                f"sin ejecutar las palancas del plan, los activos liquidos caen a {_fmt_usd(float(inv_assets or 0))}."
            )
            math_txt = (
                f"goals.chartGoals ({goal_type}) + projections.yearly[{m_date.year}]: "
                f"investable_assets={_fmt_usd(float(inv_assets or 0))}, net_worth={_fmt_usd(float(yr_row.get('net_worth', 0)))}."
            )
            return plain, math_txt

        return (
            f"Revision de hito real en {label}: {name}.",
            f"goals.chartGoals ({goal_type}) -> {m_date.isoformat()}",
        )

    def _normalize_member(self, step: IRLStep, member: str | None) -> str:
        if not self.is_couple:
            if member is None or member.lower() in ("single", "client", "a", self.member_names["single"].lower()):
                return "single"
            raise ValueError(f"Miembro '{member}' invalido para hogar individual '{self.case_id}'.")

        a_first = self.member_names["A_first"].lower()
        b_first = self.member_names["B_first"].lower()
        if member is None:
            if step.ownership_mode in ("owner_a", "owner_b"):
                return step.required_members[0]
            raise ValueError(
                f"El paso conjunto '{step.step_id}' requiere especificar member='A' ({a_first}) o member='B' ({b_first})."
            )

        norm = member.strip().lower()
        if norm in ("a", "owner_a", "owner a", "client", a_first):
            resolved = "A"
        elif norm in ("b", "owner_b", "owner b", "co-client", "co_client", b_first):
            resolved = "B"
        else:
            raise ValueError(f"Miembro '{member}' no reconocido para pareja '{self.case_id}'.")

        if resolved not in step.required_members:
            raise ValueError(
                f"El paso '{step.step_id}' pertenece a '{step.owner_label}', no a '{member}'."
            )
        return resolved

    def check_step(
        self,
        step_id: str,
        *,
        member: str | None = None,
        completed_day: int | None = None,
    ) -> dict[str, Any]:
        """Mark a step (or one partner's half of a 2/2 joint step) as completed."""
        step = self._steps_by_id.get(step_id)
        if step is None:
            raise KeyError(f"Paso desconocido: '{step_id}'")
        resolved = self._normalize_member(step, member)
        day_val = self.current_day if completed_day is None else int(completed_day)
        step.completed_by[resolved] = day_val
        return step.to_dict(
            self.current_day,
            self.member_names,
            step_inertia=self._step_inertia_snapshot(step, self.current_day),
        )

    def uncheck_step(self, step_id: str, *, member: str | None = None) -> dict[str, Any]:
        """Revert completion on a step (or one partner's check on a joint step)."""
        step = self._steps_by_id.get(step_id)
        if step is None:
            raise KeyError(f"Paso desconocido: '{step_id}'")
        if member is None and step.ownership_mode == "joint":
            step.completed_by.clear()
        else:
            resolved = self._normalize_member(step, member)
            step.completed_by.pop(resolved, None)
        return step.to_dict(
            self.current_day,
            self.member_names,
            step_inertia=self._step_inertia_snapshot(step, self.current_day),
        )

    def _is_lever_resolved(self, lever_key: str) -> bool:
        linked = [s for s in self.steps if s.inertia_lever_key == lever_key]
        if not linked:
            return False
        if lever_key == "high_apr_card":
            settlement_steps = [s for s in linked if s.day <= 3]
            if not settlement_steps:
                return all(s.is_completed for s in linked)
            final_settlement_day = max(s.day for s in settlement_steps)
            return all(s.is_completed for s in settlement_steps if s.day == final_settlement_day)
        if lever_key == "unconfirmed_property_policy":
            return all(s.is_completed for s in linked if s.day <= 3)
        return all(s.is_completed for s in linked)

    def _step_inertia_snapshot(self, step: IRLStep, current_day: int) -> dict[str, Any]:
        if step.is_completed or not step.inertia_lever_key:
            return {"daily_cost_usd": 0.0, "accrued_cost_usd": 0.0, "days_overdue": 0}
        lever = self.inertia_levers.get(step.inertia_lever_key)
        if not lever:
            return {"daily_cost_usd": 0.0, "accrued_cost_usd": 0.0, "days_overdue": 0}
        days_overdue = max(0, current_day - step.day)
        daily = float(lever.get("daily_cost_usd", 0.0))
        return {
            "lever_key": lever["key"],
            "label": lever["label"],
            "annual_cost_usd": float(lever.get("annual_cost_usd", 0.0)),
            "daily_cost_usd": daily,
            "days_overdue": days_overdue,
            "accrued_cost_usd": round(daily * days_overdue, 2),
            "tracks_days_uninsured": bool(lever.get("tracks_days_uninsured", False)),
            "shortfall_usd": float(lever.get("shortfall_usd", 0.0)),
        }

    def compute_inertia_cost(self, current_day: int | None = None) -> dict[str, Any]:
        """Calculate real ongoing and overdue inertia cost at ``current_day``."""
        day = self.current_day if current_day is None else int(current_day)
        active_components: list[dict[str, Any]] = []
        total_daily = 0.0
        total_annual = 0.0
        total_accrued_since_day0 = 0.0
        total_overdue_accrued = 0.0
        max_days_uninsured = 0

        for lever_key, lever in self.inertia_levers.items():
            if self._is_lever_resolved(lever_key):
                continue
            linked = [s for s in self.steps if s.inertia_lever_key == lever_key]
            earliest_day = min((s.day for s in linked), default=0)
            overdue_days = max(0, day - earliest_day)
            elapsed_days = max(0, day)
            daily = float(lever.get("daily_cost_usd", 0.0))
            annual = float(lever.get("annual_cost_usd", 0.0))

            if lever.get("tracks_days_uninsured"):
                max_days_uninsured = max(max_days_uninsured, elapsed_days)

            accrued_since_day0 = round(daily * elapsed_days, 2)
            accrued_overdue = round(daily * overdue_days, 2)
            total_daily += daily
            total_annual += annual
            total_accrued_since_day0 += accrued_since_day0
            total_overdue_accrued += accrued_overdue

            item = dict(lever)
            item["days_elapsed"] = elapsed_days
            item["days_overdue"] = overdue_days
            item["accrued_since_day0_usd"] = accrued_since_day0
            item["accrued_overdue_usd"] = accrued_overdue
            active_components.append(item)

        return {
            "case_id": self.case_id,
            "current_day": day,
            "daily_cost_usd": round(total_daily, 2),
            "annual_cost_usd": round(total_annual, 2),
            "accrued_since_day0_usd": round(total_accrued_since_day0, 2),
            "accrued_overdue_usd": round(total_overdue_accrued, 2),
            "days_uninsured": max_days_uninsured,
            "active_levers": active_components,
        }

    def advance_day(self, current_day: int) -> dict[str, Any]:
        """Advance Run IRL clock relentlessly to ``current_day`` and carry over overdue steps."""
        if current_day < 0:
            raise ValueError("current_day debe ser >= 0")
        self.current_day = int(current_day)
        return self.get_timeline_view(self.current_day)

    def _node_days(self) -> list[int]:
        return sorted({s.day for s in self.steps})

    def _node_label(self, day: int) -> str:
        if day in (0, 3, 14, 30):
            return f"Dia {day}"
        d = self.start_date + timedelta(days=day)
        return f"Hito {_month_year_label(d)}"

    def get_timeline_view(self, current_day: int | None = None) -> dict[str, Any]:
        """Return bidirectional timeline view at ``current_day`` without losing state."""
        day = self.current_day if current_day is None else int(current_day)
        node_days = self._node_days()
        inertia = self.compute_inertia_cost(day)

        step_dicts = [
            s.to_dict(day, self.member_names, step_inertia=self._step_inertia_snapshot(s, day))
            for s in self.steps
        ]
        overdue_steps = [s for s in step_dicts if s["status"] == "overdue"]
        active_steps = [s for s in step_dicts if s["status"] == "active"]
        completed_steps = [s for s in step_dicts if s["status"] == "completed"]
        upcoming_steps = [s for s in step_dicts if s["status"] == "upcoming"]

        nodes: list[dict[str, Any]] = []
        for nd in node_days:
            nd_steps = [s for s in step_dicts if s["day"] == nd]
            nd_date = self.start_date + timedelta(days=nd)
            carried = overdue_steps if nd == day else []
            nodes.append(
                {
                    "node_id": nd_steps[0]["node_id"] if nd_steps else f"day_{nd}",
                    "day": nd,
                    "date": nd_date.isoformat(),
                    "label": self._node_label(nd),
                    "is_current": nd == day,
                    "is_past": nd < day,
                    "is_future": nd > day,
                    "steps": nd_steps,
                    "carried_overdue_steps": carried,
                }
            )

        prev_days = [d for d in node_days if d < day]
        next_days = [d for d in node_days if d > day]
        active_node_day = max((d for d in node_days if d <= day), default=0)

        return {
            "case_id": self.case_id,
            "is_couple": self.is_couple,
            "members": self.member_names,
            "start_date": self.start_date.isoformat(),
            "current_day": day,
            "current_date": (self.start_date + timedelta(days=day)).isoformat(),
            "active_node_day": active_node_day,
            "active_node_label": self._node_label(active_node_day),
            "nodes": nodes,
            "overdue_steps": overdue_steps,
            "active_steps": active_steps,
            "completed_steps": completed_steps,
            "upcoming_steps": upcoming_steps,
            "inertia_cost": inertia,
            "navigation": {
                "node_days": node_days,
                "can_go_prev": bool(prev_days),
                "can_go_next": bool(next_days),
                "prev_node_day": prev_days[-1] if prev_days else None,
                "next_node_day": next_days[0] if next_days else None,
            },
        }

    def get_focus_mode_view(self, current_day: int | None = None) -> dict[str, Any]:
        """Return *Modo Enfoque* exposing only the single immediate next IRL action."""
        day = self.current_day if current_day is None else int(current_day)
        self.active_view = "focus_mode"
        due_or_overdue = [
            s for s in self.steps if s.day <= day and not s.is_completed
        ]
        # Priority: overdue steps oldest first, then current-day steps.
        due_or_overdue.sort(key=lambda s: (0 if s.day < day else 1, s.day, s.step_id))

        if due_or_overdue:
            primary = due_or_overdue[0]
            focus_step = primary.to_dict(
                day,
                self.member_names,
                step_inertia=self._step_inertia_snapshot(primary, day),
            )
            all_due_completed = False
        else:
            upcoming = [s for s in self.steps if s.day > day and not s.is_completed]
            focus_step = (
                upcoming[0].to_dict(day, self.member_names)
                if upcoming
                else None
            )
            all_due_completed = True

        by_owner: dict[str, Any] = {}
        if self.is_couple:
            a_pending = [
                s.to_dict(day, self.member_names, self._step_inertia_snapshot(s, day))
                for s in due_or_overdue
                if "A" in s.missing_members
            ]
            b_pending = [
                s.to_dict(day, self.member_names, self._step_inertia_snapshot(s, day))
                for s in due_or_overdue
                if "B" in s.missing_members
            ]
            by_owner = {
                "owner_a": {
                    "label": self.member_names["A"],
                    "next_step": a_pending[0] if a_pending else None,
                    "pending_count": len(a_pending),
                },
                "owner_b": {
                    "label": self.member_names["B"],
                    "next_step": b_pending[0] if b_pending else None,
                    "pending_count": len(b_pending),
                },
            }

        return {
            "case_id": self.case_id,
            "mode": "focus_mode",
            "active_view": self.active_view,
            "current_day": day,
            "current_camp_label": self._node_label(max((d for d in self._node_days() if d <= day), default=0)),
            "focus_step": focus_step,
            "all_due_steps_completed": all_due_completed,
            "overdue_count": sum(1 for s in due_or_overdue if s.day < day),
            "pending_due_count": len(due_or_overdue),
            "by_owner": by_owner,
            "inertia_snapshot": self.compute_inertia_cost(day),
            "available_actions": {
                "view_mountain_overview": "get_mountain_overview",
                "repeat_expedition": "repeat_expedition",
                "export_ics": "export_ics",
            },
        }

    # Alias for callers expecting ``focus_step`` method name
    def focus_step(self, current_day: int | None = None) -> dict[str, Any]:
        """Alias of :meth:`get_focus_mode_view`."""
        return self.get_focus_mode_view(current_day=current_day)

    def get_mountain_overview(self) -> dict[str, Any]:
        """Return resolved mountain overview (good summit path + failed branches) WITHOUT resetting IRL."""
        self.active_view = "mountain_overview"
        score_obj = self.fh.get("score", {})
        published = score_obj.get("published_score")
        combined = score_obj.get("combined_moves", [])
        top_moves = score_obj.get("top_moves", [])
        best_after = max(
            [published or 0]
            + [m.get("score_after", 0) for m in top_moves]
            + [c.get("score_after", 0) for c in combined]
        )

        yearly = self.fh.get("projections", {}).get("yearly", [])
        key_years = [2026, 2027, 2030, 2044, 2047, 2048, 2053, 2070, 2075]
        trajectory = [
            {
                "year": r.get("year"),
                "age_client": r.get("age_client"),
                "investable_assets": r.get("investable_assets"),
                "net_worth": r.get("net_worth"),
                "total_debts": r.get("total_debts"),
            }
            for r in yearly
            if r.get("year") in key_years or r.get("investable_assets", 0) < 0
        ]

        failed_branches: list[dict[str, Any]] = []
        neg_row = next((r for r in yearly if r.get("investable_assets", 0) < 0), None)
        if neg_row is not None:
            failed_branches.append(
                {
                    "branch_type": "crevasse_liquidity_depletion",
                    "year": neg_row["year"],
                    "age_client": neg_row.get("age_client"),
                    "investable_assets": neg_row["investable_assets"],
                    "net_worth": neg_row.get("net_worth"),
                    "summary": (
                        f"Grieta {neg_row['year']} (edad {neg_row.get('age_client')}): "
                        f"activos liquidos {_fmt_usd(neg_row['investable_assets'])} "
                        f"(net worth {_fmt_usd(neg_row.get('net_worth', 0))})."
                    ),
                }
            )
        for lever_key in ("high_apr_card", "life_protection_gap", "unconfirmed_property_policy", "tax_drag"):
            if lever_key in self.inertia_levers:
                lv = self.inertia_levers[lever_key]
                failed_branches.append(
                    {
                        "branch_type": "inertia_wall",
                        "lever_key": lever_key,
                        "summary": lv["label"],
                        "source": lv["source"],
                    }
                )

        return {
            "case_id": self.case_id,
            "mode": "mountain_overview",
            "active_view": self.active_view,
            "irl_progress_preserved": True,
            "expedition_reset": False,
            "simulation_run_count": self.simulation_run_count,
            "simulation_completed": self.simulation_completed,
            "irl_completed_steps": sum(1 for s in self.steps if s.is_completed),
            "irl_current_day": self.current_day,
            "good_path": {
                "score_before": published,
                "score_after_optimal": best_after,
                "chosen_moves": self.simulation_choices,
                "combined_moves": combined,
            },
            "failed_branches": failed_branches,
            "yearly_checkpoints": trajectory[:15],
        }

    def repeat_expedition(self, *, reset_irl: bool = False) -> dict[str, Any]:
        """Explicitly restart the simulated mountain expedition without accidentally wiping IRL progress."""
        self.simulation_run_count += 1
        self.simulation_completed = False
        self.simulation_choices = []
        self.active_view = "expedition_replay"
        if reset_irl:
            self.current_day = 0
            for step in self.steps:
                step.completed_by.clear()
        return {
            "case_id": self.case_id,
            "mode": "expedition_replay",
            "active_view": self.active_view,
            "expedition_reset": True,
            "irl_reset": reset_irl,
            "simulation_run_count": self.simulation_run_count,
            "simulation_completed": self.simulation_completed,
            "irl_completed_steps": sum(1 for s in self.steps if s.is_completed),
            "irl_current_day": self.current_day,
        }

    def reset_expedition(self, *, reset_irl: bool = False) -> dict[str, Any]:
        """Alias of :meth:`repeat_expedition`."""
        return self.repeat_expedition(reset_irl=reset_irl)

    def export_ics(self, start_date: date | None = None) -> str:
        """Export Run IRL check-ins and real case milestones as an RFC 5545 ``.ics`` calendar."""
        base_date = start_date or self.start_date
        now_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        def _ics_escape(text: str) -> str:
            return (
                text.replace("\\", "\\\\")
                .replace(";", "\\;")
                .replace(",", "\\,")
                .replace("\n", "\\n")
            )

        lines: list[str] = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Sherpas//Run IRL Radio del Sherpa//ES",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
        ]

        for step in self.steps:
            event_date = base_date + timedelta(days=step.day)
            end_date = event_date + timedelta(days=1)
            uid = f"{self.case_id}-{step.step_id}-{event_date.strftime('%Y%m%d')}@sherpas.irl"
            summary = f"[Sherpas IRL · {step.owner_label}] {step.title}"
            desc = f"{step.action_plain}\nDatos: {step.action_math}\nEstado: {step.completion_ratio}"
            lines.extend(
                [
                    "BEGIN:VEVENT",
                    f"UID:{uid}",
                    f"DTSTAMP:{now_stamp}",
                    f"DTSTART;VALUE=DATE:{event_date.strftime('%Y%m%d')}",
                    f"DTEND;VALUE=DATE:{end_date.strftime('%Y%m%d')}",
                    f"SUMMARY:{_ics_escape(summary)}",
                    f"DESCRIPTION:{_ics_escape(desc)}",
                    f"CATEGORIES:{'MILESTONE' if step.phase == 'milestone' else 'RUN_IRL'}",
                    "END:VEVENT",
                ]
            )

        lines.append("END:VCALENDAR")
        return "\r\n".join(lines) + "\r\n"


def create_irl_run(
    case_id: str,
    *,
    cases_dir: str | Path | None = None,
    start_date: date | None = None,
) -> IRLEngine:
    """Factory creating an :class:`IRLEngine` instance for a real case."""
    return IRLEngine(case_id, cases_dir=cases_dir, start_date=start_date)
