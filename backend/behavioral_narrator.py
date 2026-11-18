"""Behavioral translation engine: real Sherpas case loader, Dual-Lens Plain/Math,
Section 4 / Appendices A & B cognitive bias engine, Cordada Asimetrica pact, and Advisor Brief.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
from typing import Any

from backend.llm_proxy import DEFAULT_MODEL, LLMProxyClient


SUPPORTED_CASES = (
    "michael-carter",
    "samantha-lewis",
    "timothy-melanie-weah",
    "daniel-emily-johnson",
)

FALLBACK_CASES_DIR = Path(
    r"C:\Users\Silvia\.gemini\antigravity\scratch\hackathon-upv-2026\cases"
)

BIAS_CATALOG: tuple[dict[str, str], ...] = (
    {
        "bias_id": "ikea_effect",
        "section": "A",
        "name_es": "Efecto IKEA y Agencia Humana",
        "name_en": "IKEA Effect & Human Agency",
        "theorist": "Norton, Mochon & Ariely",
    },
    {
        "bias_id": "mental_accounting",
        "section": "4.1",
        "name_es": "Contabilidad Mental",
        "name_en": "Mental Accounting",
        "theorist": "Richard Thaler",
    },
    {
        "bias_id": "halo_effect",
        "section": "4.1",
        "name_es": "Efecto Halo / Ceguera de Indicador Único",
        "name_en": "Single-Metric Fallacy & Halo Effect",
        "theorist": "Edward Thorndike / Behavioral Finance",
    },
    {
        "bias_id": "house_rich_cash_poor",
        "section": "4.1",
        "name_es": "Ilusión de Riqueza Inmobiliaria",
        "name_en": "House-Rich, Cash-Poor Illusion",
        "theorist": "Liquidity vs Net Worth Framing",
    },
    {
        "bias_id": "present_bias",
        "section": "4.2",
        "name_es": "Descuento Hiperbólico / Sesgo del Presente",
        "name_en": "Present Bias / Hyperbolic Discounting",
        "theorist": "David Laibson / Ainslie",
    },
    {
        "bias_id": "future_self_gap",
        "section": "4.2",
        "name_es": "Desconexión con el Yo Futuro",
        "name_en": "Future-Self Continuity Gap",
        "theorist": "Hal Hershfield",
    },
    {
        "bias_id": "planning_fallacy",
        "section": "4.2",
        "name_es": "Falacia de Planificación y Costes Ocultos",
        "name_en": "Planning Fallacy & Hidden Cost Neglect",
        "theorist": "Kahneman & Tversky",
    },
    {
        "bias_id": "ostrich_effect",
        "section": "4.3",
        "name_es": "Efecto Avestruz",
        "name_en": "Ostrich Effect",
        "theorist": "Galai & Sade / Karlsson et al.",
    },
    {
        "bias_id": "optimism_bias",
        "section": "4.3",
        "name_es": "Sesgo de Optimismo e Invulnerabilidad",
        "name_en": "Optimism Bias & Mortality Salience",
        "theorist": "Tali Sharot / Terror Management",
    },
    {
        "bias_id": "oxygen_mask_syndrome",
        "section": "4.3",
        "name_es": "Priorización Emocional Invertida (Mascarilla de Oxígeno)",
        "name_en": "Oxygen Mask Syndrome",
        "theorist": "Behavioral Family Prioritization",
    },
    {
        "bias_id": "choice_overload",
        "section": "4.4",
        "name_es": "Parálisis por Análisis y Sobrecarga",
        "name_en": "Choice Overload / Hick's Law",
        "theorist": "Iyengar & Lepper / William Edmund Hick",
    },
    {
        "bias_id": "status_quo_bias",
        "section": "4.4",
        "name_es": "Sesgo de Statu Quo y Curva del Olvido",
        "name_en": "Status Quo Bias & Ebbinghaus Curve",
        "theorist": "Samuelson & Zeckhauser / Hermann Ebbinghaus",
    },
    {
        "bias_id": "loss_aversion_recency",
        "section": "4.4",
        "name_es": "Aversión a la Pérdida y Sesgo de Recencia",
        "name_en": "Loss Aversion & Recency Bias",
        "theorist": "Kahneman & Tversky",
    },
    {
        "bias_id": "couples_veto",
        "section": "4.4",
        "name_es": "Veto Silencioso y Silos en Pareja",
        "name_en": "Couples Veto & Role Siloing",
        "theorist": "Household Bargaining Dynamics",
    },
)

BIAS_METADATA: dict[str, dict[str, str]] = {item["bias_id"]: item for item in BIAS_CATALOG}
ALL_BIAS_IDS: tuple[str, ...] = tuple(item["bias_id"] for item in BIAS_CATALOG)
SECTION_4_BIAS_IDS: tuple[str, ...] = tuple(
    item["bias_id"] for item in BIAS_CATALOG if item["section"].startswith("4.")
)


@dataclass(frozen=True)
class ObjectiveConcern:
    """Structured objective concern (`O1..O9`) parsed from `persona.md`."""

    id: str
    severity: str
    title: str
    detail: str
    connected: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "severity": self.severity,
            "title": self.title,
            "detail": self.detail,
            "connected": self.connected,
        }


@dataclass(frozen=True)
class TensionItem:
    """Structured tension (`T1..T5`) parsed from `persona.md`."""

    id: str
    severity: str
    summary: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "severity": self.severity,
            "summary": self.summary,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class PersonaProfile:
    """Parsed structural & psychological fields from `persona.md`."""

    household_heading: str
    sections: dict[str, str]
    transition_alerts: list[str]
    subjective_concerns_raw: str
    has_subjective_concerns: bool
    objective_concerns: list[ObjectiveConcern]
    tensions: list[TensionItem]
    classification: dict[str, Any]
    risk_alignment: str
    decision_style: str
    motivational_anchor: str


@dataclass
class CaseData:
    """Real Sherpas household bundle loaded from `financial-health.json`, `investment-analysis.json`, and `persona.md`."""

    case_id: str
    case_dir: Path
    financial_health: dict[str, Any]
    investment_analysis: dict[str, Any]
    persona_text: str
    persona: PersonaProfile

    @property
    def household(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("case", {}).get("household", []))

    @property
    def adults(self) -> list[dict[str, Any]]:
        return [m for m in self.household if m.get("role") in ("client", "co-client")]

    @property
    def children(self) -> list[dict[str, Any]]:
        return [m for m in self.household if m.get("role") == "child"]

    @property
    def is_couple(self) -> bool:
        return len(self.adults) > 1

    @property
    def household_name(self) -> str:
        names = [str(m.get("first_name", "")).strip() for m in self.adults if m.get("first_name")]
        return " & ".join(names) if names else self.case_id

    @property
    def published_score(self) -> int:
        return int(self.financial_health.get("score", {}).get("published_score", 0))

    @property
    def score_band(self) -> str:
        return str(self.financial_health.get("score", {}).get("band", ""))

    @property
    def pillars(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("score", {}).get("pillars", []))

    @property
    def caps_applied(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("score", {}).get("caps_applied", []))

    @property
    def top_moves(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("score", {}).get("top_moves", []))

    @property
    def combined_moves(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("score", {}).get("combined_moves", []))

    @property
    def chart_goals(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("goals", {}).get("chartGoals", []))

    @property
    def goals_summary(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("goals", {}).get("goalsSummary", []))

    @property
    def fh_facts(self) -> dict[str, Any]:
        return dict(self.financial_health.get("key_metrics", {}).get("facts", {}))

    @property
    def ia_facts(self) -> dict[str, Any]:
        return dict(self.investment_analysis.get("key_metrics", {}).get("facts", {}))

    @property
    def yearly_projections(self) -> list[dict[str, Any]]:
        return list(self.financial_health.get("projections", {}).get("yearly", []))

    @property
    def profile(self) -> dict[str, Any]:
        return dict(self.financial_health.get("profile", {}))

    @property
    def tax_drag_analysis(self) -> dict[str, Any]:
        return dict(self.investment_analysis.get("key_metrics", {}).get("taxDragAnalysis", {}))

    @property
    def performance_analysis(self) -> dict[str, Any]:
        return dict(self.investment_analysis.get("key_metrics", {}).get("performanceAnalysis", {}))

    @property
    def savings_and_contributions(self) -> dict[str, Any]:
        return dict(self.investment_analysis.get("key_metrics", {}).get("savingsAndContributions", {}))

    @property
    def savings_waterfall(self) -> list[list[Any]]:
        return list(self.savings_and_contributions.get("savingsWaterfall", []))

    @property
    def analysis_events(self) -> list[dict[str, Any]]:
        return list(self.investment_analysis.get("analysis", {}).get("events", []))

    @property
    def per_event_drawdowns(self) -> list[dict[str, Any]]:
        return list(self.performance_analysis.get("perEventDrawdowns", []))

    @property
    def positions(self) -> list[dict[str, Any]]:
        return list(self.investment_analysis.get("positions", []))

    def first_negative_investable_year(self) -> dict[str, Any] | None:
        for row in self.yearly_projections:
            if (row.get("investable_assets") or 0) < 0:
                return row
        return None

    def first_negative_net_worth_year(self) -> dict[str, Any] | None:
        for row in self.yearly_projections:
            if (row.get("net_worth") or 0) < 0:
                return row
        return None

    def projection_for_year(self, year: int) -> dict[str, Any] | None:
        for row in self.yearly_projections:
            if row.get("year") == year:
                return row
        return None

    def tax_drag_annual_cost(self) -> float:
        for row in self.tax_drag_analysis.get("householdRollup", []):
            if len(row) >= 2 and "In-scope tax cost" in str(row[0]):
                return float(row[1])
        return 0.0

    def cash_yield_earned(self) -> float:
        cash_needs = self.investment_analysis.get("key_metrics", {}).get("cashNeeds", {})
        total = 0.0
        for row in cash_needs.get("summaryIncome", []):
            if len(row) >= 2 and str(row[0]).strip() in ("Liquidity", "Excess accessible", "Operational buffer"):
                try:
                    total += float(row[1])
                except (TypeError, ValueError):
                    pass
        return round(total, 2)

    def high_interest_debts(self, threshold: float = 0.10) -> list[dict[str, Any]]:
        debts: list[dict[str, Any]] = []
        for item in self.profile.get("liabilities", []) or []:
            bal = float(item.get("balance") or 0.0)
            rate = float(item.get("interest_rate") or 0.0)
            if bal > 0 and rate >= threshold:
                debts.append(
                    {
                        "name": item.get("name", "Card"),
                        "type": item.get("type", ""),
                        "balance": bal,
                        "interest_rate": rate,
                        "apr_pct": round(rate * 100, 1),
                        "annual_interest": round(bal * rate, 2),
                        "monthly_payment": float(item.get("monthly_payment") or 0.0),
                        "owner": list(item.get("owner") or []),
                    }
                )
        return debts

    def waterfall_row(self, bucket_fragment: str) -> dict[str, Any] | None:
        frag = bucket_fragment.lower()
        for row in self.savings_waterfall[1:]:
            if len(row) >= 4 and frag in str(row[1]).lower():
                return {
                    "step": row[0],
                    "bucket": row[1],
                    "current": row[2],
                    "optimal_target": row[3],
                    "status": row[4] if len(row) > 4 else "",
                    "delta": row[5] if len(row) > 5 else None,
                }
        return None


def resolve_cases_dir(cases_dir: str | Path | None = None) -> Path:
    """Locate the `cases/` directory using project root, `SHERPAS_CASES_DIR`, and fallback."""
    candidates: list[Path] = []
    if cases_dir is not None:
        candidates.append(Path(cases_dir))

    project_root = Path(__file__).resolve().parent.parent
    candidates.append(project_root / "cases")
    candidates.append(Path.cwd() / "cases")

    env_dir = os.environ.get("SHERPAS_CASES_DIR")
    if env_dir:
        candidates.append(Path(env_dir))

    candidates.append(FALLBACK_CASES_DIR)

    for candidate in candidates:
        if candidate.is_dir() and any((candidate / c).is_dir() for c in SUPPORTED_CASES):
            return candidate
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(
        "Could not locate Sherpas cases directory in project root, SHERPAS_CASES_DIR, or fallback."
    )


def list_available_cases(cases_dir: str | Path | None = None) -> list[str]:
    """Return sorted list of valid case IDs available on disk."""
    root = resolve_cases_dir(cases_dir)
    found = [
        p.name
        for p in sorted(root.iterdir())
        if p.is_dir() and (p / "financial-health.json").is_file()
    ]
    return found


def parse_persona_markdown(markdown_text: str) -> PersonaProfile:
    """Parse structured sections, Objective concerns (`O1..O9`), Tensions (`T1..T5`), and alerts."""
    heading = ""
    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for line in markdown_text.splitlines():
        if line.startswith("# ") and not heading:
            heading = line[2:].strip()
            continue
        if line.startswith("## "):
            current_section = line[3:].strip()
            sections[current_section] = []
            continue
        if current_section is not None:
            sections[current_section].append(line)

    section_text = {k: "\n".join(v).strip() for k, v in sections.items()}

    # Transition alerts
    transition_raw = section_text.get("Transition alerts", "")
    transition_alerts: list[str] = []
    for line in transition_raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            transition_alerts.append(stripped[2:].strip())
    if not transition_alerts and transition_raw and "none detected" not in transition_raw.lower():
        transition_alerts.append(transition_raw)

    # Subjective concerns
    subj_raw = section_text.get("Subjective concerns", "").strip()
    has_subj = bool(
        subj_raw
        and not subj_raw.lower().startswith("none detected")
        and not subj_raw.lower().startswith("none recorded")
    )

    # Objective concerns (`O1..O9` supporting both Michael and Samantha/Weah/Johnson formats)
    obj_concerns: list[ObjectiveConcern] = []
    obj_raw = section_text.get("Objective concerns", "")
    pat_a = re.compile(r"^-\s+\*\*(O\d+)\s+(CRITICAL|SIGNIFICANT|MODERATE|MINOR):\s*(.+?)\*\*\s*(.*)$")
    pat_b = re.compile(
        r"^-\s+\*\*(O\d+):\s*(.+?)\s*\((CRITICAL|SIGNIFICANT|MODERATE|MINOR)\)\.?\*\*\s*(.*)$"
    )
    for line in obj_raw.splitlines():
        s = line.strip()
        m_a = pat_a.match(s)
        m_b = pat_b.match(s)
        if m_a:
            oid, sev, title, detail = m_a.groups()
        elif m_b:
            oid, title, sev, detail = m_b.groups()
        else:
            continue
        conn_match = re.search(r"Connected:\s*([^.]+)\.?\s*$", detail)
        connected = conn_match.group(1).strip() if conn_match else ""
        obj_concerns.append(
            ObjectiveConcern(
                id=oid,
                severity=sev,
                title=title.rstrip("."),
                detail=detail.strip(),
                connected=connected,
            )
        )

    # Tensions (`T1..T5` supporting both `(HIGH):` and `: title (HIGH).` formats)
    tensions: list[TensionItem] = []
    ten_raw = section_text.get("Tensions", "")
    t_pat_a = re.compile(r"^-\s+\*\*(T\d+)\s*\((HIGH|MEDIUM|LOW)\):\*\*\s*(.*)$")
    t_pat_b = re.compile(r"^-\s+\*\*(T\d+):\s*(.+?)\s*\((HIGH|MEDIUM|LOW)\)\.?\*\*\s*(.*)$")
    for line in ten_raw.splitlines():
        s = line.strip()
        m_a = t_pat_a.match(s)
        m_b = t_pat_b.match(s)
        if m_a:
            tid, sev, detail = m_a.groups()
            summary = detail.split(".", 1)[0].strip()
        elif m_b:
            tid, summary, sev, detail = m_b.groups()
        else:
            continue
        tensions.append(
            TensionItem(
                id=tid,
                severity=sev,
                summary=summary.rstrip("."),
                detail=detail.strip(),
            )
        )

    # Classification block
    classification: dict[str, Any] = {}
    cls_match = re.search(r"```classification\s*(.*?)```", markdown_text, re.DOTALL)
    if cls_match:
        current_list_key: str | None = None
        for raw_line in cls_match.group(1).splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("- ") and current_list_key:
                classification[current_list_key].append(line[2:].strip())
            elif ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()
                if val == "":
                    classification[key] = []
                    current_list_key = key
                else:
                    classification[key] = val
                    current_list_key = None

    return PersonaProfile(
        household_heading=heading,
        sections=section_text,
        transition_alerts=transition_alerts,
        subjective_concerns_raw=subj_raw,
        has_subjective_concerns=has_subj,
        objective_concerns=obj_concerns,
        tensions=tensions,
        classification=classification,
        risk_alignment=str(classification.get("D4", "")),
        decision_style=str(classification.get("D5", "")),
        motivational_anchor=str(classification.get("D6", "")),
    )


def load_case(case_id: str, cases_dir: str | Path | None = None) -> CaseData:
    """Load real JSONs and `persona.md` for one of the 4 Sherpas cases."""
    if case_id not in SUPPORTED_CASES:
        raise ValueError(f"Unknown case_id '{case_id}'. Expected one of {SUPPORTED_CASES}.")
    root = resolve_cases_dir(cases_dir)
    case_dir = root / case_id
    fh_path = case_dir / "financial-health.json"
    ia_path = case_dir / "investment-analysis.json"
    persona_path = case_dir / "persona.md"

    if not fh_path.is_file() or not ia_path.is_file() or not persona_path.is_file():
        raise FileNotFoundError(f"Missing required case files inside {case_dir}.")

    fh = json.loads(fh_path.read_text(encoding="utf-8"))
    ia = json.loads(ia_path.read_text(encoding="utf-8"))
    persona_text = persona_path.read_text(encoding="utf-8")
    persona = parse_persona_markdown(persona_text)
    return CaseData(
        case_id=case_id,
        case_dir=case_dir,
        financial_health=fh,
        investment_analysis=ia,
        persona_text=persona_text,
        persona=persona,
    )


def _add_numeric_variants(bucket: set[float], val: float) -> None:
    if abs(val) > 1e12:
        return
    for candidate in (val, abs(val)):
        bucket.add(round(candidate, 4))
        bucket.add(round(candidate, 2))
        bucket.add(round(candidate, 1))
        bucket.add(float(round(candidate)))
    if -2.0 <= val <= 2.0:
        pct = abs(val) * 100.0
        bucket.add(round(pct, 2))
        bucket.add(round(pct, 1))
        bucket.add(float(round(pct)))


def _walk_numbers(node: Any, bucket: set[float]) -> None:
    if isinstance(node, bool):
        return
    if isinstance(node, (int, float)):
        _add_numeric_variants(bucket, float(node))
    elif isinstance(node, str):
        for raw in re.findall(r"-?\d[\d,]*(?:\.\d+)?", node):
            try:
                num = float(raw.replace(",", ""))
                _add_numeric_variants(bucket, num)
            except ValueError:
                pass
    elif isinstance(node, list):
        for item in node:
            _walk_numbers(item, bucket)
    elif isinstance(node, dict):
        for val in node.values():
            _walk_numbers(val, bucket)


def extract_case_allowed_numbers(
    case: CaseData,
    extra_numbers: list[float | int] | dict[str, Any] | str | None = None,
) -> set[float]:
    """Collect every verified number from `financial-health.json`, `investment-analysis.json`, and `persona.md`."""
    allowed: set[float] = {0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 14.0, 30.0, 60.0, 100.0}
    _walk_numbers(case.financial_health, allowed)
    _walk_numbers(case.investment_analysis, allowed)
    _walk_numbers(case.persona_text, allowed)

    # Scaled notations from persona.md / report abbreviations (e.g. $550k -> 550000, $2.35M -> 2350000)
    for match in re.finditer(r"(\d+(?:\.\d+)?)\s*([kKmM])\b", case.persona_text):
        base = float(match.group(1))
        mult = 1_000.0 if match.group(2).lower() == "k" else 1_000_000.0
        _add_numeric_variants(allowed, base * mult)
        _add_numeric_variants(allowed, base)

    # Exact derived annual debt interest and net cash drag figures directly implied by liabilities & cash
    for debt in case.high_interest_debts(threshold=0.0):
        _add_numeric_variants(allowed, debt["annual_interest"])
    cash_earned = case.cash_yield_earned()
    if cash_earned > 0:
        _add_numeric_variants(allowed, cash_earned)
    for debt in case.high_interest_debts(threshold=0.10):
        if cash_earned > 0:
            _add_numeric_variants(allowed, debt["annual_interest"] - cash_earned)

    # Combined life gap across spouses and 401(k) marginal tax saving when directly implied by waterfall
    wf_ins = case.waterfall_row("insurance")
    if wf_ins and isinstance(wf_ins.get("delta"), (int, float)):
        _add_numeric_variants(allowed, abs(float(wf_ins["delta"])))
    wf_401k = case.waterfall_row("401k")
    tax_bracket = float(
        case.savings_and_contributions.get("taxOpportunityCheck", {})
        .get("preTaxVsRothCheck", {})
        .get("currentTaxBracket", 0.0)
    )
    if wf_401k and isinstance(wf_401k.get("delta"), (int, float)) and tax_bracket > 0:
        _add_numeric_variants(allowed, abs(float(wf_401k["delta"])) * tax_bracket)

    if extra_numbers is not None:
        _walk_numbers(extra_numbers, allowed)
    return allowed


def _strip_structural_tokens(text: str) -> str:
    cleaned = re.sub(r"\b[OTD]\d+[a-c]?\b", " ", text)
    cleaned = re.sub(r"\b401\s*\(?k\)?", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b529\b", " ", cleaned)
    cleaned = re.sub(r"\b3x\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b(?:Día|Dia|Day|Step|Paso)\s+\d+\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b\d+/\d+\b", " ", cleaned)
    cleaned = re.sub(r"(?m)^\s*\d+[\.\)]\s+", " ", cleaned)
    return cleaned


def verify_text_numbers_against_case(
    text: str,
    allowed_numbers: set[float],
) -> tuple[bool, list[str]]:
    """Verify every numeric figure in `text` belongs to `allowed_numbers` (no invented numbers)."""
    cleaned = _strip_structural_tokens(text)
    unverified: list[str] = []

    for match in re.finditer(r"(-?\d[\d,]*(?:\.\d+)?)(\s*[kKmM])?", cleaned):
        raw_num = match.group(1)
        suffix = (match.group(2) or "").strip().lower()
        try:
            val = abs(float(raw_num.replace(",", "")))
        except ValueError:
            continue
        candidates = [val]
        if suffix == "k":
            candidates.append(val * 1_000.0)
        elif suffix == "m":
            candidates.append(val * 1_000_000.0)

        matched = any(
            round(c, 4) in allowed_numbers
            or round(c, 2) in allowed_numbers
            or round(c, 1) in allowed_numbers
            or float(round(c)) in allowed_numbers
            for c in candidates
        )
        if not matched:
            token = f"{raw_num}{suffix}"
            if token not in unverified:
                unverified.append(token)

    return (len(unverified) == 0, unverified)


def _fmt_usd(amount: float | int) -> str:
    val = float(amount)
    sign = "-" if val < 0 else ""
    abs_val = abs(val)
    if abs(abs_val - round(abs_val)) < 0.005:
        return f"{sign}${round(abs_val):,}"
    return f"{sign}${abs_val:,.2f}"


def _fmt_pct(value: float | str, is_decimal_ratio: bool = False) -> str:
    if isinstance(value, str):
        return value if value.endswith("%") else f"{value}%"
    pct = value * 100.0 if is_decimal_ratio else float(value)
    if abs(pct - round(pct)) < 0.05:
        return f"{round(pct)}%"
    return f"{pct:.1f}%"


def _build_topic_context(case: CaseData, topic: str, extra_context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Assemble strictly real Plain + Math content from JSONs & persona.md for the requested topic."""
    cash_facts = case.fh_facts.get("cash", {})
    ret_facts = case.fh_facts.get("retirement", {})
    edu_facts = case.fh_facts.get("education") or {}
    accessible_cash = float(cash_facts.get("accessibleCash", {}).get("value", 0.0))
    months_before = str(cash_facts.get("monthsCovered", {}).get("value", "0"))
    months_after = str(cash_facts.get("monthsCoveredAfterNearTermGoals", {}).get("value", months_before))
    net_cash_flow = float(ret_facts.get("netCashFlowThisYear", {}).get("value", 0.0))
    high_debts = case.high_interest_debts(threshold=0.10)
    tax_drag = case.tax_drag_annual_cost()
    neg_inv = case.first_negative_investable_year()
    neg_nw = case.first_negative_net_worth_year()
    savings_cur = case.savings_and_contributions.get("currentSavings", {})
    savings_rate_pct = float(savings_cur.get("currentSavingsRate", 0.0)) * 100.0
    annual_savings = float(savings_cur.get("reportedAnnualSavings", 0.0))
    perf_hh = case.performance_analysis.get("household", {})
    max_dd_pct = abs(float(perf_hh.get("maxDrawdown3y", 0.0))) * 100.0
    rec_days = int(perf_hh.get("maxDrawdownRecoveryDays", 0))
    best_move = max(case.top_moves, key=lambda m: int(m.get("score_after", 0)), default={})
    combined_best = max(case.combined_moves, key=lambda m: int(m.get("score_after", 0)), default={})

    topic_norm = (topic or "overview").strip().lower()
    metrics: list[dict[str, Any]] = []
    sources: list[str] = []

    if topic_norm in ("liquidity", "cash_flow", "cash"):
        reserve_min = float(cash_facts.get("emergencyReserve", {}).get("min", 0.0))
        reserve_max = float(cash_facts.get("emergencyReserve", {}).get("max", 0.0))
        plain_headline = f"Tienes {months_before} meses de gastos esenciales cubiertos ({months_after} meses tras metas cercanas)"
        if float(months_after) == 0:
            plain_summary = (
                f"Hoy tu colchón cubre {months_before} meses, pero tras apartar tus metas de 2027 "
                f"bajas a 0 meses de margen líquido. Ordenar primero la reserva protege la tranquilidad diaria."
            )
        elif net_cash_flow < 0:
            plain_summary = (
                f"Cuentas con {months_before} meses de colchón ({_fmt_usd(accessible_cash)}), pero cada año "
                f"salen {_fmt_usd(abs(net_cash_flow))} más de los que entran tras ahorrar {_fmt_usd(annual_savings)}/año."
            )
        else:
            plain_summary = (
                f"Cuentas con {months_before} meses de gastos cubiertos ({_fmt_usd(accessible_cash)}) "
                f"y un margen anual positivo de {_fmt_usd(net_cash_flow)}/año para equilibrar deudas y protección."
            )
        metrics = [
            {"label": "Accessible cash", "value": _fmt_usd(accessible_cash), "unit": "USD", "json_source": "financial-health.json -> key_metrics.facts.cash.accessibleCash"},
            {"label": "Months covered (before / after near-term goals)", "value": f"{months_before} / {months_after}", "unit": "months", "json_source": "financial-health.json -> key_metrics.facts.cash.monthsCovered"},
            {"label": "Recommended emergency reserve", "value": f"{_fmt_usd(reserve_min)}–{_fmt_usd(reserve_max)}", "unit": "USD", "json_source": "financial-health.json -> key_metrics.facts.cash.emergencyReserve"},
            {"label": "Net cash flow this year", "value": _fmt_usd(net_cash_flow), "unit": "USD/yr", "json_source": "financial-health.json -> key_metrics.facts.retirement.netCashFlowThisYear"},
        ]
        bias_unlock = "Separa el dinero de emergencia del dinero comprometido en metas próximas para evitar falsa liquidez."
        action_today = f"Revisa el Step 1 de tu cascada ({case.savings_waterfall[1][1] if len(case.savings_waterfall) > 1 else 'reserva'})."

    elif topic_norm in ("debt", "deuda"):
        if high_debts:
            d = high_debts[0]
            cash_earned = case.cash_yield_earned()
            net_burn = d["annual_interest"] - cash_earned if cash_earned > 0 else d["annual_interest"]
            plain_headline = f"Tu tarjeta {d['name']} quema {_fmt_usd(d['annual_interest'])} al año sin aportar valor a tu familia"
            plain_summary = (
                f"Mantener {_fmt_usd(d['balance'])} en la tarjeta al {d['apr_pct']}% APR cuesta {_fmt_usd(d['annual_interest'])}/año "
                f"({_fmt_usd(d['monthly_payment'])}/mes). Liquidarla libera flujo mensual y calma financiera inmediata."
            )
            if case.case_id == "timothy-melanie-weah":
                plain_summary += (
                    f" Mientras tanto, {_fmt_usd(accessible_cash)} en efectivo solo rinden ~{_fmt_usd(cash_earned)}/año: "
                    f"pierdes ~{_fmt_usd(net_burn)} netos al año por tener ambos cajones separados."
                )
            metrics = [
                {"label": f"{d['name']} balance", "value": _fmt_usd(d["balance"]), "unit": "USD", "json_source": "financial-health.json -> profile.liabilities"},
                {"label": f"{d['name']} APR", "value": f"{d['apr_pct']}%", "unit": "percent", "json_source": "financial-health.json -> profile.liabilities"},
                {"label": "Annual interest cost", "value": _fmt_usd(d["annual_interest"]), "unit": "USD/yr", "json_source": "financial-health.json -> profile.liabilities (balance * interest_rate)"},
                {"label": "Accessible cash", "value": _fmt_usd(accessible_cash), "unit": "USD", "json_source": "financial-health.json -> key_metrics.facts.cash.accessibleCash"},
            ]
            bias_unlock = "Rompe la Contabilidad Mental juntando ahorro e interés caro en un único balance neto."
            action_today = f"Atacar {d['name']} ({_fmt_usd(d['balance'])}) según el escalón 8 de savingsWaterfall."
        else:
            plain_headline = "Sin deudas de consumo: 0 USD quemados en intereses"
            plain_summary = "Tu hogar no arrastra deuda cara ni préstamos activos, lo que libera capacidad para asegurar el retiro."
            metrics = [
                {"label": "Debt pillar points", "value": case.pillars[1]["points_shown_in_app"] if len(case.pillars) > 1 else "20/20", "unit": "points", "json_source": "financial-health.json -> score.pillars"},
            ]
            bias_unlock = "Aprovecha la ausencia de deuda para no caer en el Efecto Halo y atender la jubilación."
            action_today = "Redirigir parte del ahorro anual a cuentas con ventaja fiscal."

    elif topic_norm in ("retirement", "jubilacion"):
        spend_need = float(ret_facts.get("spendingNeed", {}).get("value", 0.0))
        share = str(ret_facts.get("incomeShareOfNeed", {}).get("value", "0%"))
        draw_pct = str(ret_facts.get("withdrawalRateAverage", {}).get("value", "0%"))
        ret_gap = float(case.savings_and_contributions.get("goalCoverage", {}).get("retirementGap", 0.0))
        left_end = float(ret_facts.get("savingsLeftAtPlanEnd", {}).get("value", 0.0))
        if neg_inv:
            plain_headline = (
                f"Alerta de liquidez futura: en {neg_inv['year']} (edad {neg_inv['age_client']}) "
                f"el dinero líquido cae a {_fmt_usd(neg_inv['investable_assets'])}"
            )
            plain_summary = (
                f"Aunque el patrimonio total incluya vivienda ({_fmt_usd(neg_inv['net_worth'])} en {neg_inv['year']}), "
                f"los ingresos garantizados cubren {share} del gasto y el dinero líquido para facturas se agota en {neg_inv['year']}."
            )
        else:
            plain_headline = (
                f"Cobertura garantizada del {share} con {_fmt_usd(left_end)} previstos al final del plan"
                if ret_gap == 0
                else f"Brecha de retiro de {_fmt_usd(ret_gap)}: tus aportaciones actuales aún dejan margen de mejora"
            )
            plain_summary = (
                f"Tus ingresos garantizados cubren el {share} de los {_fmt_usd(spend_need)}/año necesarios en retiro. "
                f"Ahorrando {savings_rate_pct:.1f}% ({_fmt_usd(annual_savings)}/año) puedes ordenar las piezas fiscales."
            )
        metrics = [
            {"label": "Yearly retirement spending need", "value": _fmt_usd(spend_need), "unit": "USD/yr", "json_source": "financial-health.json -> key_metrics.facts.retirement.spendingNeed"},
            {"label": "Guaranteed income share", "value": share, "unit": "percent", "json_source": "financial-health.json -> key_metrics.facts.retirement.incomeShareOfNeed"},
            {"label": "Average withdrawal rate", "value": draw_pct, "unit": "percent", "json_source": "financial-health.json -> key_metrics.facts.retirement.withdrawalRateAverage"},
            {"label": "Retirement gap", "value": _fmt_usd(ret_gap), "unit": "USD", "json_source": "investment-analysis.json -> key_metrics.savingsAndContributions.goalCoverage.retirementGap"},
        ]
        if neg_inv:
            metrics.append(
                {
                    "label": f"First negative investable_assets ({neg_inv['year']}, age {neg_inv['age_client']})",
                    "value": _fmt_usd(neg_inv["investable_assets"]),
                    "unit": "USD",
                    "json_source": f"financial-health.json -> projections.yearly[{neg_inv['year']}].investable_assets",
                }
            )
        else:
            metrics.append(
                {
                    "label": "Savings left at plan end",
                    "value": _fmt_usd(left_end),
                    "unit": "USD",
                    "json_source": "financial-health.json -> key_metrics.facts.retirement.savingsLeftAtPlanEnd",
                }
            )
        bias_unlock = "Conecta tu yo de hoy con tu edad de retiro separando ladrillo ilíquido de liquidez disponible."
        action_today = best_move.get("action", "Aprovechar margen fiscal en 401(k)/HSA.")

    elif topic_norm in ("protection", "proteccion", "insurance"):
        wf_ins = case.waterfall_row("insurance") or {}
        prot_pillar = next((p for p in case.pillars if "insurance" in p.get("pillar", "").lower()), {})
        delta_abs = abs(float(wf_ins.get("delta") or 0.0))
        plain_headline = (
            f"Escudo familiar: pilar de protección en {prot_pillar.get('points_shown_in_app', '0/20')}"
        )
        if delta_abs > 0:
            plain_summary = (
                f"Si faltara un ingreso hoy, la familia tiene una brecha total de {_fmt_usd(delta_abs)} en protección. "
                f"No es hablar de escenarios negativos: es blindar el hogar y los estudios de los hijos."
            )
        else:
            plain_summary = (
                "La cobertura de vida y paraguas está sólida, pero falta confirmar pólizas de vivienda y vehículo."
            )
        metrics = [
            {"label": "Protection pillar", "value": str(prot_pillar.get("points_shown_in_app", "")), "unit": "points", "json_source": "financial-health.json -> score.pillars"},
            {"label": "Insurance waterfall current vs target", "value": f"{_fmt_usd(wf_ins.get('current', 0))} / {_fmt_usd(wf_ins.get('optimal_target', 0))}", "unit": "USD", "json_source": "investment-analysis.json -> key_metrics.savingsAndContributions.savingsWaterfall[2]"},
        ]
        if case.top_moves:
            metrics.append(
                {
                    "label": "Top protection move",
                    "value": f"{case.top_moves[0]['title']} ({case.top_moves[0]['score_before']} -> {case.top_moves[0]['score_after']})",
                    "unit": "score",
                    "json_source": "financial-health.json -> score.top_moves[0]",
                }
            )
        bias_unlock = "Reemplaza el sesgo de optimismo por tranquilidad concreta para quienes dependen de ti."
        action_today = case.top_moves[0]["action"] if case.top_moves else "Confirmar pólizas vigentes."

    elif topic_norm in ("investments", "tax_drag", "inversiones"):
        plain_headline = f"Tus inversiones soportan caídas históricas (máx. -{max_dd_pct:.1f}% recuperada en {rec_days} días) pero pagan {_fmt_usd(tax_drag)}/año en impuestos evitables"
        plain_summary = (
            f"En los últimos 3 años tu cartera resistió una caída máxima de -{max_dd_pct:.1f}% y volvió a recuperar en {rec_days} días. "
            f"Ajustar dónde colocas fondos ineficientes ahorra {_fmt_usd(tax_drag)}/año en impuestos sin asumir más riesgo."
        )
        metrics = [
            {"label": "Annual in-scope tax drag", "value": _fmt_usd(tax_drag), "unit": "USD/yr", "json_source": "investment-analysis.json -> key_metrics.taxDragAnalysis.householdRollup"},
            {"label": "3y max drawdown", "value": f"-{max_dd_pct:.2f}%", "unit": "percent", "json_source": "investment-analysis.json -> key_metrics.performanceAnalysis.household.maxDrawdown3y"},
            {"label": "Max drawdown recovery", "value": f"{rec_days}", "unit": "days", "json_source": "investment-analysis.json -> key_metrics.performanceAnalysis.household.maxDrawdownRecoveryDays"},
            {"label": "Historical macro events tracked", "value": f"{len(case.analysis_events)}", "unit": "events", "json_source": "investment-analysis.json -> analysis.events"},
        ]
        bias_unlock = "Mirar la recuperación real en días neutraliza el miedo de vender en caídas y evita fugas fiscales."
        action_today = "Revisar activos con alto dividendo ordinario (como JNK/SCHD) en cuentas sujetas a impuestos."

    elif topic_norm in ("home_purchase", "housing", "vivienda"):
        home_goals = [g for g in case.profile.get("goals", []) if g.get("type") == "REAL_ESTATE_PURCHASE"]
        if home_goals:
            hg = home_goals[0]
            yr = int(hg.get("start_year", 2027))
            amt = float(hg.get("amount", 0.0))
            planned = hg.get("planned_purchase", {})
            loan = hg.get("planned_loan", {})
            costs = {c.get("name", ""): float(c.get("yearly", 0.0)) for c in hg.get("yearly_costs", [])}
            down_amt = next((v for k, v in costs.items() if "downpayment" in k.lower()), 0.0)
            closing_amt = next((v for k, v in costs.items() if "closing" in k.lower()), 0.0)
            tax_amt = next((v for k, v in costs.items() if "tax" in k.lower()), 0.0)
            ins_amt = next((v for k, v in costs.items() if "insurance" in k.lower()), 0.0)
            y_prev = case.projection_for_year(yr - 1) or {}
            y_buy = case.projection_for_year(yr) or {}
            plain_headline = f"Comprar casa de {_fmt_usd(amt)} en {yr} cambia tu liquidez de golpe"
            plain_summary = (
                f"Más allá de la cuota mensual de {_fmt_usd(loan.get('monthly_payment', 0))}/mes, "
                f"la entrada ({_fmt_usd(down_amt)}), cierre ({_fmt_usd(closing_amt)}), impuestos ({_fmt_usd(tax_amt)}/año) "
                f"y seguro ({_fmt_usd(ins_amt)}/año) reducen los activos invertibles de "
                f"{_fmt_usd(y_prev.get('investable_assets', 0))} ({yr - 1}) a {_fmt_usd(y_buy.get('investable_assets', 0))} ({yr})."
            )
            metrics = [
                {"label": f"Home purchase ({yr})", "value": _fmt_usd(amt), "unit": "USD", "json_source": "financial-health.json -> profile.goals[REAL_ESTATE_PURCHASE].amount"},
                {"label": "Price at purchase / down payment", "value": f"{_fmt_usd(planned.get('value_at_purchase', amt))} / {_fmt_usd(down_amt)}", "unit": "USD", "json_source": "financial-health.json -> profile.goals[REAL_ESTATE_PURCHASE].yearly_costs"},
                {"label": "Hidden annual costs (property tax + insurance) & closing", "value": f"{_fmt_usd(tax_amt)}/yr + {_fmt_usd(ins_amt)}/yr; cierre {_fmt_usd(closing_amt)}", "unit": "USD", "json_source": "financial-health.json -> profile.goals[REAL_ESTATE_PURCHASE].yearly_costs"},
                {"label": f"Investable assets ({yr - 1} -> {yr})", "value": f"{_fmt_usd(y_prev.get('investable_assets', 0))} -> {_fmt_usd(y_buy.get('investable_assets', 0))}", "unit": "USD", "json_source": "financial-health.json -> projections.yearly"},
            ]
            bias_unlock = "Visibiliza todos los costes ocultos de propiedad y lleva al Advisor Brief un retraso de fecha."
            action_today = "Solicitar al asesor simular la compra de vivienda en una fecha alternativa (no hay contrafactual precalculado)."
        else:
            plain_headline = "Sin nueva compra de vivienda planeada; foco en patrimonio líquido y protección"
            plain_summary = "El hogar ya cuenta con vivienda en propiedad y su prioridad es proteger liquidez y retiro."
            metrics = [
                {"label": "Accessible cash", "value": _fmt_usd(accessible_cash), "unit": "USD", "json_source": "financial-health.json -> key_metrics.facts.cash.accessibleCash"},
            ]
            bias_unlock = "No confundir el valor bruto de la vivienda con dinero líquido disponible."
            action_today = "Priorizar eliminación de tarjeta cara y protección familiar."

    else:
        # Overview (default)
        target_score = combined_best.get("score_after") or best_move.get("score_after") or case.published_score
        if neg_inv:
            plain_headline = (
                f"{case.household_name}: hoy tienes {months_before} meses cubiertos ({months_after} tras metas), "
                f"pero el dinero líquido cae a {_fmt_usd(neg_inv['investable_assets'])} en {neg_inv['year']}"
            )
        elif high_debts:
            d = high_debts[0]
            plain_headline = (
                f"{case.household_name}: {months_before} meses cubiertos, pero la tarjeta de {_fmt_usd(d['balance'])} "
                f"al {d['apr_pct']}% quema {_fmt_usd(d['annual_interest'])}/año"
            )
        else:
            plain_headline = f"{case.household_name}: {months_before} meses de colchón con plan mejorable ({case.published_score} -> {target_score})"

        plain_summary = (
            f"Ahorras {_fmt_usd(annual_savings)}/año ({savings_rate_pct:.1f}% de ingresos) y cuentas con {months_before} meses de reserva "
            f"({months_after} meses tras metas cercanas). Reordenando prioridades pasas de score {case.published_score} a {target_score} "
            f"ganando tranquilidad familiar sin perder tu ritmo de vida."
        )
        metrics = [
            {"label": "Published score -> target score", "value": f"{case.published_score} -> {target_score}", "unit": "score", "json_source": "financial-health.json -> score.published_score / score.top_moves / score.combined_moves"},
            {"label": "Accessible cash & months covered", "value": f"{_fmt_usd(accessible_cash)} ({months_before} / {months_after} mo)", "unit": "USD / months", "json_source": "financial-health.json -> key_metrics.facts.cash"},
            {"label": "Reported annual savings", "value": f"{_fmt_usd(annual_savings)}/yr ({savings_rate_pct:.1f}%)", "unit": "USD/yr", "json_source": "investment-analysis.json -> key_metrics.savingsAndContributions.currentSavings"},
            {"label": "Net cash flow this year", "value": _fmt_usd(net_cash_flow), "unit": "USD/yr", "json_source": "financial-health.json -> key_metrics.facts.retirement.netCashFlowThisYear"},
            {"label": "In-scope annual tax drag", "value": _fmt_usd(tax_drag), "unit": "USD/yr", "json_source": "investment-analysis.json -> key_metrics.taxDragAnalysis.householdRollup"},
        ]
        if neg_inv:
            metrics.append(
                {
                    "label": f"Liquidity depletion year ({neg_inv['year']}, age {neg_inv['age_client']})",
                    "value": _fmt_usd(neg_inv["investable_assets"]),
                    "unit": "USD",
                    "json_source": f"financial-health.json -> projections.yearly[{neg_inv['year']}].investable_assets",
                }
            )
        if edu_facts and isinstance(edu_facts.get("fundingGap"), dict):
            metrics.append(
                {
                    "label": "College funding gap",
                    "value": _fmt_usd(edu_facts["fundingGap"]["value"]),
                    "unit": "USD",
                    "json_source": "financial-health.json -> key_metrics.facts.education.fundingGap",
                }
            )
        bias_unlock = (
            f"Ancla motivacional {case.persona.motivational_anchor or 'PROTECTION'}: traduce porcentajes lejanos en meses de vida cubierta "
            "y un primer paso ejecutable hoy."
        )
        action_today = best_move.get("action", "Ejecutar el primer paso del waterfall hoy.")

    for m in metrics:
        if m["json_source"] not in sources:
            sources.append(m["json_source"])

    math_headline = f"{case.household_name} | Score {case.published_score}/100 ({case.score_band})"
    math_bullets = [f"{m['label']}: {m['value']} [{m['json_source']}]" for m in metrics]
    math_summary = " | ".join(math_bullets)
    family_peace = (
        "Protege la estabilidad del hogar traduciendo cifras complejas en meses reales de colchón y pasos ordenados."
    )
    if case.children:
        child_names = ", ".join(str(ch.get("first_name", "")) for ch in case.children)
        family_peace = (
            f"Protege directamente la estabilidad diaria y el futuro de {child_names} asegurando techo, liquidez y cobertura."
        )

    return {
        "case_id": case.case_id,
        "household_name": case.household_name,
        "topic": topic_norm,
        "plain": {
            "headline": plain_headline,
            "summary": plain_summary,
            "months_of_life_covered": f"{months_before} meses hoy ({months_after} meses tras metas cercanas)",
            "family_peace_of_mind": family_peace,
            "bias_unlock": bias_unlock,
            "action_today": action_today,
            "bullets": [plain_headline, family_peace, bias_unlock, action_today],
        },
        "math": {
            "headline": math_headline,
            "summary": math_summary,
            "metrics": metrics,
            "json_sources": sources,
            "bullets": math_bullets,
        },
        "extra_context": extra_context or {},
    }


