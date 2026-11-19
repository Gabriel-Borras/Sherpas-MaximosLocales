"""Modo Día a Día: plan del Run IRL (Día 0 → 30) y aviso por Telegram de cada día.

Todo sale del motor IRL del caso (``irl_engine``), sin texto inventado:

* qué hacer cada día: ``title`` / ``action_plain`` / responsables del paso;
* por qué (una línea): el coste real de retrasarlo (``inertia_cost``), los días sin
  cobertura, o la finalidad que ya trae el propio paso («... para ...»).

Regla de avisos: el día en que toca un paso se envía ese paso; si no toca nada y hay
algún paso sin cumplir, se recuerda **cada dos días** desde su vencimiento, nombrando
a quien le falta. Si todo está hecho, no se envía nada (solo toca esperar).
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path
from typing import Any

from backend.irl_engine import create_irl_run

HORIZON_DAYS = 30
REMINDER_EVERY_DAYS = 2


def _money(value: float) -> str:
    return f"${value:,.2f}"


def _why(step: Any, inertia: dict[str, Any]) -> str:
    daily = float(inertia.get("daily_cost_usd") or 0)
    label = inertia.get("label")
    if daily > 0 and label:
        return f"Cada día que lo retrasas cuesta {_money(daily)} ({label})."
    if inertia.get("tracks_days_uninsured") and label:
        return f"Cada día sin hacerlo es un día sin cobertura ({label})."
    match = re.search(r"\bpara (.+?)(?:\.|$)", step.action_plain)
    if match:
        return f"Para {match.group(1).strip()}."
    return ""


def _member_names(engine: Any) -> dict[str, str]:
    names = engine.member_names
    if engine.is_couple:
        return {"A": names.get("A_first") or names.get("A", "A"), "B": names.get("B_first") or names.get("B", "B")}
    return {"single": names.get("single") or names.get("client") or "Tú"}


def build_plan(case_id: str, *, cases_dir: str | Path | None = None) -> dict[str, Any]:
    """Every step from Día 0 to Día 30 with who has to do it and why."""
    engine = create_irl_run(case_id, cases_dir=cases_dir)
    members = _member_names(engine)
    steps = []
    for step in sorted(engine.steps, key=lambda s: (s.day, s.step_id)):
        if step.day > HORIZON_DAYS:
            continue
        inertia = engine._step_inertia_snapshot(step, step.day + 1)
        steps.append({
            "step_id": step.step_id,
            "day": step.day,
            "title": step.title,
            "action_plain": step.action_plain,
            "estimated_minutes": step.estimated_minutes,
            "owner_label": step.owner_label,
            "required_members": list(step.required_members),
            "why": _why(step, inertia),
        })
    return {
        "case_id": case_id,
        "is_couple": bool(engine.is_couple),
        "members": [{"id": key, "name": name} for key, name in members.items()],
        "horizon_days": HORIZON_DAYS,
        "reminder_every_days": REMINDER_EVERY_DAYS,
        "steps": steps,
    }


def _missing(step: dict[str, Any], completed: dict[str, list[str]]) -> list[str]:
    done = set(completed.get(step["step_id"], []))
    return [m for m in step["required_members"] if m not in done]


def day_status(plan: dict[str, Any], day: int, completed: dict[str, list[str]]) -> dict[str, Any]:
    """What the day looks like: today's steps, pending ones and whether a reminder is due."""
    names = {m["id"]: m["name"] for m in plan["members"]}
    today = [s for s in plan["steps"] if s["day"] == day]
    pending = []
    for step in plan["steps"]:
        if step["day"] >= day:
            continue
        missing = _missing(step, completed)
        if missing:
            pending.append({**step, "missing_names": [names.get(m, m) for m in missing],
                            "days_late": day - step["day"]})
    upcoming = [s for s in plan["steps"] if s["day"] > day]
    # Cada dos días contados desde el paso pendiente más antiguo (no uno por paso).
    oldest_late = max((p["days_late"] for p in pending), default=0)
    reminder_due = (not today) and bool(pending) and oldest_late % REMINDER_EVERY_DAYS == 0
    if today:
        mode = "task"
    elif pending:
        mode = "pending"
    else:
        mode = "wait"
    return {
        "day": day,
        "mode": mode,
        "today": today,
        "pending": pending,
        "next_day": upcoming[0]["day"] if upcoming else None,
        "reminder_due": reminder_due,
    }


def notification_for_day(
    case_id: str,
    day: int,
    completed: dict[str, list[str]] | None = None,
    *,
    cases_dir: str | Path | None = None,
) -> dict[str, Any] | None:
    """The single Telegram message for ``day`` (``None`` when nothing should be sent)."""
    if not 0 <= int(day) <= HORIZON_DAYS:
        raise ValueError(f"day debe estar entre 0 y {HORIZON_DAYS}")
    plan = build_plan(case_id, cases_dir=cases_dir)
    status = day_status(plan, int(day), completed or {})
    if status["mode"] == "task":
        body = "\n\n".join(
            f"• {s['title']}\n{s['action_plain']}" + (f"\nPor qué: {s['why']}" if s["why"] else "")
            for s in status["today"]
        )
        title = "Tu paso de hoy" if day == 0 else f"Día {day}: tu siguiente paso"
        kind, severity = "milestone", ("info" if day == 0 else "warning")
    elif status["reminder_due"]:
        body = "\n\n".join(
            f"• {p['title']} (Día {p['day']}, hace {p['days_late']} días)\nFalta: {', '.join(p['missing_names'])}"
            + (f"\nPor qué: {p['why']}" if p["why"] else "")
            for p in status["pending"]
        )
        title = f"Día {day}: recordatorio pendiente"
        kind, severity = "overdue_insistence", "warning"
    else:
        return None
    return {
        "notification_id": f"dia_{day}_{uuid.uuid4().hex[:8]}",
        "kind": kind,
        "type": "milestone_insistence",
        "day": int(day),
        "severity": severity,
        "case_id": case_id,
        "target_owner": "Hogar",
        "title": title,
        "message_plain": body,
        "message_math": body,
        "deep_link": "",
        "run_id": "dia-a-dia",
    }
