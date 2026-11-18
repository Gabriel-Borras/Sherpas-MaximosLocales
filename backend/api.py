"""Thread-safe session services and HTTP adapters for the timeline engine."""

from __future__ import annotations

import json
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .timeline_engine import (
    ActionBlockedError,
    Expedition,
    PhaseOrderError,
    TimelineEngine,
)


class SessionStore:
    """Store expeditions behind a reentrant lock."""

    def __init__(self, engine=None):
        self.engine = engine or TimelineEngine()
        self.sessions = {}
        self.lock = threading.RLock()

    def create(self, case_id, mode="plain"):
        """Create and store an expedition session."""
        with self.lock:
            case = self.engine.load_case(case_id)
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = Expedition(case, mode)
            return session_id

    def get(self, session_id):
        """Return a session or raise KeyError."""
        with self.lock:
            if session_id not in self.sessions:
                raise KeyError(session_id)
            return self.sessions[session_id]


def list_cases(store=None):
    """List available cases."""
    return (store or SessionStore()).engine.list_cases()


def get_case_overview(case_id, store=None, mode=None):
    """Return an overview of one case."""
    return (store or SessionStore()).engine.overview(case_id, mode)


def create_session(case_id=None, store=None, mode="plain"):
    """Create a session and return its initial state."""
    if not case_id:
        raise ValueError("case_id es obligatorio")
    selected_store = store or SessionStore()
    session_id = selected_store.create(case_id, mode)
    return {"session_id": session_id, **selected_store.get(session_id).state()}


def get_session_state(session_id, store, mode=None):
    """Read the current session state."""
    return store.get(session_id).state(mode)


def set_view_mode(session_id, mode, store):
    """Set a session display mode."""
    if mode not in ("plain", "math"):
        raise ValueError("mode debe ser plain o math")
    expedition = store.get(session_id)
    expedition.mode = mode
    return expedition.state()


def submit_quest(session_id, body, store):
    """Submit ranked fears and subjective concerns."""
    return store.get(session_id).submit_quest(
        body.get("ranked_concerns", []), body.get("subjective_concern", ""))


def submit_cordada(session_id, body, store):
    """Submit one blind partner vote."""
    vote = {key: value for key, value in body.items() if key != "partner"}
    return store.get(session_id).submit_vote(body.get("partner"), **vote)


def get_mountain_state(session_id, store, mode=None):
    """Read the mountain state after the required phases."""
    expedition = store.get(session_id)
    expedition._require_mountain()
    return expedition.state(mode)


def preview_camp_decision(session_id, body, store):
    """Preview a camp decision."""
    if not body or not body.get("option_id"):
        raise ValueError("option_id es obligatorio")
    return store.get(session_id).preview(
        body["option_id"], body.get("camp_id"))


def decide_camp(session_id, body, store):
    """Commit a decision at the active camp."""
    return store.get(session_id).decide(
        body.get("option_id"), body.get("camp_id"),
        body.get("partner_choices"), body.get("send_to_advisor_brief", False),
        body.get("advisor_question"))


def rewind_session(session_id, store):
    """Rewind the currently blocked session."""
    return store.get(session_id).rewind()


def get_mountain_overview(session_id, store, mode=None):
    """Return the non-destructive full expedition map."""
    return store.get(session_id).overview(mode)


def restart_expedition(session_id, store):
    """Restart an expedition from Quest."""
    return store.get(session_id).restart()


def get_advisor_brief(session_id, store, mode=None):
    """Build the advisor brief for a session."""
    return store.get(session_id).advisor_brief(mode)


def _response_for(method, path, body, query, store):
    """Dispatch one normalized HTTP request."""
    if method == "OPTIONS":
        return 204, {}
    parsed = urlparse(path)
    query_values = parse_qs(parsed.query)
    if isinstance(query, str):
        query_values.update(parse_qs(query))
    elif isinstance(query, dict):
        query_values.update({key: [value] for key, value in query.items()})
    mode = query_values.get("mode", [None])[0]
    parts = [part for part in parsed.path.split("/") if part]
    payload = body or {}
    if method == "GET" and parts == ["health"]:
        return 200, {"status": "ok"}
    if method == "GET" and parts == ["api", "cases"]:
        return 200, {"cases": list_cases(store)}
    if method == "GET" and len(parts) == 3 and parts[:2] == ["api", "cases"]:
        return 200, get_case_overview(parts[2], store, mode)
    if method == "POST" and parts == ["api", "sessions"]:
        return 201, create_session(payload.get("case_id"), store,
                                   payload.get("mode", mode or "plain"))
    if len(parts) < 3 or parts[:2] != ["api", "sessions"]:
        return 404, {"error": "not_found", "message": "Ruta no encontrada"}
    session_id = parts[2]
    tail = parts[3:]
    if not tail and method == "GET":
        return 200, get_session_state(session_id, store, mode)
    if tail == ["mode"] and method in ("POST", "PATCH"):
        return 200, set_view_mode(session_id, payload.get("mode", mode), store)
    if tail == ["quest"] and method == "POST":
        return 200, submit_quest(session_id, payload, store)
    if tail == ["cordada"] and method == "POST":
        return 200, submit_cordada(session_id, payload, store)
    if tail == ["mountain"] and method == "GET":
        return 200, get_mountain_state(session_id, store, mode)
    if tail == ["mountain", "preview"] and method == "POST":
        return 200, preview_camp_decision(session_id, payload, store)
    if tail == ["mountain", "decide"] and method == "POST":
        return 200, decide_camp(session_id, payload, store)
    if tail == ["mountain", "rewind"] and method == "POST":
        return 200, rewind_session(session_id, store)
    if tail == ["mountain", "overview"] and method == "GET":
        return 200, get_mountain_overview(session_id, store, mode)
    if tail == ["mountain", "restart"] and method == "POST":
        return 200, restart_expedition(session_id, store)
    if tail == ["advisor-brief"] and method == "GET":
        return 200, get_advisor_brief(session_id, store, mode)
    return 404, {"error": "not_found", "message": "Ruta no encontrada"}