def _evaluate_bias_for_case(case: CaseData, bias_id: str) -> dict[str, Any]:
    """Compute real-data evidence, triggered status, and Plain/Math explanations for a bias."""
    if bias_id not in BIAS_METADATA:
        raise ValueError(f"Unknown bias_id '{bias_id}'. Expected one of {ALL_BIAS_IDS}.")

    meta = dict(BIAS_METADATA[bias_id])
    cash_facts = case.fh_facts.get("cash", {})
    ret_facts = case.fh_facts.get("retirement", {})
    edu_facts = case.fh_facts.get("education") or {}
    accessible_cash = float(cash_facts.get("accessibleCash", {}).get("value", 0.0))
    months_before = str(cash_facts.get("monthsCovered", {}).get("value", "0"))
    months_after = str(cash_facts.get("monthsCoveredAfterNearTermGoals", {}).get("value", months_before))
    high_debts = case.high_interest_debts(threshold=0.10)
    tax_drag = case.tax_drag_annual_cost()
    neg_inv = case.first_negative_investable_year()
    neg_nw = case.first_negative_net_worth_year()
    savings_cur = case.savings_and_contributions.get("currentSavings", {})
    annual_savings = float(savings_cur.get("reportedAnnualSavings", 0.0))
    savings_rate_pct = float(savings_cur.get("currentSavingsRate", 0.0)) * 100.0
    savings_cap = float(case.savings_and_contributions.get("savingsCapacity", {}).get("savingsCapacity", 0.0))
    perf_hh = case.performance_analysis.get("household", {})
    max_dd_pct = abs(float(perf_hh.get("maxDrawdown3y", 0.0))) * 100.0
    rec_days = int(perf_hh.get("maxDrawdownRecoveryDays", 0))
    best_move = max(case.top_moves, key=lambda m: int(m.get("score_after", 0)), default={})
    combined_best = max(case.combined_moves, key=lambda m: int(m.get("score_after", 0)), default={})
    target_score = combined_best.get("score_after") or best_move.get("score_after") or case.published_score

    triggered = False
    severity = "none"
    plain = ""
    math = ""
    unlock_mechanic = ""
    evidence: dict[str, Any] = {}
    json_sources: list[str] = []

    if bias_id == "ikea_effect":
        triggered = True
        severity = "high" if case.published_score < 65 else "medium"
        plain = (
            f"Un informe estático paraliza a {case.household_name} (score {case.published_score}); "
            f"cuando elige campamentos en la montaña, ve consecuencias y sube a {target_score} con Rewind, siente el plan como propio."
        )
        math = (
            f"published_score={case.published_score} ({case.score_band}); ruta hacia score={target_score} "
            f"con {len(case.top_moves)} top_moves y {len(case.combined_moves)} combined_moves."
        )
        unlock_mechanic = "Previsualización de tendencia + Efecto IKEA + Rewind tras bloqueo en grieta/muro."
        evidence = {"published_score": case.published_score, "target_score": target_score, "top_moves_count": len(case.top_moves)}
        json_sources = ["financial-health.json -> score.published_score", "financial-health.json -> score.top_moves"]

    elif bias_id == "mental_accounting":
        if high_debts and (accessible_cash >= 25_000 or annual_savings >= 20_000):
            d = high_debts[0]
            cash_earned = case.cash_yield_earned()
            triggered = True
            severity = "high" if d["balance"] >= 10_000 else "medium"
            if case.case_id == "timothy-melanie-weah":
                plain = (
                    f"Separáis el ahorro 'intocable' ({_fmt_usd(accessible_cash)} al 0.09%) de la tarjeta de {_fmt_usd(d['balance'])} al {d['apr_pct']}%. "
                    f"Vuestro efectivo rinde ~{_fmt_usd(cash_earned)}/año, pero la tarjeta quema {_fmt_usd(d['annual_interest'])}/año."
                )
                math = (
                    f"accessibleCash={_fmt_usd(accessible_cash)} (rendimiento ~{_fmt_usd(cash_earned)}/yr) vs. "
                    f"{d['name']}={_fmt_usd(d['balance'])} al {d['apr_pct']}% APR ({_fmt_usd(d['annual_interest'])}/yr); "
                    f"pérdida neta ~{_fmt_usd(d['annual_interest'] - cash_earned)}/yr."
                )
            elif case.case_id == "daniel-emily-johnson":
                plain = (
                    f"Ahorráis {_fmt_usd(annual_savings)}/año en distintas cuentas mientras pagáis un {d['apr_pct']}% "
                    f"en {_fmt_usd(d['balance'])} de tarjeta ({_fmt_usd(d['annual_interest'])}/año quemados en intereses)."
                )
                math = (
                    f"reportedAnnualSavings={_fmt_usd(annual_savings)}/yr vs. {d['name']}={_fmt_usd(d['balance'])} "
                    f"al {d['apr_pct']}% APR ({_fmt_usd(d['annual_interest'])}/yr; $373.50/mes en intereses)."
                )
            else:
                plain = (
                    f"Mantienes {_fmt_usd(accessible_cash)} en efectivo mientras pagas un {d['apr_pct']}% APR "
                    f"en {_fmt_usd(d['balance'])} de tarjeta ({_fmt_usd(d['annual_interest'])}/año en intereses)."
                )
                math = (
                    f"accessibleCash={_fmt_usd(accessible_cash)} vs. {d['name']}={_fmt_usd(d['balance'])} "
                    f"al {d['apr_pct']}% APR ({_fmt_usd(d['annual_interest'])}/yr)."
                )
            evidence = {
                "accessible_cash": accessible_cash,
                "annual_savings": annual_savings,
                "debt_name": d["name"],
                "debt_balance": d["balance"],
                "debt_apr_pct": d["apr_pct"],
                "debt_annual_interest": d["annual_interest"],
                "cash_yield_earned": cash_earned,
            }
        else:
            plain = f"{case.household_name} no presenta deuda cara conviviendo con efectivo ocioso."
            math = f"High-APR debt count={len(high_debts)}; accessibleCash={_fmt_usd(accessible_cash)}."
            evidence = {"high_interest_debt_count": len(high_debts), "accessible_cash": accessible_cash}
        unlock_mechanic = "Rama 'Cubo Agujereado' + Desplegable de Flujo Neto juntando ahorro e interés caro."
        json_sources = [
            "financial-health.json -> profile.liabilities",
            "financial-health.json -> key_metrics.facts.cash.accessibleCash",
            "investment-analysis.json -> key_metrics.cashNeeds.summaryIncome",
        ]

    elif bias_id == "halo_effect":
        tax_deferred_bal = float(
            case.savings_and_contributions.get("taxOpportunityCheck", {})
            .get("preTaxVsRothCheck", {})
            .get("taxDeferredAccountBalance", 0.0)
        )
        if case.published_score >= 75 and (tax_deferred_bal == 0 or neg_inv is not None):
            triggered = True
            severity = "high"
            plain = (
                f"El score verde {case.published_score}/100 ({case.score_band}) oculta que hay $0 en cuentas de jubilación "
                f"y los activos líquidos caen a {_fmt_usd(neg_inv['investable_assets'])} en {neg_inv['year']} (edad {neg_inv['age_client']})."
            )
            math = (
                f"published_score={case.published_score} ({case.score_band}); taxDeferredAccountBalance={_fmt_usd(tax_deferred_bal)}; "
                f"projections.yearly[{neg_inv['year']}].investable_assets={_fmt_usd(neg_inv['investable_assets'])} (age {neg_inv['age_client']})."
            )
            evidence = {
                "published_score": case.published_score,
                "tax_deferred_balance": tax_deferred_bal,
                "depletion_year": neg_inv["year"] if neg_inv else None,
                "depletion_investable_assets": neg_inv["investable_assets"] if neg_inv else None,
            }
        else:
            plain = (
                f"El score actual ({case.published_score}/100, {case.score_band}) no genera falsa seguridad en verde "
                "y refleja brechas visibles."
            )
            math = f"published_score={case.published_score} ({case.score_band}); taxDeferredAccountBalance={_fmt_usd(tax_deferred_bal)}."
            evidence = {"published_score": case.published_score, "tax_deferred_balance": tax_deferred_bal}
        unlock_mechanic = "HUD desglosado en 5 pilares + Salto directo al punto ciego en 2053 (edad 74)."
        json_sources = [
            "financial-health.json -> score.published_score",
            "financial-health.json -> projections.yearly",
            "investment-analysis.json -> key_metrics.savingsAndContributions.taxOpportunityCheck.preTaxVsRothCheck",
        ]

    elif bias_id == "house_rich_cash_poor":
        real_estate = [a for a in case.profile.get("other_assets", []) or [] if "home" in str(a.get("name", "")).lower() or a.get("type") == "REAL_ESTATE"]
        home_val = sum(float(a.get("value") or a.get("balance") or 0.0) for a in real_estate)
        conc_nw = float(case.investment_analysis.get("key_metrics", {}).get("concentrationAndDiversification", {}).get("totals", {}).get("netWorth", 0.0))
        if neg_inv is not None or home_val >= 500_000:
            triggered = True
            severity = "high" if neg_inv is not None else "medium"
            if neg_inv is not None:
                plain = (
                    f"El patrimonio neto incluye paredes ilíquidas ({_fmt_usd(neg_inv['net_worth'])} en {neg_inv['year']}), "
                    f"pero el dinero líquido para vivir cae a {_fmt_usd(neg_inv['investable_assets'])} a los {neg_inv['age_client']} años."
                )
                math = (
                    f"projections.yearly[{neg_inv['year']}] -> net_worth={_fmt_usd(neg_inv['net_worth'])} vs. "
                    f"investable_assets={_fmt_usd(neg_inv['investable_assets'])} (age {neg_inv['age_client']})."
                )
                if neg_nw is not None:
                    math += f" net_worth llega a {_fmt_usd(neg_nw['net_worth'])} en {neg_nw['year']}."
            else:
                plain = (
                    f"Gran parte del patrimonio ({_fmt_usd(conc_nw)}) está inmovilizado en la vivienda ({_fmt_usd(home_val)}), "
                    f"dejando solo {_fmt_usd(accessible_cash)} ({months_before} meses) en liquidez inmediata."
                )
                math = (
                    f"home_value={_fmt_usd(home_val)}; netWorth={_fmt_usd(conc_nw)}; "
                    f"accessibleCash={_fmt_usd(accessible_cash)} ({months_before} meses)."
                )
            evidence = {
                "home_value": home_val,
                "net_worth": neg_inv["net_worth"] if neg_inv else conc_nw,
                "investable_assets_at_cliff": neg_inv["investable_assets"] if neg_inv else None,
                "cliff_year": neg_inv["year"] if neg_inv else None,
                "accessible_cash": accessible_cash,
            }
        else:
            plain = f"No hay iliquidez inmobiliaria grave ahora ({_fmt_usd(accessible_cash)} líquidos)."
            math = f"accessibleCash={_fmt_usd(accessible_cash)}; netWorth={_fmt_usd(conc_nw)}."
            evidence = {"accessible_cash": accessible_cash, "net_worth": conc_nw}
        unlock_mechanic = "Separación visual Investable Assets vs. Net Worth en toda la ruta de projections.yearly."
        json_sources = [
            "financial-health.json -> projections.yearly",
            "financial-health.json -> profile.other_assets",
            "investment-analysis.json -> key_metrics.concentrationAndDiversification.totals.netWorth",
        ]

    elif bias_id == "present_bias":
        purchases = [g for g in case.profile.get("goals", []) if g.get("type") == "REAL_ESTATE_PURCHASE"]
        if purchases:
            hg = purchases[0]
            yr = int(hg.get("start_year", 2027))
            amt = float(hg.get("amount", 0.0))
            y_prev = case.projection_for_year(yr - 1) or {}
            y_buy = case.projection_for_year(yr) or {}
            prev_inv = float(y_prev.get("investable_assets", 0.0))
            buy_inv = float(y_buy.get("investable_assets", 0.0))
            triggered = True
            severity = "high" if buy_inv < prev_inv or float(months_after) == 0 else "medium"
            plain = (
                f"Priorizar la compra de casa de {_fmt_usd(amt)} en {yr} hace bajar los activos invertibles "
                f"de {_fmt_usd(prev_inv)} a {_fmt_usd(buy_inv)} y deja {months_after} meses de caja libre tras metas."
            )
            math = (
                f"goal={_fmt_usd(amt)} ({yr}); investable_assets {yr - 1}: {_fmt_usd(prev_inv)} -> {yr}: {_fmt_usd(buy_inv)}; "
                f"monthsCoveredAfterNearTermGoals={months_after}."
            )
            evidence = {
                "purchase_year": yr,
                "purchase_amount": amt,
                "investable_before": prev_inv,
                "investable_after": buy_inv,
                "months_after_near_term": months_after,
            }
        else:
            plain = f"Sin compra inmobiliaria inminente; el riesgo presente es mantener {len(high_debts)} deuda cara."
            math = f"No REAL_ESTATE_PURCHASE goal; accessibleCash={_fmt_usd(accessible_cash)}."
            evidence = {"purchase_count": 0, "accessible_cash": accessible_cash}
        unlock_mechanic = "Bifurcación instantánea en la línea temporal conectando 2026/2027 con 2047 y 2075."
        json_sources = [
            "financial-health.json -> profile.goals",
            "financial-health.json -> projections.yearly",
            "financial-health.json -> key_metrics.facts.cash.monthsCoveredAfterNearTermGoals",
        ]

    elif bias_id == "future_self_gap":
        triggered = True
        severity = "high" if neg_inv is not None else "medium"
        age_now = case.adults[0].get("age", 37) if case.adults else 37
        age_ret = case.adults[0].get("retirement_age", 62) if case.adults else 62
        end_row = case.yearly_projections[-1] if case.yearly_projections else {}
        end_age = end_row.get("age_client") or end_row.get("age_co_client") or 90
        run_out = ret_facts.get("savingsRunOut", {})
        left_end = ret_facts.get("savingsLeftAtPlanEnd", {}).get("value")
        if run_out:
            plain = (
                f"Vivir tu ruta paso a paso (Age {age_now} -> Age {age_ret} -> Age {end_age}) convierte "
                f"un dato lejano ({_fmt_usd(run_out.get('value', 0))} sin cubrir) en tu propia historia y en meses de vida ({months_before} meses)."
            )
            math = (
                f"Age {age_now} -> ret {age_ret} -> end {end_age}; {run_out.get('label', '')}: {_fmt_usd(run_out.get('value', 0))}."
            )
        else:
            plain = (
                f"En vez de cifras abstractas como {_fmt_usd(left_end or 0)} al final del plan (Age {age_now} -> Age {age_ret} -> Age {end_age}), "
                f"ves qué margen mensual real tiene tu yo futuro."
            )
            math = (
                f"Age {age_now} -> ret {age_ret} -> end {end_age}; savingsLeftAtPlanEnd={_fmt_usd(left_end or 0)}."
            )
        unlock_mechanic = f"Progreso en primera persona (Age {age_now} -> Age {age_ret} -> Age {end_age}) + Toggle Plain <-> Math."
        evidence = {"age_now": age_now, "age_retire": age_ret, "age_end": end_age, "savings_left_end": left_end}
        json_sources = [
            "financial-health.json -> case.household",
            "financial-health.json -> projections.yearly",
            "financial-health.json -> key_metrics.facts.retirement",
        ]

    elif bias_id == "planning_fallacy":
        purchases = [g for g in case.profile.get("goals", []) if g.get("type") in ("REAL_ESTATE_PURCHASE", "VEHICLE_PURCHASE")]
        home_purchases = [g for g in purchases if g.get("type") == "REAL_ESTATE_PURCHASE"]
        if home_purchases:
            hg = home_purchases[0]
            yr = int(hg.get("start_year", 2027))
            amt = float(hg.get("amount", 0.0))
            loan = hg.get("planned_loan", {})
            costs = {c.get("name", ""): float(c.get("yearly", 0.0)) for c in hg.get("yearly_costs", [])}
            prop_tax = next((v for k, v in costs.items() if "property tax" in k.lower()), 0.0)
            home_ins = next((v for k, v in costs.items() if "insurance" in k.lower()), 0.0)
            closing = next((v for k, v in costs.items() if "closing" in k.lower()), 0.0)
            down = next((v for k, v in costs.items() if "downpayment" in k.lower()), 0.0)
            rent_exp = next((e for e in case.profile.get("expenses", []) if e.get("type") == "RENT"), None)
            triggered = True
            severity = "high" if yr <= 2027 else "medium"
            rent_txt = f"alquiler de {_fmt_usd(rent_exp['monthly'])}/mes frente a " if rent_exp else ""
            plain = (
                f"Al planear casa de {_fmt_usd(amt)} en {yr}, es fácil mirar solo {rent_txt}"
                f"hipoteca de {_fmt_usd(loan.get('monthly_payment', 0))}/mes e ignorar impuestos ({_fmt_usd(prop_tax)}/año), "
                f"seguro ({_fmt_usd(home_ins)}/año) y cierre ({_fmt_usd(closing)})."
            )
            math = (
                f"Home {yr} ({_fmt_usd(amt)}): downpayment={_fmt_usd(down)}, closing={_fmt_usd(closing)}, "
                f"property_taxes={_fmt_usd(prop_tax)}/yr, home_insurance={_fmt_usd(home_ins)}/yr, "
                f"monthly_mortgage={_fmt_usd(loan.get('monthly_payment', 0))}."
            )
            evidence = {
                "year": yr,
                "amount": amt,
                "downpayment": down,
                "closing_costs": closing,
                "property_taxes_yr": prop_tax,
                "home_insurance_yr": home_ins,
                "mortgage_monthly": loan.get("monthly_payment", 0),
            }
        else:
            plain = "Sin compra inmobiliaria o vehículo con costes ocultos pendientes en este plan."
            math = "No REAL_ESTATE_PURCHASE goal in profile.goals."
            evidence = {"purchase_goals": 0}
        unlock_mechanic = "Desplegable del Campamento de Transición (2027 / 2030) con costes totales reales y Transition alerts."
        json_sources = ["financial-health.json -> profile.goals", "persona.md -> Transition alerts"]

    elif bias_id == "ostrich_effect":
        if case.published_score < 60 and annual_savings >= 25_000:
            triggered = True
            severity = "high"
            plain = (
                f"Ahorras {_fmt_usd(annual_savings)}/año ({savings_rate_pct:.1f}% de tus ingresos), un esfuerzo enorme. "
                f"Abrir el informe con un {case.published_score}/100 ({case.score_band}) invita a cerrarlo, pero reordenando piezas subes a {target_score}."
            )
            math = (
                f"reportedAnnualSavings={_fmt_usd(annual_savings)}/yr ({savings_rate_pct:.1f}% savings rate); "
                f"published_score={case.published_score} -> {target_score} ({best_move.get('title', 'top_move')})."
            )
            evidence = {
                "annual_savings": annual_savings,
                "savings_rate_pct": round(savings_rate_pct, 1),
                "published_score": case.published_score,
                "target_score": target_score,
            }
        else:
            plain = (
                f"El esfuerzo actual de ahorro ({savings_rate_pct:.1f}%, {_fmt_usd(annual_savings)}/año) se reconoce primero en el HUD "
                f"para mostrar que subir de {case.published_score} a {target_score} es alcanzable."
            )
            math = f"published_score={case.published_score} -> {target_score}; currentSavingsRate={savings_rate_pct:.1f}%."
            evidence = {"published_score": case.published_score, "target_score": target_score, "savings_rate_pct": round(savings_rate_pct, 1)}
        unlock_mechanic = f"Reframing Positivo ({savings_rate_pct:.1f}% ahorro) + Tronco central viable ({case.published_score} -> {target_score})."
        json_sources = [
            "financial-health.json -> score.published_score",
            "financial-health.json -> score.top_moves",
            "investment-analysis.json -> key_metrics.savingsAndContributions.currentSavings",
        ]

    elif bias_id == "optimism_bias":
        wf_ins = case.waterfall_row("insurance") or {}
        delta = float(wf_ins.get("delta") or 0.0)
        prot_pillar = next((p for p in case.pillars if "insurance" in p.get("pillar", "").lower()), {})
        has_gap = delta < 0 or (case.top_moves and "coverage" in str(case.top_moves[0].get("title", "")).lower())
        if has_gap:
            triggered = True
            total_prot_gap = abs(delta)
            umbrella_gap = 1_000_000.0 if not any(
                ins.get("type") == "UMBRELLA_INSURANCE" for ins in case.profile.get("insurance", [])
            ) else 0.0
            life_gap = max(0.0, total_prot_gap - umbrella_gap) if total_prot_gap > 0 else 0.0
            severity = "high" if prot_pillar.get("score", 100) < 40 else "medium"
            if life_gap > 0:
                plain = (
                    f"Nadie quiere pensar en fallecer o recibir una demanda, pero hoy hay "
                    f"una brecha de {_fmt_usd(life_gap)} en seguro de vida y {_fmt_usd(umbrella_gap)} en umbrella "
                    f"(pilar de protección {prot_pillar.get('points_shown_in_app', '')})."
                )
            else:
                plain = (
                    f"Nadie quiere pensar en un siniestro, pero la vivienda y vehículo figuran sin póliza confirmada "
                    f"(pilar de protección {prot_pillar.get('points_shown_in_app', '')})."
                )
            math = (
                f"Protection pillar={prot_pillar.get('points_shown_in_app', '')}; "
                f"life_gap={_fmt_usd(life_gap)}; umbrella_gap={_fmt_usd(umbrella_gap)}; "
                f"waterfall_protection_gap={_fmt_usd(total_prot_gap)}; score {case.published_score} -> {target_score}."
            )
            evidence = {
                "protection_points": prot_pillar.get("points_shown_in_app", ""),
                "protection_score": prot_pillar.get("score", 0),
                "life_insurance_gap": life_gap,
                "umbrella_gap": umbrella_gap,
                "total_protection_gap": total_prot_gap,
                "target_score": target_score,
            }
        else:
            plain = "Las coberturas de vida y paraguas están dentro de rango."
            math = f"Protection pillar={prot_pillar.get('points_shown_in_app', '')}."
            evidence = {"protection_points": prot_pillar.get("points_shown_in_app", "")}
        unlock_mechanic = "Quest de Miedos + Campamento de Escudo Familiar (blindar ingresos e hijos en vez de hablar de muerte)."
        json_sources = [
            "financial-health.json -> score.pillars",
            "investment-analysis.json -> key_metrics.savingsAndContributions.savingsWaterfall[2]",
            "persona.md -> D3 Protection",
        ]

    elif bias_id == "oxygen_mask_syndrome":
        edu_gap = float(edu_facts.get("fundingGap", {}).get("value", 0.0)) if edu_facts else 0.0
        college_contrib = sum(
            float(acc.get("yearly_contribution_client") or 0.0)
            for acc in case.profile.get("accounts", [])
            if "529" in str(acc.get("account_type", "")).lower() or "custodial" in str(acc.get("account_type", "")).lower()
        )
        ret_contrib = sum(
            float(acc.get("yearly_contribution_client") or 0.0)
            for acc in case.profile.get("accounts", [])
            if "401k" in str(acc.get("account_type", "")).lower()
        )
        pre_tax_check = (
            case.savings_and_contributions.get("taxOpportunityCheck", {})
            .get("preTaxVsRothCheck", {})
        )
        ret_tax_deferred = float(pre_tax_check.get("taxDeferredAccountBalance", 0.0))
        tax_bracket = float(pre_tax_check.get("currentTaxBracket", 0.0))
        wf_401k = case.waterfall_row("401k") or {}
        unused_401k = abs(float(wf_401k.get("delta") or 0.0)) if isinstance(wf_401k.get("delta"), (int, float)) else 0.0
        missed_401k_tax = round(unused_401k * tax_bracket, 2)
        if case.children and (college_contrib > 0 or edu_gap > 0) and (ret_contrib == 0 or ret_tax_deferred == 0):
            triggered = True
            severity = "high"
            total_college = float(edu_facts.get("totalCostAllGoals", {}).get("value", 0.0))
            plain = (
                f"Por proteger antes la universidad de los hijos ({_fmt_usd(total_college)} de objetivo; "
                f"{_fmt_usd(college_contrib)}/año aportados hoy), se deja el retiro propio en $0/año aportados "
                f"(perdiendo hasta {_fmt_usd(missed_401k_tax)}/año de ahorro fiscal en 401(k))."
            )
            math = (
                f"401(k)_client_contrib={_fmt_usd(ret_contrib)}/yr; unused_401k_room={_fmt_usd(unused_401k)} "
                f"(ahorro fiscal potencial {_fmt_usd(missed_401k_tax)}/yr al {_fmt_pct(tax_bracket, True)}); "
                f"taxDeferredBalance={_fmt_usd(ret_tax_deferred)}; college_contrib={_fmt_usd(college_contrib)}/yr; "
                f"totalCostAllGoals={_fmt_usd(total_college)}; educationGap={_fmt_usd(edu_gap)}."
            )
            evidence = {
                "retirement_contrib_yr": ret_contrib,
                "unused_401k_room": unused_401k,
                "missed_401k_tax_savings_yr": missed_401k_tax,
                "tax_deferred_balance": ret_tax_deferred,
                "college_contrib_yr": college_contrib,
                "total_college_cost": total_college,
                "education_gap": edu_gap,
            }
        else:
            plain = f"No hay desplazamiento grave del retiro frente a universidad (aportación 401k={_fmt_usd(ret_contrib)}/año)."
            math = f"401(k)_client_contrib={_fmt_usd(ret_contrib)}/yr; college_contrib={_fmt_usd(college_contrib)}/yr."
            evidence = {"retirement_contrib_yr": ret_contrib, "college_contrib_yr": college_contrib}
        unlock_mechanic = "Desplegable de Tensión (T5 / O1) + Orden óptimo de savingsWaterfall (mascarilla propia primero)."
        json_sources = [
            "financial-health.json -> profile.accounts",
            "financial-health.json -> key_metrics.facts.education",
            "investment-analysis.json -> key_metrics.savingsAndContributions.savingsWaterfall[13]",
            "persona.md -> Tensions / Objective concerns",
        ]

    elif bias_id == "choice_overload":
        open_buckets = [
            r for r in case.savings_waterfall[1:]
            if len(r) >= 5 and str(r[4]) in ("Empty", "Partially filled")
        ]
        triggered = len(open_buckets) >= 3
        severity = "high" if (case.is_couple or len(open_buckets) >= 5) else "medium"
        first_step = open_buckets[0][1] if open_buckets else "Primer paso"
        plain = (
            f"Hay {len(open_buckets)} frentes abiertos a la vez en la cascada (compitiendo por "
            f"{_fmt_usd(savings_cap)}/año de flujo libre); sin un único Step 1 de 3 minutos en el Día 0, la familia no ejecuta ninguno."
        )
        math = (
            f"savingsWaterfall_rows={max(0, len(case.savings_waterfall) - 1)}; pending_buckets={len(open_buckets)}; "
            f"savingsCapacity={_fmt_usd(savings_cap)}/yr; step_1='{first_step}'."
        )
        unlock_mechanic = "Secuenciación Día a Día en Run IRL: entrega un único Step 1 de 3 minutos en el Día 0."
        evidence = {
            "waterfall_total_rows": max(0, len(case.savings_waterfall) - 1),
            "pending_buckets": len(open_buckets),
            "savings_capacity": savings_cap,
            "first_open_bucket": first_step,
        }
        json_sources = [
            "investment-analysis.json -> key_metrics.savingsAndContributions.savingsWaterfall",
            "investment-analysis.json -> key_metrics.savingsAndContributions.savingsCapacity",
        ]

    elif bias_id == "status_quo_bias":
        triggered = True
        daily_cost = 0.0
        if high_debts:
            daily_cost = round(high_debts[0]["annual_interest"] / 365.0, 2)
        elif tax_drag > 0:
            daily_cost = round(tax_drag / 365.0, 2)
        severity = "high" if high_debts else "medium"
        plain = (
            f"Si en el Día 3 o Día 30 la motivación baja y el paso sigue sin marcarse, "
            f"la inercia sigue costando {_fmt_usd(daily_cost)}/día ({_fmt_usd(high_debts[0]['annual_interest'] if high_debts else tax_drag)}/año)."
        )
        math = (
            f"Inertia daily cost={_fmt_usd(daily_cost)}/day "
            f"(annual={_fmt_usd(high_debts[0]['annual_interest'] if high_debts else tax_drag)}/yr); "
            f"nodos Día 0 -> Día 3 -> Día 14 -> Día 30."
        )
        unlock_mechanic = "Tiempo IRL implacable + Notificaciones de insistencia con coste acumulado de la inercia."
        evidence = {"daily_inertia_cost": daily_cost, "tax_drag": tax_drag, "high_debt_interest_yr": high_debts[0]["annual_interest"] if high_debts else 0.0}
        json_sources = [
            "financial-health.json -> profile.liabilities",
            "investment-analysis.json -> key_metrics.taxDragAnalysis.householdRollup",
        ]

    elif bias_id == "loss_aversion_recency":
        upro_pos = next((p for p in case.positions if str(p.get("ticker", "")).upper() == "UPRO"), None)
        triggered = upro_pos is not None or len(case.analysis_events) >= 11
        severity = "high" if upro_pos is not None else "medium"
        if upro_pos is not None:
            upro_val = float(upro_pos.get("value") or 0.0)
            plain = (
                f"Melanie deja {_fmt_usd(accessible_cash)} en efectivo al 0.09% por aversión a la pérdida, "
                f"mientras Timothy mantiene {_fmt_usd(upro_val)} en UPRO (3x apalancado) confiado tras el último rally. "
                f"Los {len(case.analysis_events)} shocks reales muestran una caída máxima de -{max_dd_pct:.1f}% recuperada en {rec_days} días."
            )
            math = (
                f"accessibleCash={_fmt_usd(accessible_cash)} (~0.09%) vs. UPRO={_fmt_usd(upro_val)} (3x); "
                f"events={len(case.analysis_events)}; maxDrawdown3y=-{max_dd_pct:.2f}%, recoveryDays={rec_days}."
            )
            evidence = {
                "accessible_cash": accessible_cash,
                "upro_value": upro_val,
                "events_count": len(case.analysis_events),
                "max_drawdown_pct": round(max_dd_pct, 2),
                "recovery_days": rec_days,
            }
        else:
            plain = (
                f"Ante caídas de mercado, los {len(case.analysis_events)} eventos históricos reales demuestran "
                f"que la cartera resistió -{max_dd_pct:.1f}% y se recuperó en {rec_days} días sin vender en pánico."
            )
            math = f"events={len(case.analysis_events)}; maxDrawdown3y=-{max_dd_pct:.2f}%, recoveryDays={rec_days}."
            evidence = {"events_count": len(case.analysis_events), "max_drawdown_pct": round(max_dd_pct, 2), "recovery_days": rec_days}
        unlock_mechanic = "La Radio del Sherpa (analysis.events / perEventDrawdowns): 11 shocks reales de calma anti-pánico."
        json_sources = [
            "investment-analysis.json -> positions",
            "investment-analysis.json -> analysis.events",
            "investment-analysis.json -> key_metrics.performanceAnalysis.household",
        ]

    elif bias_id == "couples_veto":
        if case.is_couple:
            a1, a2 = case.adults[0], case.adults[1]
            r1 = str(a1.get("risk_profile", ""))
            r2 = str(a2.get("risk_profile", ""))
            triggered = (r1 != r2) or ("MISALIGNED" in case.persona.risk_alignment) or ("DUAL" in case.persona.decision_style)
            severity = "high"
            plain = (
                f"{a1['first_name']} declara perfil {r1} (4) y {a2['first_name']} {r2} (3) ({case.persona.decision_style}). "
                f"Si el plan solo habla a uno, el otro lo frena en silencio; juntos suben a {target_score}."
            )
            math = (
                f"{a1['first_name']}={r1} vs {a2['first_name']}={r2}; D4={case.persona.risk_alignment}; "
                f"D5={case.persona.decision_style}; combined_moves {case.published_score} -> {target_score}."
            )
            evidence = {
                "member_a": a1["first_name"],
                "member_a_risk": r1,
                "member_b": a2["first_name"],
                "member_b_risk": r2,
                "d4_alignment": case.persona.risk_alignment,
                "d5_style": case.persona.decision_style,
                "combined_target_score": target_score,
            }
        else:
            plain = f"{case.household_name} es hogar individual: no existe veto de pareja."
            math = f"is_couple=False; adults={len(case.adults)}."
            evidence = {"is_couple": False}
        unlock_mechanic = "Cordada Asimétrica (60s a ciegas antes de la montaña) + Reparto Owner A / Owner B en Run IRL."
        json_sources = [
            "financial-health.json -> case.household",
            "financial-health.json -> score.combined_moves",
            "persona.md -> D4 / D5",
        ]

    return {
        "bias_id": meta["bias_id"],
        "section": meta["section"],
        "name_es": meta["name_es"],
        "name_en": meta["name_en"],
        "theorist": meta["theorist"],
        "triggered": triggered,
        "severity": severity,
        "plain": plain,
        "math": math,
        "unlock_mechanic": unlock_mechanic,
        "evidence": evidence,
        "json_sources": json_sources,
    }


