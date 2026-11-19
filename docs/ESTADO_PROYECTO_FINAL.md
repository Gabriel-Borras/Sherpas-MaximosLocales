# Estado Integral del Proyecto — Sherpa Basecamp × Run IRL

Documento oficial del estado real del sistema tras la integración de los PRs `#8`, `#9`, `#10`, `#11`, `#14` (`d789463`), `#15` (`cd4924f`, `9a46224`+) y la coordinación con `#16` (`fdc88a3`) y `#17` (`1862793`).

> **Principio rector (0 inferencia / 0 cifras inventadas):** Toda cifra, edad, importe, hito, score y shock del sistema procede literalmente de los JSON oficiales de cada caso (`cases/*.json` / MCP / fallback embebido). La capa narrativa opcional (`/api/ai/*`) solo traduce o reformula datos verificados y cuenta con fallback determinista instantáneo.

---

## 1. Arquitectura y Flujo de Datos

```text
Navegador (1 o 2 dispositivos en pareja)
  │  frontend/index.html + expedicion.js + post-cima.js + cases-data.js + styles.css
  │  + frontend/assets/mountain-sumi.jpg
  ▼
backend/server.py (ThreadingHTTPServer stdlib, CORS *, UTF-8 sin BOM)
  ├── Estáticos: GET / -> frontend/index.html, /assets/*, /*.js, /*.css
  ├── Casos literales:
  │     ├── GET /api/cases                    -> backend/mcp_client.py (list_cases)
  │     ├── GET /api/cases/{id}               -> JSON literal completo (compatible cases-data.js)
  │     └── GET /api/cases/{id}/overview      -> backend/api.py / timeline_engine.py (plain|math)
  ├── Expedición Basecamp:
  │     └── /api/sessions/* y /api/expedition/* -> backend/api.py + backend/timeline_engine.py
  ├── Salas Multi-Dispositivo de Pareja (en memoria, thread-safe):
  │     └── /api/rooms, /api/rooms/{id}, /evaluation, /decision
  ├── Run IRL + La Radio del Sherpa:
  │     ├── /api/irl/*                        -> backend/irl_engine.py (Día 0/3/14/30, inercia)
  │     └── /api/radio/* y /api/radio/{id}/ics -> backend/notifications.py (milestones, 11 shocks, .ics)
  ├── Capa Narrativa Opcional (0 inferencia + fallback determinista):
  │     └── POST /api/ai/reframe | /pact | /brief -> backend/behavioral_narrator.py + backend/llm_proxy.py
  └── Webhook Saliente Opcional (no bloqueante, hilo daemon, timeout 2s):
        └── N8N_WEBHOOK_URL -> n8n -> Telegram / canales externos
```

---

## 2. Estado Real por Bloque Funcional

### 2.1 Evaluación Fase 1A (Ultra-Simple y Persistente)
- **Interfaz (`frontend/expedicion.js`, `frontend/styles.css`):** rejilla centrada de 2 columnas mostrando todas las tarjetas de preocupación de golpe (sin termómetro, sin campo de duda opcional, sin botones `+ Ver X más`).
- **Ranking Top-3 (`1º / 2º / 3º`):** selección directa de prioridades en lenguaje 100% cotidiano ES/EN (sin jerga financiera ni etiquetas técnicas).
- **Persistencia por perfil (`ProfileEvalStore`):** guarda la evaluación en `localStorage` para que solo se solicite la primera vez; al recargar entra directo en la montaña, con botón **"Rehacer evaluación"** disponible en el panel de *Brief* (`frontend/post-cima.js`).

### 2.2 Montaña *Sumi-e* Monocromática
- **Arte real integrado:** `frontend/assets/mountain-sumi.jpg` montado dentro de `#cameraRig` con `mix-blend-mode: multiply` sobre fondo `#ffffff` y filtro SVG `#dryBrush`.
- **Nodos y cámara:** 4 nodos alineados sobre la cresta (`[312,491]`, `[564,382]`, `[684,319]`, `[858,145]` con la bandera Sherpas en la cima) y zoom suavizado (`660×412` / `696×435`).
- **Estado inicial limpio:** en `stage = 0` no se muestra ningún trazo rojo ni recorrido pre-pintado por delante; en vista panorámica aparece el botón circular de campamento.

