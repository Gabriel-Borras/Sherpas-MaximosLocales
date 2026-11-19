"""Automatic delivery plumbing for La Radio del Sherpa (backend -> n8n -> Telegram).

This module keeps the n8n webhook contract untouched and adds three things:

* a durable, opt-in outbox (``SHERPAS_OUTBOX_DIR``) so a notification is never
  lost when n8n is down; the scheduler replays it on every tick;
* a :class:`NotificationScheduler` that advances every Run IRL with the real
  clock (``SHERPAS_DAY_SECONDS`` seconds per plan day) and emits each milestone
  or overdue notification exactly once;
* small helpers used by ``/api/telegram/*`` (configuration and queue status).

Everything is deterministic and uses only the standard library.  Nothing here
raises into an API caller: transport errors only leave the message in the outbox.
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Callable

DEFAULT_DAY_SECONDS = 86400
DEFAULT_MAX_DAY = 90
_OUTBOX_LOCK = threading.Lock()


def outbox_path() -> Path | None:
    """Return the JSONL outbox file, or ``None`` when persistence is disabled."""
    raw = os.environ.get("SHERPAS_OUTBOX_DIR", "").strip()
    return Path(raw) / "n8n-outbox.jsonl" if raw else None


def record_failure(payload: dict[str, Any]) -> bool:
    """Append an undelivered payload to the outbox; return whether it was stored."""
    path = outbox_path()
    if path is None:
        return False
    try:
        with _OUTBOX_LOCK:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return True
    except OSError:
        return False


def pending_count() -> int:
    """Number of payloads waiting in the outbox."""
    path = outbox_path()
    if path is None or not path.exists():
        return 0
    try:
        with _OUTBOX_LOCK:
            return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    except OSError:
        return 0


def drain_outbox(send: Callable[[dict[str, Any]], bool], *, limit: int = 50) -> int:
    """Retry stored payloads with ``send``; keep the ones that still fail.

    Returns how many were delivered.  Stops at the first failure so the order
    is preserved and a dead n8n is not hammered.
    """
    path = outbox_path()
    if path is None or not path.exists():
        return 0
    delivered = 0
    with _OUTBOX_LOCK:
        try:
            lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        except OSError:
            return 0
        remaining: list[str] = []
        failed = False
        for line in lines:
            if failed or delivered >= limit:
                remaining.append(line)
                continue
            try:
                payload = json.loads(line)
            except ValueError:
                continue  # corrupt line: drop it instead of blocking the queue
            if send(payload):
                delivered += 1
            else:
                failed = True
                remaining.append(line)
        try:
            path.write_text("".join(line + "\n" for line in remaining), encoding="utf-8")
        except OSError:
            pass
    return delivered


def _positive_float(name: str, default: float) -> float:
    try:
        value = float(os.environ.get(name, "") or default)
    except ValueError:
        return default
    return value if value > 0 else default


class NotificationScheduler:
    """Advance every Run IRL with the real clock and emit each alert once."""

    def __init__(
        self,
        state: Any,
        emit: Callable[[dict[str, Any], str], None],
        *,
        day_seconds: float | None = None,
        max_day: int | None = None,
        clock: Callable[[], float] = time.time,
        drain: Callable[[], int] | None = None,
    ) -> None:
        self.state = state
        self.emit = emit
        self.day_seconds = day_seconds or _positive_float("SHERPAS_DAY_SECONDS", DEFAULT_DAY_SECONDS)
        self.max_day = max_day if max_day is not None else int(
            _positive_float("SHERPAS_MAX_DAY", DEFAULT_MAX_DAY)
        )
        self.clock = clock
        self.drain = drain
        self._sent: set[tuple[str, str]] = set()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.ticks = 0
        self.emitted = 0

    def tick(self) -> int:
        """Run one pass; return the number of notifications emitted."""
        now = self.clock()
        count = 0
        runs = self.state.runs
        with runs.lock:
            snapshot = [
                (run_id, runs._runs[run_id], runs._notifications[run_id], runs._created.get(run_id, now))
                for run_id in list(runs._runs)
            ]
        for run_id, engine, notifications, created in snapshot:
            plan_day = min(int((now - created) // self.day_seconds), self.max_day)
            with runs.lock:
                if plan_day > engine.current_day:
                    engine.advance_day(plan_day)
                pending = notifications.generate_milestone_notifications(engine)
            for notification in pending:
                key = (run_id, notification["notification_id"])
                if key in self._sent:
                    continue
                self._sent.add(key)
                self.emit(notification, run_id)
                count += 1
        if self.drain is not None:
            self.drain()
        self.ticks += 1
        self.emitted += count
        return count

    def start(self, interval: float) -> None:
        """Start the daemon loop (idempotent)."""
        if self._thread is not None and self._thread.is_alive():
            return

        def loop() -> None:
            while not self._stop.wait(interval):
                try:
                    self.tick()
                except Exception:
                    # A scheduling pass must never kill the server thread.
                    continue

        self._stop.clear()
        self._thread = threading.Thread(target=loop, name="sherpas-scheduler", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()


def scheduler_interval() -> float:
    """Seconds between passes; ``0`` (default) keeps the scheduler disabled."""
    try:
        return max(0.0, float(os.environ.get("SHERPAS_SCHEDULER_INTERVAL", "") or 0))
    except ValueError:
        return 0.0
