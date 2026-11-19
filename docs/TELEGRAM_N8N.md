# La Radio del Sherpa por Telegram (backend → n8n → Telegram)

Los avisos del Run IRL (Día 0 / 3 / 14 / 30, insistencia por pasos vencidos y shocks de mercado) salen **solos** del backend a n8n, y n8n los entrega por Telegram. Todo es opcional: sin `N8N_WEBHOOK_URL` el backend funciona igual.

```
Usuario ──pulsa──► t.me/<Bot>?start=<case_id>_<owner> ──► [n8n · Flujo A] guarda chat_id
Backend (scheduler / advance / check / shock) ──POST──► [n8n · Flujo B] ──► Telegram (HTML)
        └─ si n8n no responde → outbox (JSONL) → se reintenta en el siguiente tick
```

## 1. Variables de entorno del backend (`.env`)

| Variable | Para qué |
| :--- | :--- |
| `N8N_WEBHOOK_URL` | URL de producción del webhook de n8n (`…/webhook/sherpas-radio`). Vacío = desactivado. |
| `N8N_WEBHOOK_SECRET` | Secreto compartido; se envía en la cabecera `X-Sherpas-Secret`. |
| `TELEGRAM_BOT_USERNAME` | Usuario del bot sin `@` (por defecto `SherpasRadioBot`). |
| `SHERPAS_SCHEDULER_INTERVAL` | Segundos entre pasadas del scheduler. `0`/vacío = desactivado. Recomendado: `3600`. |
| `SHERPAS_DAY_SECONDS` | Segundos por día del plan (por defecto `86400` = tiempo real). Para demo: `60`. |
| `SHERPAS_MAX_DAY` | Tope de días que avanza el scheduler (por defecto `90`, evita avisos infinitos). |
| `SHERPAS_OUTBOX_DIR` | Carpeta del outbox (`n8n-outbox.jsonl`). Vacío = sin persistencia de fallos. |
| `SHERPAS_ENABLE_TELEGRAM_TEST` | `1` habilita `POST /api/telegram/test`. Déjalo vacío en producción. |

El scheduler solo arranca si hay `N8N_WEBHOOK_URL` y `SHERPAS_SCHEDULER_INTERVAL > 0`. Cada pasada avanza cada Run IRL según el reloj real desde que se creó, genera sus avisos y emite **cada uno una sola vez**; además reintenta el outbox.

> Los Run IRL viven en memoria: si el servidor se reinicia, los runs (y su calendario de avisos) empiezan de nuevo. Los chat_id **no** se pierden: los guarda n8n.

## 2. Montar el flujo en n8n (una vez)

1. Crea el bot con **@BotFather** (`/newbot`) y copia el token. Pon su usuario en `TELEGRAM_BOT_USERNAME`.
2. En n8n: **Credentials → Telegram API** con ese token.
3. En n8n: **Credentials → Header Auth** con nombre de cabecera `X-Sherpas-Secret` y como valor el `N8N_WEBHOOK_SECRET`.
4. **Import from file** → `n8n/sherpas-telegram-radio.workflow.json`. Asigna las credenciales a los nodos *Telegram Trigger*, *Responder al usuario*, *Enviar por Telegram* y *Webhook Sherpas*.
5. **Activa** el flujo (si no, no persiste el registro de chats ni existe la URL de producción).
6. Copia la *Production URL* del nodo *Webhook Sherpas* a `N8N_WEBHOOK_URL`.

Telegram exige HTTPS público para el *Telegram Trigger*: si n8n corre en local, usa un túnel (p. ej. `WEBHOOK_URL` de n8n apuntando a ngrok/cloudflared).

## 3. Probar de punta a punta

1. Abre `https://t.me/<Bot>?start=michael-carter_client` y pulsa *Start* → el bot responde «Radio del Sherpa activada».
2. Arranca el backend con `SHERPAS_ENABLE_TELEGRAM_TEST=1` y lanza:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/telegram/test -H "Content-Type: application/json" \
        -d '{"case_id":"michael-carter","owner":"client"}'
   ```
3. Estado del puente: `GET /api/telegram/config` (n8n configurado, scheduler, avisos en cola; nunca devuelve secretos ni la URL).
4. Demo acelerada: `SHERPAS_DAY_SECONDS=60 SHERPAS_SCHEDULER_INTERVAL=10`; crea un run (`POST /api/irl {"case_id":"…"}`) y los hitos de Día 0/3/14/30 llegan en minutos.

## 4. Reglas de enrutado y mensaje

- **Destinatarios:** suscriptores del `case_id`. Si el aviso va a «Owner A/B (…)», solo a ese titular y a quien se suscribió como `client`/`all`. Sin letra → todo el hogar. Shocks de mercado → todo el hogar.
- **Formato:** HTML de Telegram, escapado, máx. 4096 caracteres: `🧭/⚠️/🚨 <b>título</b>` + `message_plain` + `Día N`. Shock: `📻 <b>headline</b>` + mensaje anti-pánico.
- **Idempotencia:** n8n recuerda `notification_id|chat_id` y no reenvía duplicados (p. ej. al reintentar el outbox).
- **Comandos del bot:** `/start <case>_<owner>` (alta), `/stop` (baja de todos los casos).
- Contrato del webhook sin cambios respecto a `docs/ESTADO_PROYECTO_FINAL.md` §2.5; solo se añade la cabecera `X-Sherpas-Secret` cuando hay secreto.

## 5. Tests

```bash
python -m unittest tests.test_telegram_relay -v      # secreto, outbox, scheduler, endpoints
node --test n8n/test_code_nodes.mjs                  # lógica de los nodos n8n con payloads reales
node n8n/build_workflow.mjs                          # regenera el JSON tras editar n8n/code-nodes/*.js
```
