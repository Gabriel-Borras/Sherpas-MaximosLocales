"""Entrada de Vercel: la API de Sherpa Basecamp como función Python.

Vercel sirve ``frontend/`` como estático y redirige ``/api/*`` y ``/health`` aquí
(ver ``vercel.json``). Reutiliza el mismo manejador que el servidor local
(``backend.server.make_handler``), así que no hay lógica duplicada.

Nota: en serverless el estado en memoria (salas de pareja, runs IRL) no se comparte
entre invocaciones; la web ya tiene respaldo local para esas partes, y el modo
Día a Día y los botones de La Radio son sin estado.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.server import DEFAULT_FRONTEND_DIR, ServerState, make_handler  # noqa: E402

handler = make_handler(ServerState(), DEFAULT_FRONTEND_DIR)
