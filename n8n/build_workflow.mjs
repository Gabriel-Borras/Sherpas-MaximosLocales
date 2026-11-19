// Genera n8n/sherpas-telegram-radio.workflow.json inlineando n8n/code-nodes/*.js
// Uso: node n8n/build_workflow.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const code = n => readFileSync(join(here, 'code-nodes', n), 'utf8');
const TG = { telegramApi: { id: 'REPLACE_ME', name: 'Sherpas Radio Bot' } };

const note = [
  '## La Radio del Sherpa',
  '**Flujo A (arriba):** el usuario pulsa el enlace `t.me/<Bot>?start=<case>_<owner>` y se guarda su chat_id.',
  '**Flujo B (abajo):** el backend (`N8N_WEBHOOK_URL`) envia cada aviso, se formatea y se manda por Telegram.',
  '',
  'Antes de activar: asigna la credencial *Telegram API* (token de @BotFather) y la credencial *Header Auth* del webhook (cabecera `X-Sherpas-Secret` = `N8N_WEBHOOK_SECRET` del backend).',
  'El flujo debe estar **activo** para que el registro de chats persista.',
].join('\n');

const send = (id, name, chat, text, position, extra = {}) => ({
  parameters: { resource: 'message', operation: 'sendMessage', chatId: chat, text, additionalFields: { parse_mode: 'HTML', appendAttribution: false } },
  id, name, type: 'n8n-nodes-base.telegram', typeVersion: 1.2, position, credentials: TG, ...extra,
});

const workflow = {
  name: 'Sherpas · La Radio del Sherpa (Telegram)',
  nodes: [
    { parameters: { content: note, height: 220, width: 560 }, id: 'note', name: 'Leeme', type: 'n8n-nodes-base.stickyNote', typeVersion: 1, position: [-120, -60] },

    { parameters: { updates: ['message'], additionalFields: {} }, id: 'tg-trigger', name: 'Telegram Trigger', type: 'n8n-nodes-base.telegramTrigger', typeVersion: 1.1, position: [200, 200], webhookId: 'sherpas-radio-telegram', credentials: TG },
    { parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: code('register.js') }, id: 'register', name: 'Registrar suscripción', type: 'n8n-nodes-base.code', typeVersion: 2, position: [440, 200] },
    send('tg-welcome', 'Responder al usuario', '={{ $json.chat_id }}', '={{ $json.reply }}', [680, 200]),

    { parameters: { httpMethod: 'POST', path: 'sherpas-radio', authentication: 'headerAuth', responseMode: 'onReceived', responseCode: 200, options: {} }, id: 'webhook', name: 'Webhook Sherpas', type: 'n8n-nodes-base.webhook', typeVersion: 2, position: [200, 440], webhookId: 'sherpas-radio', credentials: { httpHeaderAuth: { id: 'REPLACE_ME', name: 'Sherpas Webhook Secret' } } },
    { parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: code('route.js') }, id: 'route', name: 'Formatear y enrutar', type: 'n8n-nodes-base.code', typeVersion: 2, position: [440, 440] },
    send('tg-send', 'Enviar por Telegram', '={{ $json.chat_id }}', '={{ $json.text }}', [680, 440], { retryOnFail: true, maxTries: 3, waitBetweenTries: 2000 }),
  ],
  connections: {
    'Telegram Trigger': { main: [[{ node: 'Registrar suscripción', type: 'main', index: 0 }]] },
    'Registrar suscripción': { main: [[{ node: 'Responder al usuario', type: 'main', index: 0 }]] },
    'Webhook Sherpas': { main: [[{ node: 'Formatear y enrutar', type: 'main', index: 0 }]] },
    'Formatear y enrutar': { main: [[{ node: 'Enviar por Telegram', type: 'main', index: 0 }]] },
  },
  settings: { executionOrder: 'v1' },
  pinData: {},
};

writeFileSync(join(here, 'sherpas-telegram-radio.workflow.json'), JSON.stringify(workflow, null, 2) + '\n');
console.log('workflow escrito:', workflow.nodes.length, 'nodos');