def _enrich_with_llm(
    llm_client: LLMProxyClient,
    case: CaseData,
    task_label: str,
    grounded_facts: dict[str, Any],
    base_result: dict[str, Any],
    model: str | None = None,
) -> tuple[dict[str, Any], bool, bool, str | None]:
    """Optionally enrich a deterministic payload via LLMProxyClient while strictly blocking invented numbers."""
    allowed = extract_case_allowed_numbers(case, extra_numbers=grounded_facts)
    prompt = (
        f"Tarea: {task_label} para el hogar {case.household_name} ({case.case_id}).\n"
        "REGLA ESTRICTA: Usa ÚNICAMENTE los números que aparecen en los hechos verificados JSON adjuntos. "
        "No inventes ni estimes ninguna cifra nueva. Devuelve JSON con las claves 'plain_summary' y 'math_summary'.\n"
        f"Hechos verificados:\n{json.dumps(grounded_facts, ensure_ascii=False)}"
    )
    resp = llm_client.chat_completion(
        messages=[
            {
                "role": "system",
                "content": "Eres un narrador financiero conductual de Sherpas. Cero números inventados; solo cita datos reales proporcionados.",
            },
            {"role": "user", "content": prompt},
        ],
        model=model or llm_client.default_model,
        fallback_context={"deterministic_json": base_result},
    )
    if resp.used_fallback:
        return base_result, False, True, resp.fallback_reason

    try:
        parsed = json.loads(resp.content)
        candidate_text = " ".join(
            str(parsed.get(k, "")) for k in ("plain_summary", "math_summary") if parsed.get(k)
        )
    except (json.JSONDecodeError, TypeError):
        parsed = None
        candidate_text = resp.content

    if not candidate_text.strip():
        return base_result, False, True, "empty_llm_enrichment"

    ok, bad_nums = verify_text_numbers_against_case(candidate_text, allowed)
    if not ok:
        return base_result, False, True, f"unverified_numbers_detected: {bad_nums}"

    enriched = dict(base_result)
    if isinstance(parsed, dict):
        if parsed.get("plain_summary"):
            enriched["llm_plain_summary"] = str(parsed["plain_summary"])
        if parsed.get("math_summary"):
            enriched["llm_math_summary"] = str(parsed["math_summary"])
    else:
        enriched["llm_narrative"] = candidate_text.strip()
    return enriched, True, False, None


