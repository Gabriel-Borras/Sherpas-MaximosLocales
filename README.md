# Sherpa Basecamp

> **Convertimos el miedo financiero en calma, claridad y decisiones en frío — sin inventar ni un solo dato.**

**Sherpa Basecamp** transforma los informes financieros estáticos en una experiencia interactiva guiada sobre los datos reales de cada hogar (conectados al **MCP oficial de Sherpas** con respaldo determinista local y **0 cifras inventadas**).

---

## 1. El problema real: no fallan las matemáticas, paraliza el miedo

Un plan financiero tradicional en PDF responde a la lógica matemática, pero suele fracasar en la vida real porque ignora el factor humano. Lo que paraliza a una persona o a una pareja —o les lleva a tomar malas decisiones irreversibles— casi nunca es falta de tablas: es **el miedo**.

- **Miedo a equivocarse** con decisiones grandes (comprar vivienda, cambiar de trabajo, mover ahorros) y quedarse sin red de seguridad.
- **Miedo a mirar la realidad** cuando el informe abruma con decenas de páginas, jerga técnica y horizontes de 30 años.
- **Miedo al conflicto en pareja**, cuando un miembro busca crecimiento y el otro busca seguridad, y hablar de dinero se convierte en reproche.
- **Miedo en los momentos de pánico de mercado**, cuando caen las bolsas, llegan titulares alarmistas y el impulso emocional empuja a vender en el peor momento.

### Dónde aportamos valor
El valor diferencial de **Sherpa Basecamp** está en **calmar al cliente y ayudarle a tomar decisiones en frío**:
1. **Antes de hablar de números, escuchamos sus miedos** y ordenamos toda la experiencia a partir de lo que realmente le quita el sueño.
2. **Eliminamos el pánico al error** dejando probar consecuencias reales en un entorno seguro con *Rewind* (rebobinar), sin jerga ni sustos innecesarios.
3. **Acompañamos cuando llegan las curvas de verdad** con alertas proactivas en Telegram basadas en los shocks históricos reales de su propia cartera, recordándole con hechos que su estrategia ya aguantó tormentas similares.

---

## 2. Base psicológica: por qué funciona

Cada pantalla y mecánica de **Sherpa Basecamp** está diseñada deliberadamente sobre principios contrastados de **economía conductual y psicología de la decisión**:

| Principio psicológico | Qué bloquea al cliente | Cómo lo resuelve Sherpa Basecamp |
| :--- | :--- | :--- |
| **Efecto IKEA** (*Agencia y propiedad*) | Un plan impuesto en un PDF se percibe como ajeno y acaba olvidado en un cajón. | El cliente **construye su propia ruta** eligiendo en cada campamento de la montaña entre opciones neutras (sin spoilers). Al participar en cada decisión, siente el plan como suyo y se compromete a ejecutarlo. |
| **Descuento Hiperbólico / Sesgo del Presente** | El deseo de hoy pesa mucho más que un déficit lejano a 20 o 30 años. | Al elegir una ruta de inercia en el presente, la montaña muestra de inmediato la **rama roja** en el año y edad exactos en que el hogar se queda sin liquidez, eliminando la distancia temporal. |
| **Aversión a la Pérdida y Parálisis por Miedo** | El miedo a "hacerlo mal" paraliza o impide contratar protección básica. | La montaña permite **probar sin riesgo y rebobinar (*Rewind*)** en frío, transformando la parálisis en exploración tranquila y mostrando el coste real de no actuar (*coste de inercia*). |
| **Sobrecarga de Decisión (*Choice Overload*)** | Ver 15 tareas y 30 años de proyecciones a la vez bloquea la acción. | Al coronar la cima, la app cambia al **Modo Enfoque (Día a Día 0–30)**: oculta el ruido y muestra **un único paso inmediato ejecutable** en pocos minutos. |
| **Desactivación del conflicto en pareja** | Hablar de dinero cara a cara dispara defensas, culpa y asimetrías de riesgo. | La **Cordada Asimétrica multi-dispositivo** deja que cada miembro vote **a ciegas desde su propio móvil/pantalla**, resalta primero en qué coinciden al 100% y visualiza las divergencias en la montaña como un problema técnico compartido, no personal. |
| **Anclaje de calma ante volatilidad** | En una caída bursátil el pánico empuja a abandonar el plan en el suelo del mercado. | **La Radio del Sherpa** cruza el susto actual con los **11 shocks históricos reales** de la cartera del hogar y envía calma en frío por Telegram (vía n8n) demostrando cómo su estrategia se recuperó en semanas. |

