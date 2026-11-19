# Guion de Demo para Jueces (3 minutos) — Sherpa Basecamp × Run IRL

> **Objetivo de la demo:** Mostrar en **3 minutos** cómo *Sherpa Basecamp × Run IRL* convierte un informe financiero estático en una experiencia guiada sobre datos reales (`cases/`), sin cifras inventadas y con soporte determinista offline o con `TEAM_KEY` / `N8N_WEBHOOK_URL`.

---

## 1. Checklist de arranque limpio (`backend/server.py`)

Ejecuta estos pasos desde la raíz del repositorio antes de empezar la presentación:

1. **Verificar entorno y variables (opcional):**
   - El servidor funciona sin dependencias externas y con fallback determinista instantáneo aunque no exista `TEAM_KEY` ni `N8N_WEBHOOK_URL`.
   - Si deseas activar el proxy LLM/MCP o las alertas por n8n/Telegram, copia `.env.example` a `.env` y rellena `TEAM_KEY` / `MCP_TOKEN` / `N8N_WEBHOOK_URL`.
2. **Arrancar el servidor unificado:**
   ```bash
   python3 -m backend.server --host 127.0.0.1 --port 8000
   ```
3. **Comprobar salud del backend:**
   - Verifica `GET http://127.0.0.1:8000/health` (debe responder HTTP `200`).
   - Opcional (verificación rápida antes de salir a escena):
     ```bash
     python3 -m unittest tests/test_server.py -v
     ```
4. **Abrir la aplicación en el navegador (vista limpia):**
   - Abre `http://127.0.0.1:8000/` en una ventana limpia (o incógnito) para que no quede estado previo en `localStorage`.
   - Confirma que cargan los casos oficiales (`michael-carter`, `samantha-lewis`, `timothy-melanie-weah`, `daniel-emily-johnson`).

---

## 2. Guion cronometrado de 3 minutos (4 momentos clave)

### `0:00 – 0:45` · Momento 1: Evaluación Top-3 (Fase 1A ultra-simple)
- **Caso sugerido:** `michael-carter` (Michael Carter, 37 años, Score `26` crítico) o `samantha-lewis` (Samantha Lewis, 47 años, Score `82` fuerte).
- **Qué hacer en pantalla:**
  1. En la pantalla inicial, selecciona las **3 preocupaciones principales (`1º`, `2º`, `3º`)** en lenguaje cotidiano.
  2. Pulsa continuar para registrar el punto de partida y pasar a la montaña.
- **Qué decir a los jueces:**
  - *"El informe actual de Sherpas deja vacío el campo `Subjective concerns`. En menos de 30 segundos capturamos qué le quita el sueño a la familia y lo contrastamos directamente con los números reales de su plan."*

---

### `0:45 – 1:30` · Momento 2: Pareja ciega A/B (Cordada Asimétrica multi-dispositivo)
- **Caso sugerido:** `timothy-melanie-weah` (Timothy & Melanie Weah, Score `60`, pareja `DUAL`) o `daniel-emily-johnson` (Daniel & Emily Johnson, Score `52`).
- **Qué hacer en pantalla:**
  1. Crea una sala de pareja (`/api/rooms`) o usa la vista A/B a ciegas.
  2. Registra el **voto privado** de la Persona A (sin que B lo vea) y después el **voto privado** de la Persona B.
  3. Muestra la comparativa de pareja y la bifurcación simultánea (`couple-split`) si eligen caminos distintos.
- **Qué decir a los jueces:**
  - *"Las parejas suelen tener distinto perfil de riesgo. Con la Cordada Asimétrica votan a ciegas por separado desde su propio dispositivo: la app destaca primero en qué coinciden al 100% y visualiza los roces en tiempo real en la montaña."*

---

### `1:30 – 2:15` · Momento 3: Basecamp con rama roja real por edad
- **Caso sugerido:** `samantha-lewis` (para el contraste con Score `82`) o `michael-carter` (Score `26`).
- **Qué hacer en pantalla:**
  1. En **Basecamp · Ruta de ascenso** (4 campamentos sobre la montaña *sumi-e*), enseña el toggle `Plain ↔ Math`.
  2. Elige una opción de inercia/errónea para provocar la **rama roja** en la montaña.
  3. Abre el detalle del bloqueo (*Por qué ocurre: tensiones y hechos*) y pulsa **Rebobinar al campamento** (*Rewind*) para elegir la palanca viable (`top_moves`) y coronar la cima.
- **Qué decir a los jueces:**
  - *"Un score de `82` en PDF oculta que Samantha se queda sin liquidez en **2053 (edad 74, `-$227,414`)**, y Michael en **2075 (edad 86, `-$38,276`)**. Aquí la montaña frena en el año y edad exactos del JSON, explica por qué ocurre y deja rebobinar para probar el desvío que sí llega a la cima."*

---

### `2:15 – 3:00` · Momento 4: Día 0 + Radio `.ics` + Telegram (n8n) + Resumen del Asesor (`Advisor Brief`)
- **Qué hacer en pantalla:**
  1. Al llegar a **Cima alcanzada**, pasa a la vista de enfoque **Día 0** (*Run IRL*), mostrando el próximo paso inmediato accionable.
  2. Abre **La Radio del Sherpa**: muestra la alerta basada en shocks históricos reales del caso (`analysis.events`) y pulsa **Descargar calendario `.ics`** (`sherpas-run-irl.ics`).
  3. **Pulsar "Conectar a Telegram"** (`https://t.me/SherpasRadioBot?start=<caseId>_<voter>`) para activar las alertas de La Radio del Sherpa en el móvil del cliente vía Deep Linking y enseñar el mensaje entrante en Telegram generado por n8n.
  4. Abre la pestaña de **Resumen del Asesor (`Advisor Brief`)** (`POST /api/ai/brief`) y muestra el botón de copiar resumen en texto plano.
- **Qué decir a los jueces:**
  - *"Tras la cima no volvemos a abrumar con 30 años de gráficos: el cliente solo ve su **Día 0** ejecutable. **La Radio del Sherpa** exporta sus hitos reales a `.ics`, conecta su móvil con `@SherpasRadioBot` en Telegram mediante n8n y aporta calma ante caídas de mercado con los shocks históricos reales de su cartera. Y el asesor recibe un **Advisor Brief** listo para la reunión."*

---

## 3. Endpoints reales de referencia (`backend/server.py`)

- `GET /health`: estado del servidor.
- `GET /api/cases`, `GET /api/cases/<case_id>` y `GET /api/cases/<case_id>/overview`: catálogo, JSON literal y resumen.
- `POST /api/sessions` / `/api/expedition`: creación y avance de sesión de expedición en Basecamp.
- `POST /api/rooms` y `/api/rooms/<room_id>/(evaluation|decision)`: salas de pareja multi-dispositivo.
- `POST /api/irl` y `GET/POST /api/irl/<run_id>/...`: motor de *Run IRL* (Día 0, Día 3, Día 14, Día 30) + webhook n8n.
- `GET /api/radio/...`: feed de *La Radio del Sherpa*, exportación `.ics` y shock macro + webhook n8n.
- `POST /api/ai/reframe`, `POST /api/ai/pact`, `POST /api/ai/brief`: capa narrativa conductual (con fallback determinista sin `TEAM_KEY`).