def dispatch_request(method, path, body=None, query=None, store=None):
    """Return an HTTP status and JSON-compatible response payload."""
    selected_store = store or SessionStore()
    with selected_store.lock:
        try:
            return _response_for(
                method.upper(), path, body, query, selected_store
            )
        except KeyError as error:
            return 404, {"error": "not_found", "message": str(error)}
        except (PhaseOrderError, ActionBlockedError) as error:
            return 409, {"error": type(error).__name__, "message": str(error)}
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            return 400, {"error": "bad_request", "message": str(error)}


def _json_response(status, data):
    """Serialize a response and add shared CORS headers."""
    payload = json.dumps(data, default=str).encode("utf-8")
    return payload, [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(payload))),
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS"),
        ("Access-Control-Allow-Headers", "Content-Type"),
    ]


def create_wsgi_app(store=None):
    """Create a dependency-free WSGI application."""
    selected_store = store or SessionStore()

    def app(environ, start_response):
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")
        query = environ.get("QUERY_STRING", "")
        content_length = int(environ.get("CONTENT_LENGTH") or 0)
        if content_length:
            raw_body = environ["wsgi.input"].read(content_length)
        else:
            raw_body = b"{}"
        try:
            body = json.loads(raw_body or b"{}")
        except (ValueError, TypeError):
            body = {}
        status, data = dispatch_request(
            method, path, body, query, selected_store
        )
        payload, headers = _json_response(status, data)
        phrases = {
            200: "OK", 201: "Created", 204: "No Content",
            400: "Bad Request", 404: "Not Found", 409: "Conflict",
        }
        start_response(f"{status} {phrases.get(status, 'Error')}", headers)
        return [payload]

    return app


wsgi_app = create_wsgi_app()


def create_http_server(host="127.0.0.1", port=0, store=None):
    """Create a threaded HTTP server backed by the service dispatcher."""
    selected_store = store or SessionStore()

    class Handler(BaseHTTPRequestHandler):
        """Adapt HTTP requests to the shared dispatcher."""

        def _handle(self):
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length:
                raw_body = self.rfile.read(content_length)
            else:
                raw_body = b"{}"
            try:
                body = json.loads(raw_body or b"{}")
            except (ValueError, TypeError):
                body = {}
            status, data = dispatch_request(
                self.command, self.path, body, None, selected_store)
            payload, headers = _json_response(status, data)
            self.send_response(status)
            for name, value in headers:
                self.send_header(name, value)
            self.end_headers()
            if payload:
                self.wfile.write(payload)

        do_GET = _handle
        do_POST = _handle
        do_PATCH = _handle
        do_OPTIONS = _handle

        def log_message(self, format_string, *args):
            return

    return ThreadingHTTPServer((host, port), Handler)


def create_fastapi_app(store=None):
    """Create a FastAPI adapter when FastAPI is installed."""
    try:
        from fastapi import FastAPI, Request
        from fastapi.responses import JSONResponse
    except ImportError:
        return None
    selected_store = store or SessionStore()
    app = FastAPI()

    @app.api_route("/{path:path}", methods=["GET", "POST", "PATCH", "OPTIONS"])
    async def route(path: str, request: Request):
        try:
            body = await request.json()
        except (ValueError, TypeError):
            body = {}
        status, data = dispatch_request(
            request.method, f"/{path}", body, dict(request.query_params),
            selected_store)
        return JSONResponse(
            data, status_code=status,
            headers={"Access-Control-Allow-Origin": "*"})

    return app


def main():
    """Start the local threaded HTTP server."""
    create_http_server().serve_forever()


if __name__ == "__main__":
    main()