---

## 3. Recorrido completo de la experiencia

1. **Evaluación inicial de miedos (Fase 1A):**
   - Rejilla limpia en lenguaje 100% cotidiano (ES/EN, sin jerga financiera) donde el cliente elige sus **3 mayores preocupaciones (`1º / 2º / 3º`)**.
   - Se guarda por perfil en `localStorage` para no repetirla en cada visita (con opción de *Rehacer evaluación* en el resumen).
   - El miedo `#1` reordena automáticamente el punto de partida de la montaña (`backend/timeline_engine.py`).

2. **Cordada Asimétrica multi-dispositivo (solo parejas):**
   - Crea una sala compartida (`/api/rooms`) con enlace para que Persona A y Persona B respondan desde dispositivos separados.
   - Si ambos eligen rutas distintas en un campamento, aparecen dos exploradores (`#climberMarkerA` / `#climberMarkerB`) que animan simultáneamente la bifurcación (`couple-split`) hasta reunir la cordada o rebobinar.

3. **Basecamp — La Montaña *Sumi-e*:**
   - Recorrido visual de **4 campamentos** sobre arte *sumi-e* con 4 biomas progresivos (`forest`, `rock`, `snow`, `summit`), modal de **Salud** (pentágono de 5 pilares) y desplegable **Tu mochila**.
   - Tarjetas de decisión translúcidas y neutras (sin rojo anticipado ni *spoilers*).
   - Si se elige la inercia o una ruta inviable, se dibuja la **rama roja** sincronizada 1:1 en el año y edad literales de caída del JSON oficial, se explican los hechos en modo **Lenguaje claro ↔ Matemáticas exactas** (`Plain ↔ Math`) y se puede **Rebobinar** para elegir la palanca viable (`top_moves`).

4. **Día a Día (0–30) tras la cima:**
   - Una vez superada la montaña, la interfaz pasa a la montaña simplificada de ejecución **Día a Día** (con el nodo subiendo del Día 0 al Día 30).
   - Muestra únicamente la acción inmediata ejecutable, el **coste documentado de inercia** si pasan los días sin completarla y navegación entre hitos (`Día 0 → Día 3 → Día 14 → Día 30`).

5. **La Radio del Sherpa (Telegram + n8n + `.ics`):**
   - Hipervínculo directo con *Deep Linking* a `@SherpasRadioBot` (`https://t.me/SherpasRadioBot?start=<case_id>_<owner>`) para vincular el chat del cliente en n8n con un toque.
   - Botones de demo (`Día 0/3/14/30` y `Caída de bolsa`) + webhook saliente no bloqueante (`N8N_WEBHOOK_URL`) + *scheduler* y flujo n8n listo en `n8n/sherpas-telegram-radio.workflow.json`.
   - Exportación real de calendario `.ics`.

6. **Advisor Brief (Resumen para el asesor):**
   - Compila automáticamente los miedos declarados, el contraste entre preocupación subjetiva e impacto cuantitativo real, los acuerdos/fricciones de pareja y las preguntas sin modelar, listo para copiar antes de la reunión.

---

## 4. Regla estricta de integridad de datos (0 inferencia)

