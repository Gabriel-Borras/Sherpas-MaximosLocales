<!-- fuente: frontend/ | fecha: 2026-11-18 | git HEAD: c842732 -->
# Mapa Compacto del Repositorio — Sherpa Basecamp × Run IRL

> Reemplaza la lectura completa de `frontend/` (~783 KB / ~196k tokens; ~31.9k tokens sin `cases-data.js`) en ~961 tokens.

## 1. Frontend (`frontend/`, rediseño `#44`/`#46`)
| Archivo | Tamaño | Responsabilidad y exports clave |
| :--- | :---: | :--- |
| `frontend/index.html` | ~1 KB | Shell HTML mínimo: `<div id="app"></div>`, carga `cases-data.js`, `expedicion.js`, `post-cima.js` y llama `SherpaCasesData.loadCaseData('michael-carter')` -> `SherpaPostCima.mount('#app', ...)`. |
| `frontend/cases-data.js` | ~655 KB | `window.SherpaCasesData` (`CASE_IDS`, `CASES_DATA`, `listCases()`, `getCaseData(id)`, `loadCaseData(id)` con `fetch('/api/cases/'+id)` y fallback embebido). 4 casos literales + 11 shocks. **NO leer completo; usar `agentes/contexto/docs/casos-literales.md`.** |
| `frontend/expedicion.js` | ~85 KB | `window.SherpaExpedicion` (`listCases`, `getScenario`, `createInitialState`, `render`, `renderHeader`, `mount`, `biomes`, `svgMarkup`, `yearlyMarkup`, `localizeData`, `viewName`, `viewKey`, `text`, `failTags`, `persistLanguage`, `SherpasAI` stub determinista, `runCamera`, `campCamera`, `fullCamera`, `isMountainPhase`, `handleMountainAction`, `preview`, `riskRecord`, `strictCasePayload`). Aguada *sumi-e* `100vw×100vh` permanente (`fullCamera=[0,0,1200,750]`), cabecera única con 5 `.micro-pillar` + 2 pestañas (`Basecamp`, `Día X`) + 2 iconos (`Brief`, `Radio`), `.floating-panel` + `<details class="exact-math">`, `#climberMarker` punto limpio, rutas rojas persistentes (`riskCoordinates` en `yearly.investable_assets < 0`) con `.risk-node` inspeccionables (`renderRiskInspectionCard`) y zoom RAF. |
| `frontend/post-cima.js` | ~27 KB | `window.SherpaPostCima` (`createInitialState`, `render`, `mount`, `makeIcs`). Usa `expedition.renderHeader` y wallpaper `100vw×100vh` permanente con `.floating-panel.post-view` (sin `.post-mountain`): `current` (`Día X` IRL + `documentedInertia` literal), `radio` (`.ics` + 11 shocks), `brief` y `<details class="exact-math">`. Sin toggle `Simple/Métricas` ni llamadas a `/api/ai/*`. |
| `frontend/styles.css` | ~15 KB | Paleta sumi-e (`#FBF9F5`, `#141419`, `#4565d6`, `#C83A2B`), `.site-header.header-floating`, `.micro-pillars`/`.micro-bar`/`.micro-pillar-popover`, `.nav-tab`, `.nav-icon-btn`, `.mountain-stage.mountain-fullscreen`, `.sumi-wash`/`.sumi-ridge-soft`, `.floating-panel`, `.floating-dialog`, `.exact-math`, `.risk-path`/`.risk-node`, `.crack-grid`. |

## 2. Backend determinista + LLM Proxy (`origin/feat/unified-api-server` @ `cfc8334`, PR `#15`)
| Rama / PR | Módulo | Endpoints / Contrato (`backend/server.py`, `81/81` tests en `cfc8334`) |
| :--- | :--- | :--- |
| `feat/issue-2-mcp-client` (`#10`) | `backend/mcp_client.py` | `list_cases()`, `get_case(slug)` con fallback a `cases/` (`SHERPAS_CASES_DIR`/`CASES_DIR`). |
| `feat/issue-3-timeline-engine` (`#11`) | `backend/timeline_engine.py`, `backend/api.py` | Motor determinista Basecamp: 5 pilares, `top_moves`, `yearly`, desvío en `investable_assets < 0` y reordenación dinámica de `camps`, opción principal y `active_camp` según el miedo Top-1 (`ranked_concerns[0]` / `fear_ranking[0]`) en `Expedition.__init__`, `submit_quest`, `POST /api/sessions` y `POST /api/sessions/{id}/quest` (desde orden base sin inventar cifras ni mover campamentos de cima). |
| `feat/issue-5-irl-engine-notifications` (`#9`) | `backend/irl_engine.py`, `backend/notifications.py` | Run IRL día a día, coste de inercia literal, Radio `.ics` y shocks históricos. |
| `feat/issue-4-llm-proxy-narrator` (`#8`) | `backend/llm_proxy.py`, `backend/behavioral_narrator.py` | Capa narrativa `0` inferencia (`/api/ai/reframe`, `/api/ai/pact`, `/api/ai/brief`) con rechazo de cifras no verificadas y fallback determinista sin `TEAM_KEY`. |
| `feat/unified-api-server` (`#12`/`#15`) | `backend/server.py` | Sirve `frontend/` + `GET /api/cases/{id}` (raw literal), `/api/cases/{id}/overview`, `/api/expedition/*` (delegado a `backend/api.py` con reordenación Top-1 en `/api/expedition` y `/api/expedition/{id}/quest`), `/api/irl/*`, `/api/radio/*`, `/api/ai/*` (pendiente actualizar `frontend/` desde `c842732`). |
