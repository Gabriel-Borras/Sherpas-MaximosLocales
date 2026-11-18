## Comunicación, ahorro de tokens y coordinación (común a todos los agentes)
Agentes disponibles: `orquestador`, `frontend`, `backend`, `seguridad`, `ideas`, `revisor`, `optimizador`, `compactador`. En modo Swarm, reportá en el tablón compartiendo `@menciones` solo al destinatario necesario.

### Contexto compartido (`agentes/contexto/`)
- `mapas/<proyecto>.md` — mapa del repo (árbol, módulos, funciones clave, endpoints)
- `docs/<tema>.md` — documentos y datos compactados (ej. cifras literales de `cases-data.js`)
- `prompts/<agente>.md` — prompts comprimidos
- `INDEX.md` — tabla índice (`ruta | fuente | fecha | ~tokens | resumen`)

### Reglas estrictas para ahorrar tokens
1. **Antes de leer un archivo grande** (`frontend/cases-data.js` de ~655 KB, `docs/BIBLIA_FINAL_V1.md`, PDFs o repos enteros), mirá primero `agentes/contexto/INDEX.md`. Si existe entrada `ok` (verificable con `python agentes/bin/contexto-check`), leé SOLO el archivo compacto de `agentes/contexto/`.
2. Si falta o está `VIEJA`, pedilo al optimizador con `PEDIR-CONTEXTO: <qué> | fuente: <ruta> | para: <agente>` y esperá `CONTEXTO-LISTO`. Leé el archivo fuente entero solo si el optimizador confirma que es imprescindible o estás editando un fragmento concreto por rango de líneas.
3. Mensajes cortos: mandá rutas, hashes o `#seq`, nunca pegues archivos completos en el tablón.
4. Revisá tu consumo con `python agentes/bin/tokens` (`--por agente` / `--sesion <id>`). Si el contexto pasa de ~150k tokens, avisá para ejecutar `python agentes/bin/compactar <id>`.

### Reglas del proyecto Sherpa Basecamp × Run IRL
1. **100 % determinista y 0 inferencia / 0 AI Proxy:** Prohibido llamar a `/api/ai/*`, `TEAM_KEY` o inventar/interpolar cifras fuera de `cases/*.json` o `frontend/cases-data.js`.
2. **Todo sobre Git, sin tocar el núcleo de la máquina:** Prohibido modificar configuraciones globales del SO (`~/.codex`, timers globales, etc.). Trabajá exclusivamente en ramas Git del repositorio con commits y push frecuentes.
3. **Naming:** `Sherpa Basecamp × Run IRL` (evitar `Living Timeline`).

### Herramientas compartidas (`agentes/bin/`)
- **Bloqueos (`bloqueo`):** antes de editar archivos compartidos, `python agentes/bin/bloqueo tomar <ruta> --como <tu_nombre>` (falla con exit 1 si otro agente lo tiene); al terminar, `bloqueo soltar <ruta> --como <tu_nombre>`.
- **Contexto (`contexto-check`):** `python agentes/bin/contexto-check --pedir` detecta resúmenes desactualizados respecto a Git.
- **Consumo y compactación (`tokens`, `compactar`):** medición local en solo lectura y exportación extractiva.
- **Tablero y equipo (`tareas`, `equipo`):** `tareas tomar/listo/ls` y `equipo mias/avisar/publicar`.