- **Fuente oficial:** Los 4 casos del hackathon (`michael-carter`, `samantha-lewis`, `timothy-melanie-weah`, `daniel-emily-johnson`) se cargan desde el **MCP oficial de Sherpas** (`backend/mcp_client.py`), con fallback automático a `cases/` (`SHERPAS_CASES_DIR` / `CASES_DIR`) y datos semilla verificados.
- **0 cifras inventadas:** Ni el backend ni el frontend ni la capa narrativa opcional (`/api/ai/*`) inventan edades, importes, scores ni supuestos fuera de los JSON oficiales. Si el LLM intenta introducir un número no respaldado por el caso, el validador lo rechaza y cae de inmediato al texto determinista verificado.
- **100% funcional sin dependencias externas:** El servidor corre solo con la biblioteca estándar de Python 3 y funciona offline con fallback determinista instantáneo si faltan `MCP_TOKEN`, `TEAM_KEY` o `N8N_WEBHOOK_URL`.

---

## 5. Arquitectura y estructura del repositorio

```text
Sherpas-MaximosLocales/
├── backend/
│   ├── server.py               # Servidor HTTP unificado (stdlib ThreadingHTTPServer, CORS *, estáticos + API)
│   ├── mcp_client.py           # Cliente MCP Sherpas (list_cases / get_case) con fallback local/seed
│   ├── timeline_engine.py      # Motor determinista Basecamp (5 pilares, Top-1 miedo, bifurcación y rewind)
│   ├── api.py                  # Adaptador de sesiones /api/sessions/* y /api/expedition/*
│   ├── irl_engine.py           # Motor Día a Día (0/3/14/30), Modo Enfoque, coste de inercia y .ics
│   ├── dia_a_dia.py            # Estado y progresión visual Día 0–30 en la montaña
│   ├── notifications.py        # La Radio del Sherpa (hitos + 11 shocks históricos reales)
│   ├── telegram_relay.py       # Scheduler, outbox y puente con n8n/Telegram
│   ├── radio_demo.py           # Disparadores de demo (Día 0/3/14/30 y caída de bolsa -> Telegram)
│   ├── llm_proxy.py            # Cliente opcional del AI Proxy Sherpas (TEAM_KEY)
│   └── behavioral_narrator.py  # Capa narrativa conductual 0-inferencia (ES/EN, contraste y Advisor Brief)
├── frontend/
│   ├── index.html              # Entrada web (?case=&room=&member=)
│   ├── expedicion.js           # Fase 1A, montaña sumi-e, 4 biomas, Salud, Tu mochila, CoupleRoomSync y couple-split
│   ├── post-cima.js            # Vista post-cima, Día a Día, enlace Telegram y Advisor Brief
│   ├── dia-a-dia.js            # Montaña Día 0–30 sin biomas con nodo progresivo
│   ├── radio-demo.js           # Controles de demo para disparar alertas a Telegram
│   ├── cases-data.js           # Catálogo embebido + carga en vivo desde GET /api/cases/{id}
│   ├── styles.css              # Diseño sumi-e monocromático y paneles translúcidos
│   └── assets/                 # Arte sumi-e de montaña y 4 biomas
├── n8n/                        # Flujo n8n listo para importar (sherpas-telegram-radio.workflow.json) y tests
├── tests/                      # Suite completa unittest (backend, MCP, servidor, E2E, Telegram/n8n y Día a Día)
└── docs/                       # Biblia del proyecto, guía de demo, API IA, Telegram/n8n y estado final
```

---

## 6. Arranque rápido

### 1. Configurar variables de entorno (opcional)
El proyecto arranca directamente sin configuración. Para conectar el **MCP real de Sherpas**, el **AI Proxy** o las alertas de **Telegram/n8n**, copia `.env.example` a `.env` (ignorado por Git):

