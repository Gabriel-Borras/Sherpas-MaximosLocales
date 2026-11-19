# Guía de acceso y conexión a la API de IA de Sherpas (Hackathon UPV 2026)

Resumen extraído de la documentación oficial de [`SherpasEngineering/hackathon-upv-2026`](https://github.com/SherpasEngineering/hackathon-upv-2026) sobre cómo obtener los **$50 USD en créditos** por equipo y cómo conectar los modelos de IA a nuestra web mediante API.

---

## 1. Cómo conseguir los $50 en créditos (`TEAM_KEY`)

1. Entra en la página de acceso: **https://mcp-hackathon.sherpaswealth.com/personal-token**
2. Inicia sesión con **el correo electrónico con el que te registraste** en el hackathon.
3. Recibirás un **código de 6 dígitos** por correo (revisa la carpeta de spam; caduca a los 10 minutos).
4. Una vez dentro verás:
   - **Clave de IA del equipo (`TEAM_KEY`)**: es la clave compartida de todo el equipo con los **$50 USD de crédito** (válidos hasta el **21 de noviembre**). No cambia entre inicios de sesión.
   - **Token del MCP de casos (`MCP_TOKEN`)**: tu token personal para leer los casos desde código (dura 72 horas y se renueva cada vez que inicias sesión).
   - **Para tu backend**: un bloque `.env` listo para copiar con `MCP_URL`, `MCP_TOKEN`, `LLM_PROXY_URL` y `TEAM_KEY`.

> **Si hay problemas de acceso:** si aparece *"Tu equipo todavía no tiene clave"* o *"Este correo no está en la lista de participantes"*, contacta con un mentor en el [Discord del hackathon](https://discord.gg/wVUZXmxdS).

---

## 2. Modelos de IA disponibles en el proxy

El proxy está en `https://llm-hackathon.sherpaswealth.com` (si se abre en el navegador devuelve `{"detail":"Not Found"}`, es normal porque es solo para llamadas desde código) y es compatible con el SDK de OpenAI.

| Modelo | Modo | Precio (entrada / salida por 1M tokens, salvo indicado) |
|---|---|---|
| `gpt-5-mini` | Texto | $0.25 / $2.00 |
| `deepseek-flash` | Texto | $0.30 / $1.20 |
| `gemini-3.5-flash-lite` | Texto | $0.30 / $2.50 |
| `gpt-realtime-2.1-mini` | Voz (WebSocket) | $10 / $20 audio; $0.60 / $2.40 texto |
| `gpt-realtime-2.1` | Voz (WebSocket) | $32 / $64 audio; $4 / $24 texto |
| `gemini-3.8-live` | Voz (WebSocket) | $3 / $12 audio; $0.75 / $4.50 texto |
| `gpt-live-1` | Voz (WebSocket `/v1/live/sessions`) | $0.05 / minuto de sesión |
| `eleven-flash-v2.5` | Texto a voz (ElevenLabs) | $0.04 / 1.000 caracteres |
| `eleven-multilingual-v2` | Texto a voz (ElevenLabs) | $0.08 / 1.000 caracteres |
| `eleven-v3` | Texto a voz (ElevenLabs) | $0.08 / 1.000 caracteres |
| `scribe-v2` | Voz a texto (ElevenLabs) | $0.22 / hora de audio |

> **Nota sobre ElevenLabs:** hay un límite compartido de **$1.40 USD** dentro de los $50 del equipo para ElevenLabs (voz y transcripción juntos).

---

## 3. Cómo conectarlo a nuestra web mediante API

**Regla de seguridad:** la `TEAM_KEY` **nunca** debe exponerse en el frontend (navegador). Debe guardarse en un archivo `.env` en el **backend** (sin subirlo a GitHub). El frontend de nuestra web llamará a nuestro backend, y nuestro backend llamará al proxy de Sherpas.

### Variables en `.env`
```env
LLM_PROXY_URL=https://llm-hackathon.sherpaswealth.com
TEAM_KEY=tu-clave-de-equipo
```

### Opción A: Backend en Node.js / JavaScript (SDK de OpenAI)
Instalación: `npm install openai` (en Node 22+: `node --env-file=.env app.mjs`)

```js
import OpenAI from "openai";

const llm = new OpenAI({
  baseURL: "https://llm-hackathon.sherpaswealth.com/v1",
  apiKey: process.env.TEAM_KEY,
});

const reply = await llm.chat.completions.create({
  model: "gpt-5-mini",
  messages: [
    { role: "user", content: "Explain a 401(k) in two sentences." }
  ],
});

console.log(reply.choices[0].message.content);
```

### Opción B: Backend en Python (SDK de OpenAI)
Instalación: `pip install openai python-dotenv`

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

llm = OpenAI(
    base_url="https://llm-hackathon.sherpaswealth.com/v1",
    api_key=os.environ["TEAM_KEY"],
)

reply = llm.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "user", "content": "Explain a 401(k) in two sentences."}
    ],
)

print(reply.choices[0].message.content)
```

---

## 4. Límites, voz en tiempo real y control de gasto

- **Rate limits:** máximo **60 peticiones por minuto** y **4 peticiones o sesiones concurrentes** por equipo (`429 Too many requests` si se supera).
- **Uso de `gpt-5-mini`:** omitir `max_tokens` o usar al menos `1000`, ya que un límite muy bajo puede consumirse entero en el razonamiento y devolver una respuesta vacía.
- **Voz en tiempo real:** conexión WebSocket desde el backend a `wss://llm-hackathon.sherpaswealth.com/v1/realtime?model=gpt-realtime-2.1-mini` con el header `Authorization: Bearer <TEAM_KEY>` (audio PCM16 a 24 kHz en base64; hay un ejemplo funcional en `examples/voice/` del repo de Sherpas). Cerrar siempre la sesión WebSocket al terminar.
- **Consultar el gasto restante (`info.spend` e `info.max_budget` en USD):**
  ```powershell
  $env:TEAM_KEY = "tu-clave-de-equipo"
  curl.exe https://llm-hackathon.sherpaswealth.com/key/info -H "Authorization: Bearer $env:TEAM_KEY"
  ```