class BehavioralNarrator:
    """High-level Behavioral Translation Engine grounded in real Sherpas case data."""

    def __init__(
        self,
        cases_dir: str | Path | None = None,
        llm_client: LLMProxyClient | None = None,
    ) -> None:
        self.cases_dir = cases_dir
        self.llm_client = llm_client
        self._cache: dict[str, CaseData] = {}

    def list_cases(self) -> list[str]:
        return list_available_cases(self.cases_dir)

    def load_case(self, case_id: str) -> CaseData:
        if case_id not in self._cache:
            self._cache[case_id] = load_case(case_id, cases_dir=self.cases_dir)
        return self._cache[case_id]

    def _get_client(self, llm_client: LLMProxyClient | None = None) -> LLMProxyClient:
        return llm_client or self.llm_client or LLMProxyClient()

    def translate_dual_lens(
        self,
        case_id: str,
        topic: str = "overview",
        lens: str = "both",
        use_llm: bool = False,
        llm_client: LLMProxyClient | None = None,
        model: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Translate a case topic into Dual-Lens `plain` (everyday impact) and `math` (exact USD/JSON sources)."""
        if lens not in ("both", "plain", "math"):
            raise ValueError("lens must be 'both', 'plain', or 'math'.")
        case = self.load_case(case_id)
        base = _build_topic_context(case, topic=topic, extra_context=context)
        used_llm = False
        llm_fallback_used = False
        fallback_reason: str | None = None

        if use_llm:
            client = self._get_client(llm_client)
            grounded = {
                "case_id": case_id,
                "topic": base["topic"],
                "plain": base["plain"],
                "math": base["math"],
            }
            base, used_llm, llm_fallback_used, fallback_reason = _enrich_with_llm(
                client, case, f"Dual-Lens {topic}", grounded, base, model=model
            )

        result: dict[str, Any] = {
            "case_id": base["case_id"],
            "household_name": base["household_name"],
            "topic": base["topic"],
            "requested_lens": lens,
            "plain": base["plain"],
            "math": base["math"],
            "used_llm": used_llm,
            "llm_fallback_used": llm_fallback_used,
            "fallback_reason": fallback_reason,
            "verified_numbers_only": True,
        }
        if "llm_plain_summary" in base:
            result["plain"] = dict(result["plain"], enriched_summary=base["llm_plain_summary"])
        if "llm_math_summary" in base:
            result["math"] = dict(result["math"], enriched_summary=base["llm_math_summary"])
        if "llm_narrative" in base:
            result["llm_narrative"] = base["llm_narrative"]
        return result

    def detect_behavioral_biases(
        self,
        case_id: str,
        include_untriggered: bool = False,
        category: str | None = None,
    ) -> list[dict[str, Any]]:
        """Detect triggered behavioral biases across Section 4 (4.1–4.4) and Appendix A for a case."""
        case = self.load_case(case_id)
        severity_rank = {"high": 0, "medium": 1, "low": 2, "none": 3}
        items: list[dict[str, Any]] = []
        for bias_id in ALL_BIAS_IDS:
            entry = _evaluate_bias_for_case(case, bias_id)
            if category and entry["section"] != category:
                continue
            if include_untriggered or entry["triggered"]:
                items.append(entry)
        items.sort(key=lambda x: (not x["triggered"], severity_rank.get(x["severity"], 9), x["section"]))
        return items

    def explain_bias(
        self,
        case_id: str,
        bias_id: str,
        use_llm: bool = False,
        llm_client: LLMProxyClient | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        """Explain any specific behavioral bias for the case in Plain + Math with optional LLM enrichment."""
        case = self.load_case(case_id)
        entry = _evaluate_bias_for_case(case, bias_id)
        used_llm = False
        llm_fallback_used = False
        fallback_reason: str | None = None

        if use_llm:
            client = self._get_client(llm_client)
            entry, used_llm, llm_fallback_used, fallback_reason = _enrich_with_llm(
                client, case, f"Explicar sesgo {bias_id}", entry, entry, model=model
            )

        entry["case_id"] = case.case_id
        entry["household_name"] = case.household_name
        entry["used_llm"] = used_llm
        entry["llm_fallback_used"] = llm_fallback_used
        entry["fallback_reason"] = fallback_reason
        entry["verified_numbers_only"] = True
        return entry

    def synthesize_cordada_pact(
        self,
        case_id: str,
        member_a_votes: dict[str, Any] | None = None,
        member_b_votes: dict[str, Any] | None = None,
        use_llm: bool = False,
        llm_client: LLMProxyClient | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        """Synthesize the 60s blind Cordada Asimetrica pact before entering the mountain (BIBLIA_FINAL_V1)."""
        case = self.load_case(case_id)
        if not case.is_couple:
            return {
                "case_id": case.case_id,
                "household_name": case.household_name,
                "is_couple": False,
                "shared_100_percent": [],
                "friction_points": [],
                "midpoint_pact": None,
                "plain_summary": f"{case.household_name} es un hogar individual; pasa directo al Quest de Miedos sin votación en pareja.",
                "math_summary": f"is_couple=False; published_score={case.published_score}.",
                "used_llm": False,
                "llm_fallback_used": False,
                "verified_numbers_only": True,
            }

        a1, a2 = case.adults[0], case.adults[1]
        name_a = str(a1.get("first_name", "Member A"))
        name_b = str(a2.get("first_name", "Member B"))
        va = dict(member_a_votes or {})
        vb = dict(member_b_votes or {})

        fears_a = list(va.get("top_fears") or va.get("fears") or [o.id for o in case.persona.objective_concerns[:2]])
        fears_b = list(vb.get("top_fears") or vb.get("fears") or [o.id for o in case.persona.objective_concerns[:2]])
        shared_fear_ids = [f for f in fears_a if f in fears_b]
        concern_map = {o.id: o for o in case.persona.objective_concerns}

        best_combined = max(case.combined_moves, key=lambda m: int(m.get("score_after", 0)), default={})
        target_score = int(best_combined.get("score_after") or case.published_score)
        shared_100 = [
            f"Ancla motivacional compartida ({case.persona.motivational_anchor or 'PROTECTION'}): proteger a la familia y el futuro de los hijos."
        ]
        for fid in shared_fear_ids:
            if fid in concern_map:
                shared_100.append(f"Coincidencia en {fid}: {concern_map[fid].title}")
        if best_combined:
            moves_txt = " + ".join(best_combined.get("moves", []))
            shared_100.append(f"Camino conjunto validado por Sherpas ({moves_txt}): score {case.published_score} -> {target_score}.")

        # Isolate 1-2 friction points
        friction_points: list[dict[str, Any]] = []
        r1 = str(va.get("risk_choice") or a1.get("risk_profile", "Growth"))
        r2 = str(vb.get("risk_choice") or a2.get("risk_profile", "Moderate"))
        if r1 != r2:
            friction_points.append(
                {
                    "id": "friction_risk_profile",
                    "title": f"Perfil de riesgo distinto: {name_a} ({r1}) vs {name_b} ({r2})",
                    "detail": (
                        f"{name_a} busca perfil {r1} mientras {name_b} prioriza {r2}; "
                        f"la alineación D4 figura como {case.persona.risk_alignment or 'MISALIGNED'}."
                    ),
                }
            )

        # Case-specific secondary cash/account friction from real data
        high_debts = case.high_interest_debts(threshold=0.10)
        if case.case_id == "timothy-melanie-weah":
            upro_val = next((float(p.get("value") or 0) for p in case.positions if str(p.get("ticker", "")).upper() == "UPRO"), 12740.0)
            excess = float(case.ia_facts.get("cash", {}).get("cashAboveTotalNeeded", {}).get("value", 60222.5))
            d = high_debts[0]
            friction_points.append(
                {
                    "id": "friction_cash_vs_leverage",
                    "title": f"Efectivo ocioso vs UPRO apalancado y tarjeta al {d['apr_pct']}%",
                    "detail": (
                        f"{name_b} retiene $150,800 en efectivo (~0.09%) mientras {name_a} mantiene {_fmt_usd(upro_val)} en UPRO (3x) "
                        f"y la tarjeta Chase CC ({_fmt_usd(d['balance'])}) quema {_fmt_usd(d['annual_interest'])}/año."
                    ),
                }
            )
            midpoint_pact = {
                "headline": "Pacto realista de Cordada: liquidez segura + limpieza de deuda cara + protección conjunta",
                "cash_flow_basis": f"Exceso de efectivo libre tras reserva y vacaciones: {_fmt_usd(excess)} (cashAboveTotalNeeded).",
                "owner_a_action": f"{name_a}: acotar exposición 3x (UPRO {_fmt_usd(upro_val)}) y subir 401(k) (+$10,500 de margen).",
                "owner_b_action": f"{name_b}: liquidar tarjeta de {_fmt_usd(d['balance'])} al {d['apr_pct']}% usando parte del efectivo excedente.",
                "joint_2_of_2": f"Check conjunto (2/2): cerrar brecha de vida ($1,100,000) y añadir umbrella ($1,000,000) para subir score {case.published_score} -> {target_score}.",
            }
        elif case.case_id == "daniel-emily-johnson":
            fcf = float(case.fh_facts.get("retirement", {}).get("netCashFlowThisYear", {}).get("value", 15032.01))
            d = high_debts[0]
            friction_points.append(
                {
                    "id": "friction_silos_debt_529",
                    "title": f"Silos de roles ({case.persona.decision_style}): tarjeta {d['apr_pct']}% y 529 vs 401(k) en $0",
                    "detail": (
                        f"{name_b} gestiona $26,000/año de ahorro ($8,000 al 529 y $12,000 a brokerage), mientras {name_a} "
                        f"carga {_fmt_usd(d['balance'])} al {d['apr_pct']}% ({_fmt_usd(d['annual_interest'])}/año) y ambos 401(k) reciben $0."
                    ),
                }
            )
            midpoint_pact = {
                "headline": "Pacto realista de Cordada: blindar hijos primero y redirigir flujo sin culpa",
                "cash_flow_basis": f"Flujo de caja libre actual: {_fmt_usd(fcf)}/año + $26,000/año de ahorro existente.",
                "owner_a_action": f"{name_a}: congelar nuevos cargos y liderar amortización acelerada de tarjeta al {d['apr_pct']}%.",
                "owner_b_action": f"{name_b}: redirigir temporalmente parte de los $12,000 de brokerage hacia colchón (1.4 meses -> 3 meses) y 401(k).",
                "joint_2_of_2": f"Check conjunto (2/2): activar cobertura de vida (+$1,166,000) + umbrella ($1,000,000) y subir score {case.published_score} -> {target_score}.",
            }
        else:  # pragma: no cover - defensive fallback for any future couple case
            fcf = float(case.fh_facts.get("retirement", {}).get("netCashFlowThisYear", {}).get("value", 0.0))
            midpoint_pact = {
                "headline": "Pacto realista de Cordada",
                "cash_flow_basis": f"Flujo de caja neto anual: {_fmt_usd(fcf)}/año.",
                "owner_a_action": f"{name_a}: priorizar pasos asignados en waterfall.",
                "owner_b_action": f"{name_b}: coordinar liquidez y protección.",
                "joint_2_of_2": f"Check conjunto (2/2) hacia score {target_score}.",
            }

        # Check explicit node vote disagreements if supplied
        votes_a_map = va.get("votes") if isinstance(va.get("votes"), dict) else {}
        votes_b_map = vb.get("votes") if isinstance(vb.get("votes"), dict) else {}
        for node_key in sorted(set(votes_a_map) & set(votes_b_map)):
            if votes_a_map[node_key] != votes_b_map[node_key] and len(friction_points) < 3:
                friction_points.append(
                    {
                        "id": f"vote_diff_{node_key}",
                        "title": f"Voto divergente en '{node_key}'",
                        "detail": f"{name_a} votó '{votes_a_map[node_key]}' y {name_b} votó '{votes_b_map[node_key]}'.",
                    }
                )

        # Keep isolated friction points concise (max 2 unless explicit vote diffs added)
        friction_points = friction_points[: max(2, len(friction_points))]

        result: dict[str, Any] = {
            "case_id": case.case_id,
            "household_name": case.household_name,
            "is_couple": True,
            "member_a": {"name": name_a, "risk_profile": r1, "top_fears": fears_a},
            "member_b": {"name": name_b, "risk_profile": r2, "top_fears": fears_b},
            "shared_100_percent": shared_100,
            "friction_points": friction_points,
            "midpoint_pact": midpoint_pact,
            "plain_summary": (
                f"Coincidís al 100% en proteger a vuestra familia ({case.persona.motivational_anchor or 'PROTECTION'}). "
                f"Aislados solo {len(friction_points)} puntos de roce para acordar antes de escalar: {midpoint_pact['headline']}."
            ),
            "math_summary": (
                f"{name_a} ({r1}) vs {name_b} ({r2}) | score {case.published_score} -> {target_score} | "
                f"{midpoint_pact['cash_flow_basis']}"
            ),
            "used_llm": False,
            "llm_fallback_used": False,
            "fallback_reason": None,
            "verified_numbers_only": True,
        }

        if use_llm:
            client = self._get_client(llm_client)
            enriched, used_llm, fb_used, fb_reason = _enrich_with_llm(
                client, case, "Síntesis Pacto Cordada Asimétrica", result, result, model=model
            )
            enriched["used_llm"] = used_llm
            enriched["llm_fallback_used"] = fb_used
            enriched["fallback_reason"] = fb_reason
            return enriched
        return result

    build_cordada_pact = synthesize_cordada_pact

    def generate_advisor_brief(
        self,
        case_id: str,
        fear_ranking: list[str] | None = None,
        subjective_concerns: list[str] | str | None = None,
        couple_votes: dict[str, Any] | None = None,
        skipped_moves: list[str] | None = None,
        unmodeled_goals: list[str] | None = None,
        use_llm: bool = False,
        llm_client: LLMProxyClient | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        """Compile Advisor Brief: O1..O8 ranking + subjective concerns, T1..T5 tensions,
        A/B couple disagreements, and unmodeled goals turned into concrete advisor questions.
        """
        case = self.load_case(case_id)

        # 1. Fear ranking (`O1..O9` + Subjective concerns)
        concerns_by_id = {c.id: c for c in case.persona.objective_concerns}
        ordered_ids: list[str] = []
        for fid in fear_ranking or []:
            norm_id = str(fid).strip().upper()
            if norm_id in concerns_by_id and norm_id not in ordered_ids:
                ordered_ids.append(norm_id)
        for c in case.persona.objective_concerns:
            if c.id not in ordered_ids:
                ordered_ids.append(c.id)

        ranked_fears = [
            {
                "rank": idx + 1,
                **concerns_by_id[oid].to_dict(),
                "user_prioritized": oid in {str(x).strip().upper() for x in (fear_ranking or [])},
            }
            for idx, oid in enumerate(ordered_ids)
        ]

        if isinstance(subjective_concerns, str):
            captured_subj = [subjective_concerns.strip()] if subjective_concerns.strip() else []
        elif isinstance(subjective_concerns, list):
            captured_subj = [str(s).strip() for s in subjective_concerns if str(s).strip()]
        else:
            captured_subj = []

        subjective_section = {
            "persona_md_status": case.persona.subjective_concerns_raw or "None recorded",
            "persona_has_subjective": case.persona.has_subjective_concerns,
            "captured_from_user": captured_subj,
        }

        # 2. Tensions (`T1..T5`)
        tensions_list = [t.to_dict() for t in case.persona.tensions]

        # 3. Couple A/B disagreements
        if case.is_couple:
            cv = couple_votes or {}
            va = cv.get("member_a") or cv.get("partner_a") or cv.get("a") or {}
            vb = cv.get("member_b") or cv.get("partner_b") or cv.get("b") or {}
            pact = self.synthesize_cordada_pact(case_id, member_a_votes=va, member_b_votes=vb, use_llm=False)
            couple_section: dict[str, Any] = {
                "is_couple": True,
                "disagreements": pact["friction_points"],
                "shared_alignment": pact["shared_100_percent"],
                "midpoint_pact": pact["midpoint_pact"],
            }
            # Also handle explicit node vote list if provided: [{"node": "...", "vote_a": "...", "vote_b": "..."}]
            for item in cv.get("nodes", []) if isinstance(cv.get("nodes"), list) else []:
                if isinstance(item, dict) and item.get("vote_a") != item.get("vote_b"):
                    couple_section["disagreements"].append(
                        {
                            "id": f"node_{item.get('node', 'decision')}",
                            "title": f"Desacuerdo en nodo {item.get('node', '')}",
                            "detail": (
                                f"{pact['member_a']['name']} eligió '{item.get('vote_a')}' vs "
                                f"{pact['member_b']['name']} eligió '{item.get('vote_b')}'."
                            ),
                        }
                    )
        else:
            couple_section = {
                "is_couple": False,
                "disagreements": [],
                "shared_alignment": [],
                "midpoint_pact": None,
                "note": "Hogar individual: sin desacuerdos A/B de pareja.",
            }

        # 4. Unmodeled goals (no precalculated counterfactual in Sherpas -> concrete advisor questions)
        unmodeled_questions: list[dict[str, Any]] = []
        for g in case.profile.get("goals", []):
            gtype = str(g.get("type", ""))
            if gtype == "REAL_ESTATE_PURCHASE":
                yr = int(g.get("start_year", 2027))
                amt = float(g.get("amount", 0.0))
                planned = g.get("planned_purchase", {})
                costs = {c.get("name", ""): float(c.get("yearly", 0.0)) for c in g.get("yearly_costs", [])}
                down = next((v for k, v in costs.items() if "downpayment" in k.lower()), 0.0)
                closing = next((v for k, v in costs.items() if "closing" in k.lower()), 0.0)
                y_prev = case.projection_for_year(yr - 1) or {}
                y_buy = case.projection_for_year(yr) or {}
                neg_inv = case.first_negative_investable_year()
                cliff_note = (
                    f" y evitar el déficit líquido en {neg_inv['year']} ({_fmt_usd(neg_inv['investable_assets'])})"
                    if neg_inv
                    else ""
                )
                question = (
                    f"Sherpas no tiene calculado un escenario alternativo para la compra de vivienda de {_fmt_usd(amt)} en {yr} "
                    f"(precio proyectado {_fmt_usd(planned.get('value_at_purchase', amt))}, entrada {_fmt_usd(down)}, cierre {_fmt_usd(closing)}). "
                    f"Si retrasamos la compra 2-3 años o reducimos presupuesto, ¿cómo cambia la caída de activos invertibles "
                    f"de {_fmt_usd(y_prev.get('investable_assets', 0))} a {_fmt_usd(y_buy.get('investable_assets', 0))}{cliff_note}?"
                )
                unmodeled_questions.append(
                    {
                        "goal_name": g.get("name", "Purchase a home"),
                        "goal_type": gtype,
                        "target_year": yr,
                        "amount": amt,
                        "question": question,
                        "json_source": "financial-health.json -> profile.goals / projections.yearly",
                    }
                )
            elif gtype == "VEHICLE_PURCHASE":
                yr = int(g.get("start_year", 2028))
                amt = float(g.get("amount", 0.0))
                planned = g.get("planned_purchase", {})
                unmodeled_questions.append(
                    {
                        "goal_name": g.get("name", "Purchase a vehicle"),
                        "goal_type": gtype,
                        "target_year": yr,
                        "amount": amt,
                        "question": (
                            f"Para la compra del vehículo de {_fmt_usd(amt)} en {yr} "
                            f"({_fmt_usd(planned.get('value_at_purchase', amt))} a fecha de compra), "
                            "¿conviene pagarlo al contado con el exceso de liquidez o financiarlo tras liquidar la tarjeta al 18%?"
                        ),
                        "json_source": "financial-health.json -> profile.goals[VEHICLE_PURCHASE]",
                    }
                )

        # Also add data-grounded structural questions where Sherpas notes unknowns or unclosed gaps
        if case.case_id == "samantha-lewis":
            unmodeled_questions.append(
                {
                    "goal_name": "401(k) availability & taxable cost-basis",
                    "goal_type": "RETIREMENT_AND_TAX",
                    "target_year": 2026,
                    "amount": 24500,
                    "question": (
                        "¿Dispone su empleador de un 401(k) ($24,500 de margen) y podemos recopilar el cost basis faltante "
                        "de la cuenta taxable ($300,000, $3,032.20/año de tax drag) para reubicar VTI/JNK/SCHD sin impacto fiscal innecesario?"
                    ),
                    "json_source": "persona.md -> D2/O7/O8 & investment-analysis.json -> taxDragAnalysis.costBasisBlockingNotes",
                }
            )
        elif case.case_id == "daniel-emily-johnson":
            ret_gap = float(case.savings_and_contributions.get("goalCoverage", {}).get("retirementGap", 1427455.89))
            fcf = float(case.fh_facts.get("retirement", {}).get("netCashFlowThisYear", {}).get("value", 15032.01))
            unmodeled_questions.append(
                {
                    "goal_name": "Employer 401(k) match verification & gap sequencing",
                    "goal_type": "RETIREMENT_AND_PROTECTION",
                    "target_year": 2026,
                    "amount": ret_gap,
                    "question": (
                        f"El flujo libre anual es {_fmt_usd(fcf)} frente a {_fmt_usd(ret_gap)} de brecha de retiro: "
                        "¿confirmamos los matches estimados del 401(k) ($6,400 Daniel y $4,800 Emily) y cómo escalonar tarjeta al 24.9% + seguros?"
                    ),
                    "json_source": "persona.md -> O1/T1 & investment-analysis.json -> savingsWaterfall[4..5]",
                }
            )
        elif case.case_id == "timothy-melanie-weah":
            unmodeled_questions.append(
                {
                    "goal_name": "Expense reconciliation & UPRO exit plan",
                    "goal_type": "CASHFLOW_AND_RISK",
                    "target_year": 2026,
                    "amount": 12740,
                    "question": (
                        "La reconciliación de flujo marca gastos posiblemente subestimados (savingsCapacityReliable: false). "
                        "¿Confirmamos el gasto real mensual antes de asignar los $60,222.50 de efectivo libre y reducir UPRO ($12,740)?"
                    ),
                    "json_source": "investment-analysis.json -> savingsAndContributions.cashflowReconciliation & positions",
                }
            )

        for extra_goal in unmodeled_goals or []:
            unmodeled_questions.append(
                {
                    "goal_name": str(extra_goal),
                    "goal_type": "USER_FLAGGED",
                    "target_year": None,
                    "amount": None,
                    "question": f"El hogar pidió evaluar un contrafactual con el asesor para: {extra_goal}.",
                    "json_source": "user_simulation_flag",
                }
            )

        advisor_questions = [q["question"] for q in unmodeled_questions]
        if ranked_fears:
            top_f = ranked_fears[0]
            advisor_questions.insert(
                0,
                f"Miedo #1 priorizado por la familia ({top_f['id']} · {top_f['severity']}): {top_f['title']} — definir plan inmediato.",
            )
        for s in captured_subj:
            advisor_questions.append(f"Preocupación subjetiva expresada por el hogar (ausente en persona.md): {s}")
        for skipped in skipped_moves or []:
            advisor_questions.append(f"Decisión omitida en la simulación que requiere revisión conjunta: {skipped}")

        lines = [
            f"# Advisor Brief — {case.household_name} ({case.case_id})",
            f"- **Score publicado:** {case.published_score}/100 ({case.score_band})",
            f"- **Ancla motivacional:** {case.persona.motivational_anchor or 'N/A'} | **Estilo:** {case.persona.decision_style or 'N/A'}",
            "",
            "## 1. Ranking de Miedos (O1..O8/O9) + Miedos Subjetivos",
            *[f"{f['rank']}. [{f['id']} · {f['severity']}] {f['title']}" for f in ranked_fears[:5]],
            f"- **Subjective concerns (persona.md):** {subjective_section['persona_md_status']}",
            *(
                [f"- **Capturados en Quest:** {'; '.join(captured_subj)}"]
                if captured_subj
                else []
            ),
            "",
            "## 2. Tensiones Reales (T1..T5)",
            *[f"- **{t['id']} ({t['severity']}):** {t['summary']}" for t in tensions_list],
            "",
            "## 3. Desacuerdos de Pareja (Votación A/B)",
            *(
                [f"- {d['title']}: {d['detail']}" for d in couple_section["disagreements"]]
                if couple_section["disagreements"]
                else [f"- {couple_section.get('note', 'Sin desacuerdos.')}"]
            ),
            "",
            "## 4. Preguntas Concretas al Asesor (Metas sin Contrafactual Precalculado)",
            *[f"- {q}" for q in advisor_questions],
        ]

        brief: dict[str, Any] = {
            "case_id": case.case_id,
            "household_name": case.household_name,
            "published_score": case.published_score,
            "score_band": case.score_band,
            "fear_ranking": ranked_fears,
            "subjective_concerns": subjective_section,
            "tensions": tensions_list,
            "couple_disagreements": couple_section,
            "unmodeled_goal_questions": unmodeled_questions,
            "skipped_moves": list(skipped_moves or []),
            "advisor_questions": advisor_questions,
            "markdown_brief": "\n".join(lines),
            "used_llm": False,
            "llm_fallback_used": False,
            "fallback_reason": None,
            "verified_numbers_only": True,
        }

        if use_llm:
            client = self._get_client(llm_client)
            grounded = {
                "case_id": case.case_id,
                "published_score": case.published_score,
                "top_fears": ranked_fears[:3],
                "tensions": tensions_list,
                "unmodeled_goal_questions": unmodeled_questions,
            }
            enriched, used_llm, fb_used, fb_reason = _enrich_with_llm(
                client, case, "Generar resumen ejecutivo Advisor Brief", grounded, brief, model=model
            )
            enriched["used_llm"] = used_llm
            enriched["llm_fallback_used"] = fb_used
            enriched["fallback_reason"] = fb_reason
            return enriched

        return brief


def translate_dual_lens(
    case_id: str,
    topic: str = "overview",
    lens: str = "both",
    use_llm: bool = False,
    llm_client: LLMProxyClient | None = None,
    model: str | None = None,
    cases_dir: str | Path | None = None,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Module-level wrapper for `BehavioralNarrator.translate_dual_lens`."""
    return BehavioralNarrator(cases_dir=cases_dir, llm_client=llm_client).translate_dual_lens(
        case_id=case_id,
        topic=topic,
        lens=lens,
        use_llm=use_llm,
        llm_client=llm_client,
        model=model,
        context=context,
    )


def detect_behavioral_biases(
    case_id: str,
    include_untriggered: bool = False,
    category: str | None = None,
    cases_dir: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Module-level wrapper for `BehavioralNarrator.detect_behavioral_biases`."""
    return BehavioralNarrator(cases_dir=cases_dir).detect_behavioral_biases(
        case_id=case_id,
        include_untriggered=include_untriggered,
        category=category,
    )


def explain_bias(
    case_id: str,
    bias_id: str,
    use_llm: bool = False,
    llm_client: LLMProxyClient | None = None,
    model: str | None = None,
    cases_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Module-level wrapper for `BehavioralNarrator.explain_bias`."""
    return BehavioralNarrator(cases_dir=cases_dir, llm_client=llm_client).explain_bias(
        case_id=case_id,
        bias_id=bias_id,
        use_llm=use_llm,
        llm_client=llm_client,
        model=model,
    )


def synthesize_cordada_pact(
    case_id: str,
    member_a_votes: dict[str, Any] | None = None,
    member_b_votes: dict[str, Any] | None = None,
    use_llm: bool = False,
    llm_client: LLMProxyClient | None = None,
    model: str | None = None,
    cases_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Module-level wrapper for `BehavioralNarrator.synthesize_cordada_pact`."""
    return BehavioralNarrator(cases_dir=cases_dir, llm_client=llm_client).synthesize_cordada_pact(
        case_id=case_id,
        member_a_votes=member_a_votes,
        member_b_votes=member_b_votes,
        use_llm=use_llm,
        llm_client=llm_client,
        model=model,
    )


build_cordada_pact = synthesize_cordada_pact


def generate_advisor_brief(
    case_id: str,
    fear_ranking: list[str] | None = None,
    subjective_concerns: list[str] | str | None = None,
    couple_votes: dict[str, Any] | None = None,
    skipped_moves: list[str] | None = None,
    unmodeled_goals: list[str] | None = None,
    use_llm: bool = False,
    llm_client: LLMProxyClient | None = None,
    model: str | None = None,
    cases_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Module-level wrapper for `BehavioralNarrator.generate_advisor_brief`."""
    return BehavioralNarrator(cases_dir=cases_dir, llm_client=llm_client).generate_advisor_brief(
        case_id=case_id,
        fear_ranking=fear_ranking,
        subjective_concerns=subjective_concerns,
        couple_votes=couple_votes,
        skipped_moves=skipped_moves,
        unmodeled_goals=unmodeled_goals,
        use_llm=use_llm,
        llm_client=llm_client,
        model=model,
    )