```env
MCP_URL=https://mcp-hackathon.sherpaswealth.com/mcp
MCP_TOKEN=tu_token_personal_de_72h
LLM_PROXY_URL=https://llm-hackathon.sherpaswealth.com/v1
TEAM_KEY=tu_team_key
N8N_WEBHOOK_URL=
TELEGRAM_BOT_USERNAME=SherpasRadioBot
```

### 2. Levantar el servidor unificado
```bash
python3 -m backend.server --host 127.0.0.1 --port 8000
```
Abre en tu navegador: **http://127.0.0.1:8000**

*(También puedes abrir cualquier caso directamente con `?case=michael-carter`, `?case=samantha-lewis`, `?case=timothy-melanie-weah` o `?case=daniel-emily-johnson`.)*

### 3. Verificar conexión con el MCP real (opcional)
```bash
python3 -c "from backend.mcp_client import SherpasMCPClient as C; c=C(allow_fallback=False); print([x.get('id') for x in c.list_cases()]); print(c.last_source)"
```
Debe devolver los 4 casos y `mcp`.

---

## 7. Endpoints principales (`backend/server.py`)

| Grupo | Rutas | Función |
| :--- | :--- | :--- |
| **Salud y Web** | `GET /health`, `GET /` | Estado del servidor y entrega de `frontend/`. |
| **Casos** | `GET /api/cases`, `GET /api/cases/{id}`, `GET /api/cases/{id}/overview` | Catálogo oficial, JSON literal completo y resumen `plain`/`math`. |
| **Expedición Basecamp** | `POST /api/expedition`, `/api/expedition/{id}/(quest\|cordada\|preview\|decide\|rewind\|restart\|overview\|advisor-brief)`, `/api/sessions/*` | Flujo completo determinista de miedos, pareja, campamentos y rebobinado. |
| **Salas de Pareja** | `POST /api/rooms`, `GET /api/rooms/{room_id}`, `POST /api/rooms/{room_id}/(evaluation\|decision)` | Sincronización multi-dispositivo A/B para evaluación y decisiones de montaña. |
| **Día a Día y Radio** | `/api/irl/*`, `/api/dia-a-dia/*`, `GET /api/radio`, `GET /api/radio/{id}`, `POST /api/radio/{id}/shock`, `GET /api/radio/{id}/ics`, `/api/radio/demo/*` | Progresión Día 0–30, coste de inercia, calendario `.ics`, enlace Telegram y disparo a n8n. |
| **Capa Narrativa** | `POST /api/ai/reframe`, `POST /api/ai/pact`, `POST /api/ai/brief` | Reformulación bilingüe `ES/EN` con 0 inferencia y fallback determinista instantáneo. |

---

## 8. Tests y validación

```bash
# Suite completa de Python
python3 -m unittest discover -s tests -v

# Validación de sintaxis de frontend y nodos n8n
for f in frontend/*.js; do node --check "$f"; done
node --test n8n/test_code_nodes.mjs
```

---

## 9. Documentación adicional

- [`docs/BIBLIA_FINAL_V1.md`](docs/BIBLIA_FINAL_V1.md) — Especificación completa de producto, casos y sesgos psicológicos.
- [`docs/ESTADO_PROYECTO_FINAL.md`](docs/ESTADO_PROYECTO_FINAL.md) — Estado integral del sistema y mapa de módulos/PRs.
- [`docs/CAPACIDADES_BACKEND.md`](docs/CAPACIDADES_BACKEND.md) — Detalle de capacidades del backend unificado.
- [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) — Guion cronometrado de demo de 3 minutos para jueces.
- [`docs/TELEGRAM_N8N.md`](docs/TELEGRAM_N8N.md) — Configuración de alertas automáticas por Telegram vía n8n.
- [`docs/GUIA_API_IA_SHERPAS.md`](docs/GUIA_API_IA_SHERPAS.md) — Guía de acceso al MCP y AI Proxy de Sherpas.
- [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) — Sistema multi-agente y coordinación entre máquinas usado durante el desarrollo.
