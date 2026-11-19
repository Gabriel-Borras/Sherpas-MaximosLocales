"""Mensajes de demo de La Radio del Sherpa: un mensaje por clic, con datos reales.

* ``day_payload``: el paso (o pasos, en parejas) que toca el Día N del Run IRL.
* ``shock_payload``: ante una caída de bolsa, busca el shock histórico más parecido
  que la cartera del hogar ya superó y lo cuenta con sus cifras reales
  (``perEventDrawdowns`` + ``performanceAnalysis.household``). Cero cifras inventadas.

Ambos devuelven payloads con el mismo formato que ya entiende el flujo de n8n.
"""

from __future__ import annotations

import uuid
from pathlib import Path

from backend.irl_engine import create_irl_run
from backend.notifications import NotificationEngine

DEMO_DAYS = (0, 3, 14, 30)
_MONTHS = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
           "agosto", "septiembre", "octubre", "noviembre", "diciembre")


def _pct(ratio: float) -> str:
    return f"{abs(ratio) * 100:.1f}".replace(".", ",") + " %"


def _month_year(date_label: str) -> str:
    year, month = str(date_label)[:4], str(date_label)[5:7]
    try:
        return f"{_MONTHS[int(month) - 1]} de {year}"
    except (ValueError, IndexError):
        return str(date_label)


def day_payload(case_id: str, day: int, *, cases_dir: str | Path | None = None) -> dict[str, Any]:
    """One Telegram message with what the household has to do on ``day``."""
    if day not in DEMO_DAYS:
        raise ValueError(f"day debe ser uno de {list(DEMO_DAYS)}")
    engine = create_irl_run(case_id, cases_dir=cases_dir)
    steps = engine.get_timeline_view(day)["active_steps"]
    if not steps:
        raise ValueError(f"El caso {case_id} no tiene pasos el Día {day}")
    body = "\n\n".join(f"• {step['title']}\n{step['action_plain']}" for step in steps)
    return {
        "notification_id": f"demo_day{day}_{uuid.uuid4().hex[:8]}",
        "kind": "milestone",
        "type": "milestone_insistence",
        "day": day,
        "severity": "info" if day == 0 else "warning",
        "case_id": case_id,
        # Sin «Owner A/B»: en la demo el aviso llega a todo el hogar.
        "target_owner": "Hogar",
        "title": "Tu paso de hoy" if day == 0 else f"Día {day}: tu siguiente paso",
        "message_plain": body,
        "message_math": body,
        "deep_link": "",
        "run_id": "demo",
    }


def shock_payload(case_id: str, drop_pct: float = 8.0, *, cases_dir: str | Path | None = None) -> dict[str, Any]:
    """Anti-panic message comparing today's drop with a real one the portfolio already survived."""
    if not 0 < drop_pct <= 60:
        raise ValueError("drop_pct debe estar entre 0 y 60")
    notifications = NotificationEngine(case_id, cases_dir=cases_dir)
    shocks = [
        s for s in notifications.list_historical_shocks()
        if isinstance(s.get("household_drawdown_pct"), (int, float)) and s["household_drawdown_pct"] < 0
    ]
    if not shocks:
        raise ValueError(f"El caso {case_id} no tiene shocks históricos")
    match = min(shocks, key=lambda s: abs(abs(s["household_drawdown_pct"]) * 100 - drop_pct))

    analysis = notifications.case_data.get("investment_analysis") or notifications.case_data.get("investment-analysis") or {}
    household = ((analysis.get("key_metrics") or {}).get("performanceAnalysis") or {}).get("household") or {}
    max_dd = household.get("maxDrawdown3y")
    max_rec = household.get("maxDrawdownRecoveryDays")

    when = _month_year(match.get("date_label") or match.get("start_date") or "")
    event_rec = match.get("household_recovery_days")
    if isinstance(event_rec, int) and event_rec > 0:
        reference = (f"En {when} tu cartera cayó un {_pct(match['household_drawdown_pct'])} "
                     f"y, manteniendo tu estrategia, te recuperaste en {event_rec} días.")
    elif isinstance(max_dd, (int, float)) and isinstance(max_rec, int):
        reference = (f"En {when} tu cartera cayó un {_pct(match['household_drawdown_pct'])}. "
                     f"Tu peor caída de los últimos 3 años fue del {_pct(max_dd)} y, "
                     f"manteniendo tu estrategia, te recuperaste en {max_rec} días.")
    else:
        reference = f"En {when} tu cartera cayó un {_pct(match['household_drawdown_pct'])} y siguió adelante con tu plan."

    drop_label = f"{drop_pct:g}".replace(".", ",")
    return {
        "notification_id": f"demo_shock_{uuid.uuid4().hex[:8]}",
        "kind": "macro_shock",
        "type": "macro_shock_radio",
        "case_id": case_id,
        "headline": f"La bolsa cae hoy un {drop_label} %. Tranquilidad: esto ya lo has superado.",
        "anti_panic_message_plain": (
            f"{reference}\n\nNo es tu primera tormenta. Mantén el rumbo: estás en el buen camino."
        ),
        "matched_event": match.get("name"),
        "matched_event_date": match.get("date_label"),
        "run_id": "demo",
    }
