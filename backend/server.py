"""Servidor HTTP unificado y determinista de Sherpa Basecamp x Run IRL.

La capa HTTP no calcula recomendaciones ni genera datos: entrega los casos y
delega cada transición a los motores deterministas ya verificados del
repositorio.
"""

from __future__ import annotations

import argparse
import copy
import json
import mimetypes
import os
import sys
import threading
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

# ``python -m backend.server`` is the preferred invocation.  Adding the
# repository root also keeps the documented ``python backend/server.py`` CLI
# usable without turning ``backend`` into a regular package.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.api import SessionStore, dispatch_request
from backend.behavioral_narrator import BehavioralNarrator
from backend.irl_engine import IRLEngine, create_irl_run
from backend.llm_proxy import LLMProxyClient
from backend.mcp_client import CaseNotFoundError, get_case, list_cases, load_env_file
from backend.notifications import NotificationEngine
from backend.timeline_engine import TimelineEngine


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FRONTEND_DIR = REPOSITORY_ROOT / "frontend"
OFFICIAL_CASES_DATA = DEFAULT_FRONTEND_DIR / "cases-data.js"

_N8N_MILESTONE_FIELDS = (
    "notification_id",
    "kind",
    "type",
    "day",
    "severity",
    "case_id",
    "target_owner",
    "title",
    "message_plain",
    "message_math",
    "deep_link",
)


def _n8n_webhook_url() -> str:
    """Return the optional n8n URL, loading the local .env only as a fallback."""
    if "N8N_WEBHOOK_URL" not in os.environ:
        load_env_file()
    return os.environ.get("N8N_WEBHOOK_URL", "").strip()


def _telegram_bot_username() -> str:
    """Return the configured Telegram bot username, defaulting to SherpasRadioBot."""
    if "TELEGRAM_BOT_USERNAME" not in os.environ:
        load_env_file()
    return os.environ.get("TELEGRAM_BOT_USERNAME", "").strip().lstrip("@") or "SherpasRadioBot"


def _telegram_deep_link(case_id: str, owner: str | None = None) -> str:
    """Build the official Telegram deep link for La Radio del Sherpa."""
    bot = _telegram_bot_username()
    target = (owner or "client").strip() or "client"
    return f"https://t.me/{bot}?start={case_id or 'demo'}_{target}"


