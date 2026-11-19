// n8n Code node (Run Once for All Items) — "Formatear y enrutar".
// Input : Webhook item ({ body: <payload del backend> }).
// Output: one item per Telegram recipient { chat_id, text, notification_id }.
const raw = $input.first().json || {};
const p = raw.body && typeof raw.body === 'object' ? raw.body : raw;
if (!p || !p.case_id) return [];

const store = $getWorkflowStaticData('global');
store.subs = store.subs || {};
store.sent = store.sent || [];

const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const EMOJI = { critical: '🚨', warning: '⚠️', info: '🧭' };

// 1) Texto (HTML de Telegram; máx. 4096 caracteres).
let text;
if (p.type === 'macro_shock_radio' || p.kind === 'macro_shock') {
  const body = p.anti_panic_message_plain || p.anti_panic_message_math || '';
  text = `📻 <b>${esc(p.headline || 'La Radio del Sherpa')}</b>\n${esc(body)}`;
} else {
  const icon = EMOJI[p.severity] || '🧭';
  const day = Number.isFinite(Number(p.day)) ? `\n<i>Día ${esc(p.day)} · Sherpas</i>` : '';
  text = `${icon} <b>${esc(p.title || 'La Radio del Sherpa')}</b>\n${esc(p.message_plain || '')}${day}`;
}
if (text.length > 4000) text = text.slice(0, 3997) + '…';

// 2) Destinatarios: suscriptores del caso; si el aviso es de "Owner A/B", solo ese
//    titular (y quien se suscribió como client/all). Sin letra => todo el hogar.
const subs = store.subs[p.case_id] || [];
const m = String(p.target_owner || '').match(/Owner\s+([AB])\b/i);
const who = m ? m[1].toUpperCase() : null;
const recipients = subs.filter(s => !who || ['client', 'all'].includes(String(s.owner).toLowerCase()) || String(s.owner).toUpperCase() === who);

// 3) Idempotencia: no reenviar el mismo aviso al mismo chat (reintentos del outbox).
const out = [];
for (const s of recipients) {
  const key = `${p.notification_id || text.slice(0, 40)}|${s.chat_id}`;
  if (store.sent.includes(key)) continue;
  store.sent.push(key);
  out.push({ json: { chat_id: s.chat_id, text, notification_id: p.notification_id || null } });
}
if (store.sent.length > 1000) store.sent = store.sent.slice(-500);
return out;
