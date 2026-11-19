// n8n Code node (Run Once for All Items) — "Registrar suscripción".
// Input : Telegram Trigger item ({ message: { chat, text } }).
// Output: one item { chat_id, reply } for the Telegram "sendMessage" node.
// The deep link built by the backend is https://t.me/<Bot>?start=<case_id>_<owner>.
const item = $input.first().json || {};
const msg = item.message || {};
const chatId = msg.chat && msg.chat.id;
if (!chatId) return [];

const store = $getWorkflowStaticData('global');
store.subs = store.subs || {};
const text = String(msg.text || '').trim();

if (/^\/stop(@\w+)?$/i.test(text)) {
  for (const key of Object.keys(store.subs)) {
    store.subs[key] = store.subs[key].filter(s => s.chat_id !== chatId);
  }
  return [{ json: { chat_id: chatId, reply: '🔕 Has dejado de recibir La Radio del Sherpa. Vuelve a abrir el enlace de la app cuando quieras reactivarla.' } }];
}

const start = text.match(/^\/start(?:@\w+)?(?:\s+(\S+))?$/i);
if (!start) {
  return [{ json: { chat_id: chatId, reply: 'Hola 👋 Soy La Radio del Sherpa. Para activar tus avisos, abre el enlace «Sintonizar Radio en Telegram» desde la app.' } }];
}

const payload = start[1] || '';
const cut = payload.lastIndexOf('_');
const caseId = cut > 0 ? payload.slice(0, cut) : (payload || 'demo');
const owner = cut > 0 ? payload.slice(cut + 1) : 'client';
if (!/^[A-Za-z0-9-]{1,64}$/.test(caseId) || !/^[A-Za-z0-9]{1,16}$/.test(owner)) {
  return [{ json: { chat_id: chatId, reply: 'Ese enlace no es válido. Ábrelo de nuevo desde la app.' } }];
}

const list = store.subs[caseId] = store.subs[caseId] || [];
const existing = list.find(s => s.chat_id === chatId);
if (existing) existing.owner = owner; else list.push({ chat_id: chatId, owner });

return [{ json: { chat_id: chatId, reply: '✅ <b>Radio del Sherpa activada</b>\nTe avisaré aquí de tus próximos pasos (Día 0, 3, 14 y 30) y de las caídas de mercado. Escribe /stop para pararla.' } }];
