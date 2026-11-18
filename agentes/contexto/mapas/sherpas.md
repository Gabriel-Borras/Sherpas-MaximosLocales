<!-- fuente: frontend/ | fecha: 2026-11-18 | git HEAD: 55254c7 -->
# Mapa Compacto del Repositorio â€” Sherpa Basecamp Ã— Run IRL

> Reemplaza la lectura completa de `frontend/` (~783 KB / ~196k tokens; ~31.9k tokens sin `cases-data.js`) en ~961 tokens.

## 1. Frontend (`frontend/`, rediseÃ±o `#44`/`#46`)
| Archivo | TamaÃ±o | Responsabilidad y exports clave |
| :--- | :---: | :--- |
| `frontend/index.html` | ~1 KB | Shell HTML mÃ­nimo: `<div id="app"></div>`, carga `cases-data.js`, `expedicion.js`, `post-cima.js` y llama `SherpaCasesData.loadCaseData('michael-carter')` -> `SherpaPostCima.mount('#app', ...)`. |
| `frontend/cases-data.js` | ~655 KB | `window.SherpaCasesData` (`CASE_IDS`, `CASES_DATA`, `listCases()`, `getCaseData(id)`, `loadCaseData(id)` con `fetch('/api/cases/'+id)` y fallback embebido). 4 casos literales + 11 shocks. **NO leer completo; usar `agentes/contexto/docs/casos-literales.md`.** |
| `frontend/expedicion.js` | ~96 KB | `window.SherpaExpedicion` (`listCases`, `getScenario`, `createInitialState`, `render`, `renderHeader`, `mount`, `biomes`, `svgMarkup`, `yearlyMarkup`, `localizeData`, `viewName`, `viewKey`, `text`, `thermoLabels`, `buildContrastSummary`, `buildThermometerReframe`, `orderedTopMoves`, `failTags`, `persistLanguage`, `SherpasAI` con `/api/ai/reframe|pact|brief` y respaldo humano ES/EN, `runCamera`, `campCamera`, `fullCamera`, `isMountainPhase`, `handleMountainAction`, `preview`, `riskRecord`, `strictCasePayload`). Fase 1A en `.eval-overlay` centrado 2 columnas con Top-3 (`1Âº, 2Âº, 3Âº`), termÃ³metro emocional (1â€“5), modo pareja unificado Aâ†’B a ciegas, Contraste pre-Basecamp (`#1` enfoca primer nodo sin alterar rama roja `yearly`) y aguada *sumi-e* `100vwÃ—100vh` permanente. |
| `frontend/post-cima.js` | ~28 KB | `window.SherpaPostCima` (`createInitialState`, `render`, `mount`, `makeIcs`). Usa `expedition.renderHeader`, `buildContrastSummary` y wallpaper `100vwÃ—100vh` permanente con `.floating-panel.post-view`: `current` (`DÃ­a X` IRL + recap Top-3/termÃ³metro/contraste + `documentedInertia` literal), `radio` (`.ics` + 11 shocks), `brief` (Top-3, termÃ³metro, contraste, diagnÃ³stico pareja `D4Human` y `/api/ai/brief`) y `<details class="exact-math">`. |
| `frontend/styles.css` | ~21 KB | Paleta sumi-e (`#FBF9F5`, `#141419`, `#4565d6`, `#C83A2B`), `.site-header.header-floating`, `.micro-pillars`/`.micro-bar`/`.micro-pillar-popover`, `.nav-tab`, `.nav-icon-btn`, `.mountain-stage.mountain-fullscreen`, `.eval-overlay`, `.concerns-grid` (2 cols), `.concern-card`/`.rank-badge`, `.thermometer-pills`, `.couple-turn-banner`, `.contrast-grid`, `.focus-priority-pill`, `.floating-panel`, `.floating-dialog`, `.exact-math`, `.risk-path`/`.risk-node`, `.crack-grid`. |

## 2. Backend determinista + LLM Proxy (`origin/feat/unified-api-server` @ `cfc8334`, PR `#15`)
| Rama / PR | MÃ³dulo | Endpoints / Contrato (`backend/server.py`, `81/81` tests en `cfc8334`) |
| :--- | :--- | :--- |
| `feat/issue-2-mcp-client` (`#10`) | `backend/mcp_client.py` | `list_cases()`, `get_case(slug)` con fallback a `cases/` (`SHERPAS_CASES_DIR`/`CASES_DIR`). |
| `feat/issue-3-timeline-engine` (`#11`) | `backend/timeline_engine.py`, `backend/api.py` | Motor determinista Basecamp: 5 pilares, `top_moves`, `yearly`, desvÃ­o en `investable_assets < 0`. |
| `feat/issue-5-irl-engine-notifications` (`#9`) | `backend/irl_engine.py`, `backend/notifications.py` | Run IRL dÃ­a a dÃ­a, coste de inercia literal, Radio `.ics` y shocks histÃ³ricos. |
| `feat/issue-4-llm-proxy-narrator` (`#8`) | `backend/llm_proxy.py`, `backend/behavioral_narrator.py` | Capa narrativa `0` inferencia (`/api/ai/reframe`, `/api/ai/pact`, `/api/ai/brief`) con rechazo de cifras no verificadas y fallback determinista sin `TEAM_KEY`. |
| `feat/unified-api-server` (`#12`/`#15`) | `backend/server.py` | Sirve `frontend/` + `GET /api/cases/{id}` (raw literal), `/api/cases/{id}/overview`, `/api/expedition/*`, `/api/irl/*`, `/api/radio/*`, `/api/ai/*` (pendiente actualizar `frontend/` desde `c842732`). |
