"""Entrada de Vercel: la API de Sherpa Basecamp como función Python.

Vercel sirve ``frontend/`` como estático y redirige ``/api/*`` y ``/health`` aquí
(ver ``vercel.json``). Reutiliza el mismo manejador que el servidor local
(``backend.server.make_handler``), así que no hay lógica duplicada.

Nota: en serverless el estado en memoria (salas de pareja, runs IRL) no se comparte
entre invocaciones; la web ya tiene respaldo local para esas partes, y el modo
Día a Día y los botones de La Radio son sin estado.
"""

import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.server import DEFAULT_FRONTEND_DIR, ServerState, make_handler  # noqa: E402

_Shared = make_handler(ServerState(), DEFAULT_FRONTEND_DIR)


class handler(BaseHTTPRequestHandler):  # nombre y base que exige el runtime de Python de Vercel
    pass


# Copia los métodos del manejador compartido (todos funcionan sobre cualquier
# subclase de BaseHTTPRequestHandler; el estado va en el cierre de make_handler).
for _name, _value in vars(_Shared).items():
    if not _name.startswith("__"):
        setattr(handler, _name, _value)
