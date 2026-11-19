# Sherpa Basecamp × Run IRL — Sherpas Máximos Locales

> Hackathon UPV 2026 · Reto Sherpas · **Paso 3 del asesor: *Bring the plan to life***

**Demo en vivo:** https://sherpas-maximoslocales.vercel.app  (casos: `?case=michael-carter`, `samantha-lewis`, `timothy-melanie-weah`, `daniel-emily-johnson`)

Convertimos el informe financiero de 22 páginas de Sherpas en una **expedición de montaña interactiva** que la familia hace una sola vez (menos de 90 s), conectada a una **línea de vida real** que la acompaña día a día y fuera de la app. Todo sale de los **datos reales de los 4 casos** de Sherpas (`financial-health.json`, `investment-analysis.json`, `persona.md`), **sin inventar cifras**.

## Qué hace

| Fase | Qué ve la familia | Problema de Sherpas que resuelve |
| :--- | :--- | :--- |
| **1. Quest de miedos** | Elige y ordena sus 3 preocupaciones reales (`O1..O8`). | El campo *Subjective concerns* llega vacío. |
| **2. Cordada a ciegas (parejas)** | Cada miembro vota por separado; se muestra primero en qué coinciden. | Parejas con riesgo `MISALIGNED` que no acuerdan. |
| **3. Basecamp (montaña sumi-e)** | Decide en 4 campamentos sobre la curva real `projections.yearly`. Si elige mal, la montaña **le bloquea en el año exacto** en que el plan falla y le deja **rebobinar**. | No ven cómo una decisión de hoy cambia su futuro; un buen score oculta problemas (Samantha `82` → sin liquidez en 2053). |
| **4. Salud y Tu mochila** | Pentágono de los 5 pilares y balance real, solo lectura. | Cifras grandes sin contexto. |
| **5. Día a Día (Run IRL)** | La montaña con un nodo por día (0 → 30). Cada día: **qué hacer**, **por qué** (coste real de retrasarlo) o **«hoy toca esperar»**. Se puede arrastrar y ampliar. | Demasiadas opciones sin primer paso; el plan se olvida a los 3 y 30 días. |
| **6. La Radio del Sherpa (Telegram)** | El paso de cada día y un **recordatorio cada 2 días** si algo queda pendiente. Si cae la bolsa, la caída histórica más parecida que su cartera **ya superó** (p. ej. *«En abril de 2025 tu cartera cayó un 8,1 %… te recuperaste en 61 días»*). | El pánico ante caídas y la inercia fuera de la app. |
| **7. Resumen para el asesor** | Miedos, pacto de pareja, ramas descartadas y dudas, listo para copiar. | El asesor no conoce los miedos reales. |

Fundamentación completa (sesgos conductuales, mapa de datos por caso): [`docs/BIBLIA_FINAL_V1.md`](docs/BIBLIA_FINAL_V1.md).

## Probar en 2 minutos

1. Abre la demo y elige un caso arriba a la izquierda (p. ej. *Timothy & Melanie*).
2. Elige tus 3 preocupaciones y entra al **Basecamp**; decide en los campamentos (si eliges mal, la montaña te bloquea y puedes rebobinar).
3. Pulsa **Día 0** en la barra superior: ves lo que toca hoy y por qué; avanza con **Día siguiente →** (arrastra y usa la rueda para mover/ampliar la cámara).
4. Para recibir los avisos por Telegram: abre `https://t.me/SherpasRadioBot?start=<caso>_client` y pulsa *Start* (parejas: `_A` / `_B`). Después, en el panel **📻 Radio** pulsa **📉 Cae la bolsa**.

## Ejecutar en local

Requisitos: **Python 3.10+**. Solo usa la biblioteca estándar; no hay dependencias que instalar.

```bash
python -m backend.server            # http://127.0.0.1:8000
```

Abre `http://127.0.0.1:8000/` (un caso concreto: `?case=michael-carter`, `samantha-lewis`, `timothy-melanie-weah` o `daniel-emily-johnson`).

Configuración opcional en `.env` (plantilla en [`.env.example`](.env.example), nunca se sube):