### 2.3 Cards de Decisión y Ramas Rojas 1:1
- **Cards translúcidas sin spoilers:** ancladas abajo-derecha (`rgba(255,255,255,0.72)` con `backdrop-filter: blur(10px)`), texto mínimo y ambas opciones visualmente neutras (sin rojo anticipado ni badge `X→Y`), con alternativa cotidiana de *statu quo* y orden alterno.
- **Ramas rojas sincronizadas:** `.risk-path` y `.route-ink` usan `pathLength="1000"` sin `non-scaling-stroke`, manteniendo sincronización 1:1 con `#climberMarker` bajo cualquier zoom.

### 2.4 Parejas Multi-Dispositivo (`CoupleRoomSync` + `couple-split`)
- **Backend (`/api/rooms/*` en `backend/server.py`, commit `5ca9bae`):** estado en memoria thread-safe dentro de `ServerState`, genérico para cualquier caso de pareja y con CORS abierto (`*`):
  - `POST /api/rooms` (`{ case_id }`) → crea sala y devuelve `room_id`, `case_id`, `share_query` (`?case=<id>&room=<room_id>&member=B`), `evaluation: {A: null, B: null}`, `evaluation_ready: false`, `decisions: {}`.
  - `GET /api/rooms/{room_id}` → estado completo de evaluaciones y decisiones por campamento (`0..3`).
  - `POST /api/rooms/{room_id}/evaluation` (`member: "A"|"B"`, `top_fears`, `thermometer`, `priority`, `subjective`) → marca `evaluation_ready: true` al recibir ambos.
  - `POST /api/rooms/{room_id}/decision` (`member: "A"|"B"`, `stage`, `route: "good"|"bad"`, `label`) → marca `ready: true` y `aligned: (A.route === B.route)` cuando ambos votan en el mismo `stage`.
- **Frontend (`frontend/expedicion.js`, commit `dc8616b` / `d789463`):** `CoupleRoomSync` sincroniza vía `/api/rooms/*` (con fallback local por `BroadcastChannel`/`localStorage`). Cuando A y B divergen en una decisión, `#climberMarkerA` y `#climberMarkerB` ejecutan la animación bifurcada simultánea (`couple-split`), recorriendo a la vez la cresta segura y la rama roja hasta **Reunir cordada y avanzar** o **Rebobinar**.

### 2.5 Notificaciones, Webhooks n8n y Propuesta Telegram
- **Webhook saliente a n8n (`N8N_WEBHOOK_URL`, commit `9a46224`):**
  - Configurado opcionalmente mediante variable de entorno o `.env` (documentado vacío en `.env.example`; `no-op` silencioso si no está definido).
  - Helper `_emit_n8n_webhook(payload)` en `backend/server.py` usando `urllib.request`, timeout corto (`2s`), `try/except` y ejecución en hilo `daemon` para no bloquear ni romper nunca la API si n8n no responde.
  - Disparado automáticamente en:
    - `POST /api/irl/{run_id}/advance` y `POST /api/irl/{run_id}/check`: emite las notificaciones de hitos generadas por `NotificationEngine.generate_milestone_notifications(engine)`.
    - `POST /api/radio/{identifier}/shock`: emite la alerta de shock macro generada por `NotificationEngine.generate_macro_shock_notification(...)`.
- **Botón "Conectar a Telegram" (Deep Linking en `frontend/post-cima.js`):**
  - Implementado en el panel de **La Radio del Sherpa** junto a **Descargar calendario `.ics`** con enlace directo `https://t.me/SherpasRadioBot?start=${state.caseId || 'demo'}_${state.voters ? state.voters[0] : 'client'}` (`target="_blank"`), vinculando `chat_id` en n8n al pulsar *Start*. Documentado en el Momento 4 de `docs/DEMO_SCRIPT.md`.

---

## 3. Mapa de Ramas, Módulos y PRs

