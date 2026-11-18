<!-- fuente: frontend/ | fecha: 2026-11-18 | git HEAD: 28b16ef -->
# Mapa Compacto del Repositorio — Sherpa Basecamp × Run IRL

> Reemplaza la lectura completa de `frontend/` (~766 KB / ~191k tokens; ~27.7k tokens sin `cases-data.js`) en ~879 tokens.

## 1. Frontend (`frontend/`, orden `#92`)
| Archivo | Tamaño | Responsabilidad y exports clave |
| :--- | :---: | :--- |
| `frontend/index.html` | ~1 KB | Shell HTML mínimo: `<div id="app"></div>`, carga `cases-data.js`, `expedicion.js`, `post-cima.js` y llama `SherpaCasesData.loadCaseData('michael-carter')` -> `SherpaPostCima.mount('#app', ...)`. |
| `frontend/cases-data.js` | ~655 KB | `window.SherpaCasesData` (`CASE_IDS`, `CASES_DATA`, `listCases()`, `getCaseData(id)`, `loadCaseData(id)` con `fetch('/api/cases/'+id)` y fallback embebido). 4 casos literales + 11 shocks. **NO leer completo; usar `agentes/contexto/docs/casos-literales.md`.** |
| `frontend/expedicion.js` | ~72 KB | `window.SherpaExpedicion` (`listCases`, `getScenario`, `createInitialState`, `render`, `mount`, `biomes`, `svgMarkup`, `yearlyMarkup`, `localizeData`, `viewName`, `viewKey`, `text`, `failTags`, `persistLanguage`, `SherpasAI` stub determinista, `runCamera`, `campCamera`, `fullCamera`, `isMountainPhase`, `handleMountainAction`, `preview`, `riskRecord`, `strictCasePayload`). Fases `fears` -> `cordada` (60s) -> `cross` -> `expedition`/`blocked` (`isMountainPhase`: oculta `.left-rail`, montaña *sumi-e* `100vw × 100vh`, `fullCamera=[0,0,1200,750]`, 4 `.micro-camp` + `.sherpas-flag`, `campCamera` `8x` `150×93.75` vía `requestAnimationFrame`, `.floating-dialog` post-zoom y `.risk-path` `#C83A2B` estricto en `yearly.investable_assets < 0` + `Rewind`). |
| `frontend/post-cima.js` | ~24 KB | `window.SherpaPostCima` (`createInitialState`, `render`, `mount`, `makeIcs`). Delega fase de montaña en `handleMountainAction`/`isMountainPhase` y limpia `is-mountain-viewport` en `unmount`; formato `-$` en `money()`. Modo Enfoque (`current` IRL Día 0/3/14/30/Hito + `documentedInertia` literal), Vista General (`overview`), Radio (`radio` + `.ics` + 11 shocks), Advisor Brief (`brief`). Cero llamadas al AI Proxy. |
| `frontend/styles.css` | ~14 KB | Paleta editorial sumi-e (`#FBF9F5`, `#141419`, `#4565d6`, `#C83A2B`), `.site-header.header-floating`, `.mountain-stage.mountain-fullscreen` (`100vw × 100vh`, `body.is-mountain-viewport`), `.mountain-hud` / `.camp-pills` / `.hud-zoom-btn`, `.floating-dialog`, `.floating-overview-cta`, `.micro-camp`, `.storm-shake`, `.risk-path`, `.post-mountain`, `@media (prefers-reduced-motion)` y `<900px`. |

## 2. Backend determinista (PRs en GitHub `#10`, `#11`, `#9` + Issue `#12` por Sabater)
| Rama / PR | Módulo previsto | Endpoints / Contrato objetivo (`backend/server.py`, sin `#8` AI Proxy) |
| :--- | :--- | :--- |
| `feat/issue-2-mcp-client` (`#10`) | `backend/mcp_client.py` | `list_cases()`, `get_case(slug)` con fallback a `cases/` (`SHERPAS_CASES_DIR`/`CASES_DIR`). |
| `feat/issue-3-timeline-engine` (`#11`) | `backend/timeline_engine.py`, `backend/api.py` | Motor determinista Basecamp: 5 pilares, `top_moves`, `yearly`, desvío en `investable_assets < 0`. |
| `feat/issue-5-irl-engine-notifications` (`#9`) | `backend/irl_engine.py` | Run IRL día a día, coste de inercia literal, Radio `.ics` y shocks históricos. |
| `feat/unified-api-server` (`#12`) | `backend/server.py` | Merge `#10+#11+#9` (`ed20345`); pendiente `backend/server.py` para servir `frontend/` + `/api/cases`, `/api/expedition`, `/api/irl`, `/api/radio`. |
