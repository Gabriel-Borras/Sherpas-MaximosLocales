<!-- fuente: frontend/ | fecha: 2026-11-19 | git HEAD: 9e5669d -->
# Mapa Compacto del Repositorio — Sherpa Basecamp × Run IRL

> Reemplaza la lectura completa de `frontend/` (~820 KB) en ~900 tokens. Documentación integral en `docs/ESTADO_PROYECTO_FINAL.md`.

## 1. Frontend (`frontend/`, PR `#14` @ `d789463` / `dc8616b`)
| Archivo | Tamaño | Responsabilidad y exports clave |
| :--- | :---: | :--- |
| `frontend/index.html` | ~1 KB | Shell HTML mínimo (`?case=&room=&member=`): `<div id="app"></div>`, carga `cases-data.js`, `expedicion.js`, `post-cima.js` y monta `SherpaPostCima.mount('#app', ...)`. |
| `frontend/cases-data.js` | ~655 KB | `window.SherpaCasesData` (`CASE_IDS`, `CASES_DATA`, `listCases()`, `getCaseData(id)`, `loadCaseData(id)` con `fetch('/api/cases/'+id)` y fallback embebido). 4 casos literales + 11 shocks. **NO leer completo; usar `agentes/contexto/docs/casos-literales.md`.** |
| `frontend/expedicion.js` | ~112 KB | `window.SherpaExpedicion`. Fase 1A ultra-simple (rejilla centrada 2 cols con todas las tarjetas, Top-3 `1º/2º/3º`, 0 jerga, `ProfileEvalStore` en `localStorage`); montaña *sumi-e* real (`assets/mountain-sumi.jpg` + `#dryBrush`, 4 nodos en cresta, zoom `660×412`/`696×435`, 0 trazos rojos en `stage=0`); cards translúcidas abajo-derecha sin spoilers; rama roja `pathLength="1000"` 1:1; `CoupleRoomSync` (`/api/rooms/*` + fallback local) con `#climberMarkerA`/`#climberMarkerB` y bifurcación simultánea `couple-split`; `SherpasAI` (`/api/ai/reframe\|pact\|brief`, timeout 1200ms + fallback humano ES/EN). |
| `frontend/post-cima.js` | ~28 KB | `window.SherpaPostCima` (`createInitialState`, `render`, `mount`, `makeIcs`): `current` (`Día X` IRL + `documentedInertia` literal), `radio` (`.ics` + 11 shocks), `brief` (resumen, botón `Rehacer evaluación` y `/api/ai/brief`) y `<details class="exact-math">`. |
| `frontend/styles.css` | ~25 KB | Paleta *sumi-e* monocromática (`#ffffff`, `#141419`, `#4565d6`, `#C83A2B`), `.eval-overlay`, `.concerns-grid`, `.floating-panel`, cards translúcidas, `.risk-path`/`.route-ink`, botón circular de campamento y marcadores A/B. |
| `frontend/assets/mountain-sumi.jpg` | ~224 KB | Arte *sumi-e* real integrado en `#cameraRig` con `mix-blend-mode: multiply`. |

## 2. Backend unificado (`origin/feat/unified-api-server`, PR `#15`, `89/89` tests OK)
| Rama / PR | Módulo | Endpoints / Contrato (`backend/server.py`) |
| :--- | :--- | :--- |
| `feat/issue-2-mcp-client` (`#10`) | `backend/mcp_client.py` | `list_cases()`, `get_case(slug)` con fallback a `cases/` (`SHERPAS_CASES_DIR`/`CASES_DIR`) y seed. |
| `feat/issue-3-timeline-engine` (`#11`) | `backend/timeline_engine.py`, `backend/api.py` | Motor determinista Basecamp: 5 pilares, `top_moves`, `yearly`, desvío en `investable_assets < 0`. |
| `feat/issue-5-irl-engine-notifications` (`#9`) | `backend/irl_engine.py`, `backend/notifications.py` | Run IRL Día 0/3/14/30, coste de inercia literal, Radio `.ics` y 11 shocks históricos. |
| `feat/issue-4-llm-proxy-narrator` (`#8`) | `backend/llm_proxy.py`, `backend/behavioral_narrator.py` | Capa narrativa `0` inferencia (`/api/ai/reframe`, `/api/ai/pact`, `/api/ai/brief`) con rechazo de cifras inventadas y fallback determinista sin `TEAM_KEY`. |
| `feat/unified-api-server` (`#12`/`#15`) | `backend/server.py` | Sirve `frontend/` + `GET /api/cases/{id}` (raw literal), `/overview`, `/api/expedition/*`, `/api/irl/*`, `/api/radio/*`, `/api/ai/*`, **salas de pareja `/api/rooms/*`** (`5ca9bae`) y **webhook saliente `N8N_WEBHOOK_URL`** no bloqueante (`9a46224`). |
| `feat/juan-eval-ai-e2e` (`#17`, Juan) | `behavioral_narrator.py`, `tests/test_e2e_demo.py`, `docs/DEMO_SCRIPT.md` | PR abierto contra `#15`: `lang` ES/EN, `blind_spot_contrast`, `anxiety_gap`, suite E2E (4 casos) y guion de demo 3 min. |