| PR / Rama | Responsable | Estado | Contenido principal |
| :--- | :---: | :---: | :--- |
| **PR #10** (`feat/issue-2-mcp-client`) | Sabater | Integrado en `#15` | `backend/mcp_client.py` (`list_cases`, `get_case`, fallback `cases/`/`SHERPAS_CASES_DIR`/`CASES_DIR` + seed). |
| **PR #11** (`feat/issue-3-timeline-engine`) | Sabater | Integrado en `#15` | `backend/timeline_engine.py`, `backend/api.py` (motor determinista Basecamp, 5 pilares, cordada, rewind). |
| **PR #9** (`feat/issue-5-irl-engine-notifications`) | Juan | Integrado en `#15` | `backend/irl_engine.py`, `backend/notifications.py` (Run IRL Día 0/3/14/30, inercia literal, `.ics`, 11 shocks). |
| **PR #8** (`feat/issue-4-llm-proxy-narrator`) | Juan | Integrado en `#15` | `backend/llm_proxy.py`, `backend/behavioral_narrator.py` (capa narrativa 0 inferencia + fallback sin `TEAM_KEY`). |
| **PR #13 / #14** (`feat/issue-7-frontend-post-cima` @ `d789463`) | Gabriel → Juan | Integrado en `#15` | `frontend/*` (Fase 1A ultra-simple, `mountain-sumi.jpg`, cards neutras, `CoupleRoomSync`, `couple-split`, Post-Cima). |
| **PR #15** (`feat/unified-api-server`) | Sabater | Activo (`89/89` tests OK) | `backend/server.py` + `tests/test_server.py`: servidor unificado, `/api/cases/*`, `/api/expedition/*`, `/api/irl/*`, `/api/radio/*`, `/api/ai/*`, `/api/rooms/*`, `N8N_WEBHOOK_URL`. |
| **PR #16** (`docs/capacidades-backend` @ `fdc88a3`) | Juan | Abierto contra `main` | `docs/CAPACIDADES_BACKEND.md`: catálogo detallado de capacidades del backend unificado. |
| **PR #17** (`feat/juan-eval-ai-e2e` @ `1862793`) | Juan | Abierto contra `#15` | `lang` ES/EN, `blind_spot_contrast`, `anxiety_gap` en `behavioral_narrator.py`, `tests/test_e2e_demo.py` (4 casos) y `docs/DEMO_SCRIPT.md`. |

---

## 4. Endpoints del Servidor Unificado (`backend/server.py`)

| Grupo | Rutas | Descripción |
| :--- | :--- | :--- |
| **Salud y estáticos** | `GET /health`, `GET /`, `GET /<asset>` | Estado del servidor y entrega segura de `frontend/` (`relative_to`, MIME types). |
| **Casos** | `GET /api/cases`, `GET /api/cases/{id}`, `GET /api/cases/{id}/overview` | Catálogo oficial, JSON literal completo compatible con `cases-data.js` y resumen `plain`/`math`. |
| **Expedición / Basecamp** | `POST /api/expedition`, `GET /api/expedition/{id}`, `POST .../quest\|cordada\|preview\|decide\|rewind\|restart`, `GET .../overview\|advisor-brief`, `/api/sessions/*` | Ciclo completo de expedición determinista. |
| **Salas de pareja** | `POST /api/rooms`, `GET /api/rooms/{room_id}`, `POST .../evaluation`, `POST .../decision` | Sincronización multi-dispositivo A/B para evaluación y campamentos `0..3`. |
| **Run IRL** | `POST /api/irl`, `GET /api/irl/{run_id}`, `POST .../check\|uncheck\|advance\|repeat`, `GET .../inertia` | Progresión Día 0/3/14/30, coste de inercia literal y disparo de webhook n8n en `advance`/`check`. |
| **La Radio del Sherpa** | `GET /api/radio`, `GET /api/radio/{id}`, `POST /api/radio/{id}/shock`, `GET /api/radio/{run_id}/ics` | Shocks históricos, milestones, exportación `.ics` (`text/calendar`) y webhook n8n en `shock`. |
| **Capa narrativa (opcional)** | `POST /api/ai/reframe`, `POST /api/ai/pact`, `POST /api/ai/brief` | Reformulación con rechazo de cifras inventadas y fallback determinista instantáneo sin `TEAM_KEY`. |

---

## 5. Arranque y Verificación Local

```bash
# Arrancar el servidor unificado (sirve frontend/ y /api/*)
python3 -m backend.server --host 127.0.0.1 --port 8000

# Suite completa de tests unitarios (sin backend/__init__.py y UTF-8 sin BOM)
python3 -m unittest discover -s tests -v

# Validación de sintaxis del frontend
for f in frontend/*.js; do node --check "$f"; done

# Validación de frescura del contexto compacto
python3 agentes/bin/contexto-check
```