def _emit_n8n_webhook(payload: dict[str, Any]) -> None:
    """Best-effort, asynchronous n8n delivery that never delays an API response."""
    webhook_url = _n8n_webhook_url()
    if not webhook_url:
        return

    def post_webhook() -> None:
        try:
            request = urllib.request.Request(
                webhook_url,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                method="POST",
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(request, timeout=2):
                pass
        except Exception:
            # The webhook is an optional side effect: transport, HTTP and JSON
            # errors must never affect the deterministic API response.
            return

    try:
        threading.Thread(target=post_webhook, daemon=True).start()
    except Exception:
        # Thread creation is equally optional from the API caller's viewpoint.
        return


def _milestone_webhook_payload(
    notification: dict[str, Any], run_id: str,
) -> dict[str, Any]:
    """Expose the n8n milestone contract without internal notification fields."""
    return {
        **{field: notification[field] for field in _N8N_MILESTONE_FIELDS},
        "run_id": run_id,
    }


class BadRequestError(ValueError):
    """The HTTP payload or route parameters are not usable by an engine."""


class IRLRunStore:
    """Thread-safe, in-memory store for deterministic Run IRL instances."""

    def __init__(self, cases_dir: str | Path | None = None) -> None:
        self.cases_dir = cases_dir
        self._runs: dict[str, IRLEngine] = {}
        self._notifications: dict[str, NotificationEngine] = {}
        self._next_run_number = 1
        self.lock = threading.RLock()

    def create(self, case_id: str) -> tuple[str, IRLEngine]:
        if not isinstance(case_id, str) or not case_id:
            raise BadRequestError("case_id es obligatorio")
        with self.lock:
            engine = create_irl_run(case_id, cases_dir=self.cases_dir)
            notification_engine = NotificationEngine(
                case_id, cases_dir=self.cases_dir
            )
            run_id = f"irl-{self._next_run_number}"
            self._next_run_number += 1
            self._runs[run_id] = engine
            self._notifications[run_id] = notification_engine
            return run_id, engine

    def get(self, run_id: str) -> tuple[IRLEngine, NotificationEngine]:
        with self.lock:
            try:
                return self._runs[run_id], self._notifications[run_id]
            except KeyError as error:
                raise KeyError(run_id) from error


class ServerState:
    """Dependencies shared by all request handler instances of one server."""

    def __init__(
        self,
        *,
        session_store: SessionStore | None = None,
        cases_dir: str | Path | None = None,
        llm_client: LLMProxyClient | None = None,
    ) -> None:
        self.cases_dir = cases_dir

        def case_provider(case_id: str) -> Any:
            return get_case(case_id, cases_dir=cases_dir)

        self.case_provider = case_provider
        # The case provider makes the existing MCP/local/seed client the single
        # input for the expedition endpoints as well.
        self.session_store = session_store or SessionStore(
            engine=TimelineEngine(case_provider=case_provider, cases_dir=cases_dir)
        )
        self.runs = IRLRunStore(cases_dir=cases_dir)
        # A missing TEAM_KEY is handled synchronously by LLMProxyClient without
        # any network access.  With a key, keep failed/unreachable proxy calls
        # bounded so the narrator can immediately return its deterministic,
        # case-grounded response instead of holding an HTTP request open.
        self.llm_client = llm_client or LLMProxyClient(
            timeout=0.25,
            concurrency_timeout=0.0,
            rate_limit_timeout=0.0,
        )
        self.narrator = BehavioralNarrator(
            cases_dir=cases_dir,
            llm_client=self.llm_client,
        )
        # Rooms are intentionally independent from expedition sessions.  They
        # only synchronize the blind inputs sent by two devices, and can be
        # used with any case accepted by ``case_provider``.
        self.rooms: dict[str, dict[str, Any]] = {}
        self.rooms_lock = threading.RLock()

    def create_room(self, case_id: str) -> dict[str, Any]:
        """Create a room after the canonical provider has accepted its case."""
        # Validate before allocating an id, so invalid case ids cannot create
        # orphaned rooms.  ``case_provider`` also keeps this generic as the
        # catalogue gains cases from local files or MCP.
        self.case_provider(case_id)
        with self.rooms_lock:
            room_id = f"room-{uuid.uuid4().hex}"
            room = {
                "room_id": room_id,
                "case_id": case_id,
                "share_query": f"?case={case_id}&room={room_id}&member=B",
                "evaluation": {"A": None, "B": None},
                "evaluation_ready": False,
                "decisions": {},
            }
            self.rooms[room_id] = room
            return copy.deepcopy(room)

    def get_room(self, room_id: str) -> dict[str, Any]:
        """Return an immutable-to-callers snapshot of one synchronized room."""
        with self.rooms_lock:
            try:
                return copy.deepcopy(self.rooms[room_id])
            except KeyError as error:
                raise KeyError(room_id) from error

    def submit_room_evaluation(
        self,
        room_id: str,
        member: str,
        evaluation: dict[str, Any],
    ) -> dict[str, Any]:
        """Save one member's blind evaluation and return the updated room."""
        with self.rooms_lock:
            try:
                room = self.rooms[room_id]
            except KeyError as error:
                raise KeyError(room_id) from error
            room["evaluation"][member] = copy.deepcopy(evaluation)
            room["evaluation_ready"] = all(
                room["evaluation"][participant] is not None
                for participant in ("A", "B")
            )
            return copy.deepcopy(room)

    def submit_room_decision(
        self,
        room_id: str,
        member: str,
        stage: str,
        vote: dict[str, Any],
    ) -> dict[str, Any]:
        """Save one stage vote and derive its pair readiness and alignment."""
        with self.rooms_lock:
            try:
                room = self.rooms[room_id]
            except KeyError as error:
                raise KeyError(room_id) from error
            decision = room["decisions"].setdefault(
                stage,
                {"A": None, "B": None, "ready": False, "aligned": False},
            )
            decision[member] = copy.deepcopy(vote)
            decision["ready"] = all(
                decision[participant] is not None for participant in ("A", "B")
            )
            decision["aligned"] = bool(
                decision["ready"]
                and decision["A"]["route"] == decision["B"]["route"]
            )
            return copy.deepcopy(room)


def _validate_mode(value: str | None) -> str | None:
    if value is None:
        return None
    if value not in ("plain", "math"):
        raise BadRequestError("mode debe ser plain o math")
    return value


def _query_value(parsed, name: str) -> str | None:
    values = parsed.query.split("&") if parsed.query else []
    for value in values:
        key, separator, raw_value = value.partition("=")
        if key == name:
            return unquote(raw_value) if separator else ""
    return None


def _load_official_cases() -> dict[str, Any]:
    """Read the literal case catalogue bundled with the frontend.

    ``cases-data.js`` deliberately publishes ``CASES_DATA`` as a JSON object
    inside its small UMD wrapper.  Decoding that object keeps the detail API
    aligned with the frontend contract without transforming, supplementing or
    otherwise inventing any case data.
    """
    try:
        source = OFFICIAL_CASES_DATA.read_text(encoding="utf-8")
        marker = "const CASES_DATA = "
        start = source.index(marker) + len(marker)
        cases, _ = json.JSONDecoder().raw_decode(source[start:])
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise FileNotFoundError("Catálogo oficial de casos no disponible") from error
    if not isinstance(cases, dict):
        raise ValueError("El catálogo oficial de casos no es un objeto JSON")
    return cases


def _official_case(case_id: str) -> dict[str, Any]:
    """Return one unmodified frontend case, or the usual not-found error."""
    cases = _load_official_cases()
    try:
        case = cases[case_id]
    except KeyError as error:
        raise CaseNotFoundError(f"Caso no encontrado: {case_id}") from error
    if not isinstance(case, dict):
        raise ValueError("El caso oficial no es un objeto JSON")
    return case


def _response_data_for_case(path: str, parsed, state: ServerState) -> tuple[int, Any]:
    """Serve case summaries, literal frontend data and timeline overviews."""
    mode = _validate_mode(_query_value(parsed, "mode"))
    parts = [part for part in parsed.path.split("/") if part]
    if parts == ["api", "cases"]:
        # list_cases is the canonical MCP/local/seed catalogue; it contains no
        # presentation text and therefore does not need a display mode.
        return 200, {"cases": list_cases(cases_dir=state.cases_dir)}
    if len(parts) == 3 and parts[:2] == ["api", "cases"]:
        if mode is None:
            return 200, _official_case(parts[2])
        # A display mode opts in to TimelineEngine's existing presentation
        # adapter.  The raw route above must remain the frontend's full JSON
        # document, rather than a normalised overview.
        state.case_provider(parts[2])
        return dispatch_request("GET", path, store=state.session_store)
    if len(parts) == 4 and parts[:2] == ["api", "cases"] and parts[3] == "overview":
        # Keep an explicit overview endpoint for callers that want the
        # TimelineEngine representation without adding a mode query parameter.
        state.case_provider(parts[2])
        overview_path = f"/api/cases/{parts[2]}"
        if parsed.query:
            overview_path = f"{overview_path}?{parsed.query}"
        return dispatch_request("GET", overview_path, store=state.session_store)
    raise KeyError("Ruta de caso no encontrada")


def _room_member(body: dict[str, Any]) -> str:
    """Return a room participant while keeping the public A/B contract strict."""
    member = body.get("member")
    if member not in {"A", "B"}:
        raise BadRequestError("member debe ser A o B")
    return member


def _room_stage(value: Any) -> str:
    """Validate a four-stage decision and expose its canonical string key."""
    if isinstance(value, bool):
        raise BadRequestError("stage debe ser un entero entre 0 y 3")
    if isinstance(value, int):
        stage = value
    elif isinstance(value, str) and value in {"0", "1", "2", "3"}:
        stage = int(value)
    else:
        raise BadRequestError("stage debe ser un entero entre 0 y 3")
    if not 0 <= stage <= 3:
        raise BadRequestError("stage debe ser un entero entre 0 y 3")
    return str(stage)


def _handle_rooms(
    method: str,
    parsed,
    body: dict[str, Any],
    state: ServerState,
) -> tuple[int, Any]:
    """Handle lightweight, case-agnostic synchronization rooms for two devices."""
    parts = [part for part in parsed.path.split("/") if part]
    if method == "POST" and parts == ["api", "rooms"]:
        case_id = body.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise BadRequestError("case_id es obligatorio")
        return 201, state.create_room(case_id.strip())

    if len(parts) < 3 or parts[:2] != ["api", "rooms"]:
        raise KeyError("Ruta de sala no encontrada")
    room_id = parts[2]
    suffix = parts[3:]
    if method == "GET" and not suffix:
        return 200, state.get_room(room_id)

    if method == "POST" and suffix == ["evaluation"]:
        member = _room_member(body)
        evaluation = {
            field: body.get(field)
            for field in ("top_fears", "thermometer", "priority", "subjective")
        }
        return 200, state.submit_room_evaluation(room_id, member, evaluation)

    if method == "POST" and suffix == ["decision"]:
        member = _room_member(body)
        route = body.get("route")
        if route not in {"good", "bad"}:
            raise BadRequestError("route debe ser good o bad")
        stage = _room_stage(body.get("stage"))
        vote = {"route": route, "label": body.get("label")}
        return 200, state.submit_room_decision(room_id, member, stage, vote)

    raise KeyError("Ruta de sala no encontrada")


def _expedition_target(path: str) -> str | None:
    """Translate the public expedition aliases to backend.api session routes."""
    parsed = urlsplit(path)
    parts = [part for part in parsed.path.split("/") if part]
    if not parts[:2] == ["api", "expedition"]:
        return None
    tail = parts[2:]
    target: str | None = None
    if not tail:
        target = "/api/sessions"
    elif len(tail) >= 1:
        session_id = tail[0]
        rest = tail[1:]
        route_map = {
            (): "",
            ("quest",): "/quest",
            ("cordada",): "/cordada",
            ("preview",): "/mountain/preview",
            ("decide",): "/mountain/decide",
            ("rewind",): "/mountain/rewind",
            ("restart",): "/mountain/restart",
            ("overview",): "/mountain/overview",
            ("advisor-brief",): "/advisor-brief",
        }
        suffix = route_map.get(tuple(rest))
        if suffix is not None:
            target = f"/api/sessions/{session_id}{suffix}"
    if target is None:
        return None
    return f"{target}?{parsed.query}" if parsed.query else target


def _get_radio_context(
    identifier: str,
    state: ServerState,
) -> tuple[str | None, IRLEngine, NotificationEngine]:
    """Use an existing run when possible, otherwise build a case-only view."""
    try:
        engine, notifications = state.runs.get(identifier)
        return identifier, engine, notifications
    except KeyError:
        engine = create_irl_run(identifier, cases_dir=state.runs.cases_dir)
        notifications = NotificationEngine(
            identifier, cases_dir=state.runs.cases_dir
        )
        return None, engine, notifications


def _radio_payload(
    run_id: str | None,
    engine: IRLEngine,
    notifications: NotificationEngine,
    owner: str | None = None,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "case_id": engine.case_id,
        "current_day": engine.current_day,
        "milestones": notifications.generate_milestone_notifications(engine),
        "macro_shocks": notifications.list_historical_shocks(),
        "telegram_bot_username": _telegram_bot_username(),
        "telegram_deep_link": _telegram_deep_link(engine.case_id, owner),
    }


def _handle_irl(
    method: str,
    parsed,
    body: dict[str, Any],
    state: ServerState,
) -> tuple[int, Any]:
    parts = [part for part in parsed.path.split("/") if part]
    if method == "POST" and parts == ["api", "irl"]:
        run_id, engine = state.runs.create(body.get("case_id"))
        return 201, {
            "run_id": run_id,
            "case_id": engine.case_id,
            "focus_mode_view": engine.get_focus_mode_view(),
        }
    if len(parts) < 3 or parts[:2] != ["api", "irl"]:
        raise KeyError("Ruta Run IRL no encontrada")

    run_id = parts[2]
    suffix = parts[3:]
    engine, notifications = state.runs.get(run_id)
    with state.runs.lock:
        if method == "GET" and not suffix:
            mountain = engine.get_mountain_overview()
            timeline = engine.get_timeline_view()
            focus = engine.get_focus_mode_view()
            return 200, {
                "run_id": run_id,
                "case_id": engine.case_id,
                "focus_mode_view": focus,
                "timeline_view": timeline,
                "mountain_overview": mountain,
            }
        if method == "POST" and suffix == ["check"]:
            step_id = body.get("step_id")
            if not step_id:
                raise BadRequestError("step_id es obligatorio")
            result = engine.check_step(
                step_id,
                member=body.get("member"),
                completed_day=body.get("completed_day"),
            )
            for notification in notifications.generate_milestone_notifications(engine):
                _emit_n8n_webhook(_milestone_webhook_payload(notification, run_id))
            return 200, {"run_id": run_id, **result}
        if method == "POST" and suffix == ["uncheck"]:
            step_id = body.get("step_id")
            if not step_id:
                raise BadRequestError("step_id es obligatorio")
            result = engine.uncheck_step(step_id, member=body.get("member"))
            return 200, {"run_id": run_id, **result}
        if method == "POST" and suffix == ["advance"]:
            day = body.get("day", body.get("current_day"))
            if day is None:
                raise BadRequestError("day es obligatorio")
            result = engine.advance_day(int(day))
            for notification in notifications.generate_milestone_notifications(engine):
                _emit_n8n_webhook(_milestone_webhook_payload(notification, run_id))
            return 200, {"run_id": run_id, **result}
        if method == "POST" and suffix == ["repeat"]:
            reset_irl = body.get("reset_irl", False)
            if not isinstance(reset_irl, bool):
                raise BadRequestError("reset_irl debe ser booleano")
            result = engine.repeat_expedition(reset_irl=reset_irl)
            return 200, {"run_id": run_id, **result}
        if method == "GET" and suffix == ["inertia"]:
            return 200, {"run_id": run_id, **engine.compute_inertia_cost()}
    raise KeyError("Ruta Run IRL no encontrada")


def _handle_radio(
    method: str,
    parsed,
    body: dict[str, Any],
    state: ServerState,
) -> tuple[int, Any, str | None]:
    """Return status, payload and an optional non-JSON content type."""
    parts = [part for part in parsed.path.split("/") if part]
    if method == "GET" and parts == ["api", "radio"]:
        # The historical series is portfolio-specific.  The canonical first
        # supported case gives the complete official 11-event series without
        # fabricating a cross-household aggregate.
        notifications = NotificationEngine(
            "michael-carter", cases_dir=state.runs.cases_dir
        )
        return 200, {
            "historical_shocks": notifications.list_historical_shocks(),
            "telegram_bot_username": _telegram_bot_username(),
            "telegram_deep_link": _telegram_deep_link("demo", _query_value(parsed, "owner")),
        }, None
    if len(parts) < 3 or parts[:2] != ["api", "radio"]:
        raise KeyError("Ruta Radio no encontrada")

    identifier = parts[2]
    suffix = parts[3:]
    run_id, engine, notifications = _get_radio_context(identifier, state)
    if method == "GET" and not suffix:
        return 200, _radio_payload(run_id, engine, notifications, owner=_query_value(parsed, "owner")), None
    if method == "POST" and suffix == ["shock"]:
        event_name = body.get("event_name")
        if event_name is not None and not isinstance(event_name, str):
            raise BadRequestError("event_name debe ser texto")
        for key in ("alert_type", "headline"):
            if key in body and body[key] is not None and not isinstance(body[key], str):
                raise BadRequestError(f"{key} debe ser texto")
        market_drop_pct = body.get("market_drop_pct")
        if market_drop_pct is not None:
            try:
                market_drop_pct = float(market_drop_pct)
            except (TypeError, ValueError) as error:
                raise BadRequestError("market_drop_pct debe ser numerico") from error

        kwargs = {
            key: body[key]
            for key in ("alert_type", "headline")
            if key in body and body[key] is not None
        }
        if market_drop_pct is not None:
            kwargs["market_drop_pct"] = market_drop_pct
        if event_name:
            notification = notifications.generate_macro_shock_notification(
                **kwargs, event_name=event_name
            )
        else:
            matched = notifications.match_macro_shock(**kwargs)
            notification = notifications.generate_macro_shock_notification(
                **kwargs, event_name=matched["name"]
            )
        _emit_n8n_webhook({**notification, "run_id": run_id})
        return 200, {"run_id": run_id, **notification}, None
    if method == "GET" and suffix == ["ics"]:
        if run_id is None:
            raise KeyError(identifier)
        return 200, engine.export_ics(), "text/calendar; charset=utf-8"
    raise KeyError("Ruta Radio no encontrada")


def _required_case_id(body: dict[str, Any], state: ServerState) -> str:
    """Validate a narrative request case without translating unknown IDs to 400."""
    case_id = body.get("case_id")
    if not isinstance(case_id, str) or not case_id.strip():
        raise BadRequestError("case_id es obligatorio")
    case_id = case_id.strip()
    if case_id not in state.narrator.list_cases():
        raise CaseNotFoundError(f"Caso no encontrado: {case_id}")
    return case_id


def _optional_string(
    body: dict[str, Any],
    name: str,
    *,
    default: str | None = None,
    allowed: set[str] | None = None,
) -> str | None:
    """Read a non-empty optional string and, when supplied, validate its domain."""
    value = body.get(name, default)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise BadRequestError(f"{name} debe ser texto no vacio")
    value = value.strip()
    if allowed is not None and value not in allowed:
        choices = ", ".join(sorted(allowed))
        raise BadRequestError(f"{name} debe ser uno de: {choices}")
    return value


def _optional_string_list(body: dict[str, Any], name: str) -> list[str] | None:
    """Require a list of non-empty strings when an optional list is supplied."""
    if name not in body or body[name] is None:
        return None
    value = body[name]
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise BadRequestError(f"{name} debe ser una lista de textos no vacios")
    return [item.strip() for item in value]


def _optional_mapping(body: dict[str, Any], name: str) -> dict[str, Any] | None:
    """Require an object when an optional narrator mapping is supplied."""
    if name not in body or body[name] is None:
        return None
    value = body[name]
    if not isinstance(value, dict):
        raise BadRequestError(f"{name} debe ser un objeto JSON")
    return value


def _handle_ai(
    method: str,
    parsed,
    body: dict[str, Any],
    state: ServerState,
) -> tuple[int, Any]:
    """Expose only the case-grounded narrator operations over HTTP.

    Each operation deliberately opts into the existing narrator's LLM path.
    That path verifies generated numbers against the loaded case and returns
    the deterministic payload whenever TEAM_KEY is absent, the proxy errors,
    times out, or returns an unverified figure.
    """
    if method != "POST":
        raise KeyError("Ruta narrativa no encontrada")

    route = parsed.path
    if route not in {"/api/ai/reframe", "/api/ai/pact", "/api/ai/brief"}:
        raise KeyError("Ruta narrativa no encontrada")
    case_id = _required_case_id(body, state)
    model = _optional_string(body, "model")

    if route == "/api/ai/reframe":
        topic = _optional_string(
            body,
            "topic",
            default="overview",
            allowed={
                "overview",
                "liquidity",
                "cash_flow",
                "cash",
                "debt",
                "deuda",
                "retirement",
                "jubilacion",
                "protection",
                "proteccion",
                "insurance",
                "investments",
                "tax_drag",
                "inversiones",
                "home_purchase",
                "housing",
                "vivienda",
            },
        )
        lens = _optional_string(
            body,
            "lens",
            default="both",
            allowed={"both", "plain", "math"},
        )
        context = _optional_mapping(body, "context")
        return 200, state.narrator.translate_dual_lens(
            case_id=case_id,
            topic=topic or "overview",
            lens=lens or "both",
            context=context,
            use_llm=True,
            llm_client=state.llm_client,
            model=model,
        )

    if route == "/api/ai/pact":
        return 200, state.narrator.synthesize_cordada_pact(
            case_id=case_id,
            member_a_votes=_optional_mapping(body, "member_a_votes"),
            member_b_votes=_optional_mapping(body, "member_b_votes"),
            use_llm=True,
            llm_client=state.llm_client,
            model=model,
        )

    if route == "/api/ai/brief":
        subjective_concerns = body.get("subjective_concerns")
        if subjective_concerns is not None and (
            not isinstance(subjective_concerns, str)
            and (
                not isinstance(subjective_concerns, list)
                or any(
                    not isinstance(item, str) or not item.strip()
                    for item in subjective_concerns
                )
            )
        ):
            raise BadRequestError(
                "subjective_concerns debe ser texto o una lista de textos no vacios"
            )
        if isinstance(subjective_concerns, str) and not subjective_concerns.strip():
            raise BadRequestError("subjective_concerns debe ser texto no vacio")
        if isinstance(subjective_concerns, list):
            subjective_concerns = [item.strip() for item in subjective_concerns]
        elif isinstance(subjective_concerns, str):
            subjective_concerns = subjective_concerns.strip()

        return 200, state.narrator.generate_advisor_brief(
            case_id=case_id,
            fear_ranking=_optional_string_list(body, "fear_ranking"),
            subjective_concerns=subjective_concerns,
            couple_votes=_optional_mapping(body, "couple_votes"),
            skipped_moves=_optional_string_list(body, "skipped_moves"),
            unmodeled_goals=_optional_string_list(body, "unmodeled_goals"),
            use_llm=True,
            llm_client=state.llm_client,
            model=model,
        )

    raise KeyError("Ruta narrativa no encontrada")


def _json_bytes(data: Any) -> bytes:
    return json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")


def create_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    *,
    store: SessionStore | None = None,
    cases_dir: str | Path | None = None,
    frontend_dir: str | Path | None = None,
    llm_client: LLMProxyClient | None = None,
) -> ThreadingHTTPServer:
    """Create the standard-library threaded API server without starting it."""
    state = ServerState(
        session_store=store,
        cases_dir=cases_dir,
        llm_client=llm_client,
    )
    static_root = Path(frontend_dir) if frontend_dir is not None else DEFAULT_FRONTEND_DIR

    class Handler(BaseHTTPRequestHandler):
        """HTTP adapter for static files and the unified deterministic API."""

        server_version = "SherpaBasecamp/1.0"

        def _cors_headers(self) -> None:
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")

        def _send(self, status: int, data: Any = None, content_type: str | None = None) -> None:
            if content_type is None:
                content_type = "application/json; charset=utf-8"
                payload = b"" if status == 204 else _json_bytes(data)
            elif isinstance(data, bytes):
                payload = data
            elif isinstance(data, str):
                payload = data.encode("utf-8")
            else:
                payload = _json_bytes(data)
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self._cors_headers()
            self.end_headers()
            if payload:
                self.wfile.write(payload)

        def _read_body(self) -> dict[str, Any]:
            raw_length = self.headers.get("Content-Length", "0")
            try:
                content_length = int(raw_length)
            except ValueError as error:
                raise BadRequestError("Content-Length invalido") from error
            if content_length < 0:
                raise BadRequestError("Content-Length invalido")
            if content_length == 0:
                return {}
            try:
                value = json.loads(self.rfile.read(content_length).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise BadRequestError("JSON invalido") from error
            if not isinstance(value, dict):
                raise BadRequestError("El cuerpo JSON debe ser un objeto")
            return value

        def _serve_static(self, parsed) -> bool:
            if self.command != "GET":
                return False
            relative_url = unquote(parsed.path).lstrip("/")
            relative_path = Path("index.html") if not relative_url else Path(relative_url)
            try:
                root = static_root.resolve()
                candidate = (root / relative_path).resolve()
                candidate.relative_to(root)
            except (OSError, ValueError):
                self._send(404, {"error": "not_found", "message": "Ruta no encontrada"})
                return True
            if not candidate.is_file():
                self._send(404, {"error": "not_found", "message": "Ruta no encontrada"})
                return True
            mime_type, _ = mimetypes.guess_type(candidate.name)
            if mime_type is None:
                mime_type = "application/octet-stream"
            if mime_type.startswith("text/") or mime_type in {"application/javascript", "application/json"}:
                mime_type = f"{mime_type}; charset=utf-8"
            self._send(200, candidate.read_bytes(), mime_type)
            return True

        def _dispatch(self) -> None:
            if self.command == "OPTIONS":
                self._send(204)
                return
            parsed = urlsplit(self.path)
            if not parsed.path.startswith("/api/") and parsed.path != "/health":
                if not self._serve_static(parsed):
                    self._send(404, {"error": "not_found", "message": "Ruta no encontrada"})
                return
            try:
                body = self._read_body() if self.command in ("POST", "PATCH") else {}
                if self.command == "GET" and parsed.path.startswith("/api/cases"):
                    status, data = _response_data_for_case(self.path, parsed, state)
                    self._send(status, data)
                    return

                if parsed.path == "/api/rooms" or parsed.path.startswith("/api/rooms/"):
                    status, data = _handle_rooms(self.command, parsed, body, state)
                    self._send(status, data)
                    return

                expedition_path = _expedition_target(self.path)
                if expedition_path is not None:
                    status, data = dispatch_request(
                        self.command,
                        expedition_path,
                        body,
                        store=state.session_store,
                    )
                    self._send(status, data)
                    return

                if parsed.path.startswith("/api/sessions") or parsed.path == "/health":
                    status, data = dispatch_request(
                        self.command,
                        self.path,
                        body,
                        store=state.session_store,
                    )
                    self._send(status, data)
                    return
                if parsed.path == "/api/irl" or parsed.path.startswith("/api/irl/"):
                    status, data = _handle_irl(self.command, parsed, body, state)
                    self._send(status, data)
                    return
                if parsed.path == "/api/radio" or parsed.path.startswith("/api/radio/"):
                    status, data, content_type = _handle_radio(
                        self.command, parsed, body, state
                    )
                    self._send(status, data, content_type)
                    return
                if parsed.path.startswith("/api/ai/"):
                    status, data = _handle_ai(self.command, parsed, body, state)
                    self._send(status, data)
                    return
                self._send(404, {"error": "not_found", "message": "Ruta no encontrada"})
            except (BadRequestError, ValueError, TypeError) as error:
                self._send(400, {"error": "bad_request", "message": str(error)})
            except (KeyError, FileNotFoundError, CaseNotFoundError) as error:
                self._send(404, {"error": "not_found", "message": str(error)})
            except Exception:
                self._send(500, {"error": "internal_error", "message": "Error interno"})

        do_GET = _dispatch
        do_POST = _dispatch
        do_PATCH = _dispatch
        do_OPTIONS = _dispatch

        def log_message(self, format_string: str, *args: Any) -> None:
            """Keep the library server quiet; callers may add their own logging."""

    httpd = ThreadingHTTPServer((host, port), Handler)
    httpd.state = state  # type: ignore[attr-defined]
    httpd.frontend_dir = static_root  # type: ignore[attr-defined]
    return httpd


def main(argv: list[str] | None = None) -> None:
    """Start the unified server from the command line."""
    parser = argparse.ArgumentParser(description="Sherpa Basecamp x Run IRL API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)
    create_server(args.host, args.port).serve_forever()


if __name__ == "__main__":
    main()