| Variable | Para qué |
| :--- | :--- |
| `MCP_URL`, `MCP_TOKEN` | Leer los casos del MCP de Sherpas. Sin token se usan los datos incluidos en el repo. Guía: [`docs/GUIA_API_IA_SHERPAS.md`](docs/GUIA_API_IA_SHERPAS.md). |
| `LLM_PROXY_URL`, `TEAM_KEY` | Capa narrativa con IA. Sin clave responde con texto determinista. |
| `N8N_WEBHOOK_URL`, `N8N_WEBHOOK_SECRET`, `TELEGRAM_BOT_USERNAME` | La Radio del Sherpa por Telegram vía n8n. |
| `SHERPAS_ENABLE_TELEGRAM_TEST=1` | Muestra el panel **📻 Radio** de demo (Día 0/3/14/30 · Cae la bolsa). |

Puesta en marcha de Telegram + n8n (flujo importable incluido): [`docs/TELEGRAM_N8N.md`](docs/TELEGRAM_N8N.md).

## Tests

```bash
python -m unittest discover -s tests          # backend (Python)
node --test tests/frontend/test_dia_a_dia.mjs n8n/test_code_nodes.mjs   # vista Día a Día y nodos de n8n
```

## Despliegue (Vercel)

- `frontend/` se publica como web estática.
- `/api/*` y `/health` van a una función Python ([`api/index.py`](api/index.py)) que reutiliza el mismo manejador que el servidor local.
- Las variables de entorno se configuran en el proyecto de Vercel, no en el repo.
- En serverless no hay memoria compartida entre peticiones. Las salas de pareja usan el respaldo local del navegador; el Día a Día y la Radio no guardan estado. Los avisos automáticos programados (`SHERPAS_SCHEDULER_INTERVAL`) solo funcionan con el servidor local.

## Estructura

```
frontend/     Web (HTML/CSS/JS sin dependencias): expedicion.js (Basecamp), post-cima.js, dia-a-dia.js, radio-demo.js
backend/      API en Python estándar: server.py, timeline_engine.py, irl_engine.py, notifications.py,
              dia_a_dia.py, radio_demo.py, telegram_relay.py, mcp_client.py, llm_proxy.py, behavioral_narrator.py
api/          Entrada de la función de Vercel
n8n/          Flujo de n8n para Telegram (importable) y tests de sus nodos
tests/        Tests de backend (Python) y de la vista Día a Día (Node)
docs/         Documentación del proyecto (docs/historico/: documentos del proceso)
agentes/, central/, instalar.ps1   Herramientas internas de coordinación del equipo (docs/HERRAMIENTAS_EQUIPO.md)
```

## Documentación

| Documento | Contenido |
| :--- | :--- |
| [`docs/BIBLIA_FINAL_V1.md`](docs/BIBLIA_FINAL_V1.md) | Documento maestro: problema, flujo, datos por caso y economía conductual. |
| [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) | Guion de la demo de 3 minutos. |
| [`docs/TELEGRAM_N8N.md`](docs/TELEGRAM_N8N.md) | La Radio del Sherpa: backend → n8n → Telegram. |
| [`docs/SPEC_UI_SALUD_Y_MOCHILA.md`](docs/SPEC_UI_SALUD_Y_MOCHILA.md) | Especificación de Salud y Tu mochila. |
| [`docs/CAPACIDADES_BACKEND.md`](docs/CAPACIDADES_BACKEND.md) | Catálogo del backend. |
| [`docs/GUIA_API_IA_SHERPAS.md`](docs/GUIA_API_IA_SHERPAS.md) | Acceso al MCP y a la IA de Sherpas. |
| [`docs/HERRAMIENTAS_EQUIPO.md`](docs/HERRAMIENTAS_EQUIPO.md) | Coordinación multi-máquina del equipo. |
| [`docs/historico/`](docs/historico/) | Documentos del proceso del hackathon (propuesta inicial, estado intermedio, guion alternativo). |

## Equipo

Gabriel (orquestación), Juan (frontend) y Adrián / Sabater (backend).
