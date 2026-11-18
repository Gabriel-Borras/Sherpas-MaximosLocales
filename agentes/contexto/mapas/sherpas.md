<!-- fuente: frontend/ | fecha: 2026-11-18 | git HEAD: 89b4d8c -->
# Mapa Compacto del Repositorio — Sherpa Basecamp × Run IRL

> Reemplaza la lectura completa de `frontend/` (~740 KB / ~185k tokens) en ~600 tokens.

## 1. Frontend (`frontend/`)
| Archivo | Tamaño | Responsabilidad y exports clave |
| :--- | :---: | :--- |
| `frontend/index.html` | ~1 KB | Shell HTML mínimo: `<div id="app"></div>`, carga `cases-data.js`, `expedicion.js`, `post-cima.js` y llama `SherpaCasesData.loadCaseData('michael-carter')` -> `SherpaPostCima.mount('#app', ...)`. |
| `frontend/cases-data.js` | ~655 KB | `window.SherpaCasesData` (`CASE_IDS`, `CASES_DATA`, `listCases()`, `getCaseData(id)`, `loadCaseData(id)` con `fetch('/api/cases/'+id)` y fallback embebido). Contiene los 4 casos literales + 11 shocks. **NO leer completo; consultar `agentes/contexto/docs/casos-literales.md`.** |
| `frontend/expedicion.js` | ~44 KB | `window.SherpaExpedicion` (`listCases`, `getScenario`, `createInitialState`, `render`, `mount`, `biomes`, `svgMarkup`, `yearlyMarkup`, `localizeData`, `viewName`, `viewKey`, `text`, `failTags`, `persistLanguage`, `SherpasAI` stub local determinista, `runCamera`, `riskRecord`, `strictCasePayload`). Fase 1A (Fears), 1B (Cordada 60s), Cross-check, Fase 2 (Montaña sumi-e SVG + cámara `requestAnimationFrame` + desvío rojo estricto en `yearly.investable_assets < 0`). |
| `frontend/post-cima.js` | ~24 KB | `window.SherpaPostCima` (`createInitialState`, `render`, `mount`, `makeIcs`). Modo Enfoque (`current` IRL Día 0/3/14/30/Hito con `documentedInertia` literal), Vista General (`overview`), La Radio del Sherpa (`radio` + `.ics` + 11 shocks), Advisor Brief (`brief`). Cero llamadas al AI Proxy. |
| `frontend/styles.css` | ~11 KB | Paleta editorial sumi-e (`#FBF9F5`, `#141311`, `#4565d6`, `#C83A2B` riesgo), `.mountain-stage` full-bleed (`100vw`, `min-height: min(72vh,720px)`), `.mountain-svg`, `.storm-shake`, `.risk-path`, responsive `<900px`. Sin badge `Lydia AI`. |

## 2. Backend determinista (PRs en GitHub `#10`, `#11`, `#9` + Issue `#12` en progreso por Sabater)
| Rama / PR | Módulo previsto | Endpoints / Contrato objetivo (`backend/server.py`, sin `#8` AI Proxy) |
| :--- | :--- | :--- |
| `feat/issue-2-mcp-client` (`#10`) | `backend/mcp_client.py` | `list_cases()`, `get_case(slug)` con fallback a `cases/` (`SHERPAS_CASES_DIR`/`CASES_DIR`). |
| `feat/issue-3-timeline-engine` (`#11`) | `backend/timeline_engine.py`, `backend/api.py` | Motor determinista Basecamp: 5 pilares, `top_moves`, `yearly`, desvío en `investable_assets < 0`. |
| `feat/issue-5-irl-engine-notifications` (`#9`) | `backend/irl_engine.py` | Run IRL día a día, coste de inercia literal, Radio `.ics` y shocks históricos. |
| `feat/unified-api-server` (`#12`) | `backend/server.py` | Sirve `frontend/` estático + `GET /api/cases`, `GET /api/cases/{id}`, `/api/expedition`, `/api/irl`, `/api/radio` (100% determinista). |
