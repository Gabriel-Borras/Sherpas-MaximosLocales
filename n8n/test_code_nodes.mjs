// Prueba la lógica de los Code nodes con payloads REALES del backend y los globals de n8n simulados.
// Uso: node --test n8n/test_code_nodes.mjs   (desde la raíz del repo)
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const load = n => readFileSync(join(here, 'code-nodes', n), 'utf8');

// Payloads reales: exactamente lo que server.py envía a n8n.
const real = JSON.parse(execFileSync('python', ['-c', `
import json
from backend.server import _milestone_webhook_payload
from backend.notifications import NotificationEngine
from backend.irl_engine import create_irl_run
out = {}
for cid in ("michael-carter", "timothy-melanie-weah"):
    e = create_irl_run(cid); n = NotificationEngine(cid)
    out[cid] = [_milestone_webhook_payload(x, "irl-1") for x in n.generate_milestone_notifications(e)]
n = NotificationEngine("michael-carter")
shock = n.generate_macro_shock_notification(market_drop_pct=-8, event_name=n.list_historical_shocks()[0]["name"])
out["shock"] = {**shock, "run_id": "irl-1"}
print(json.dumps(out, ensure_ascii=False))
`], { cwd: root, encoding: 'utf8' }));

function run(codeName, item, staticData) {
  const fn = new Function('$input', '$getWorkflowStaticData', `return (function(){ ${load(codeName)} })();`);
  return fn({ first: () => ({ json: item }), all: () => [{ json: item }] }, () => staticData);
}
const tgStart = (chat, text) => ({ message: { chat: { id: chat }, text } });

test('/start registra el chat con case_id (con guiones) y owner', () => {
  const sd = {};
  const out = run('register.js', tgStart(111, '/start timothy-melanie-weah_B'), sd);
  assert.equal(out[0].json.chat_id, 111);
  assert.match(out[0].json.reply, /activada/);
  assert.deepEqual(sd.subs['timothy-melanie-weah'], [{ chat_id: 111, owner: 'B' }]);
});

test('/start repetido actualiza el owner sin duplicar', () => {
  const sd = {};
  run('register.js', tgStart(111, '/start michael-carter_client'), sd);
  run('register.js', tgStart(111, '/start michael-carter_A'), sd);
  assert.equal(sd.subs['michael-carter'].length, 1);
  assert.equal(sd.subs['michael-carter'][0].owner, 'A');
});

test('enlaces inválidos y texto libre no registran nada', () => {
  const sd = {};
  assert.match(run('register.js', tgStart(1, '/start ../../etc_x'), sd)[0].json.reply, /no es válido/);
  assert.match(run('register.js', tgStart(1, 'hola'), sd)[0].json.reply, /Radio del Sherpa/);
  assert.deepEqual(sd.subs, {});
  assert.deepEqual(run('register.js', { message: {} }, sd), []);
});

test('/stop elimina al usuario de todos los casos', () => {
  const sd = {};
  run('register.js', tgStart(5, '/start michael-carter_client'), sd);
  run('register.js', tgStart(6, '/start michael-carter_client'), sd);
  run('register.js', tgStart(5, '/stop'), sd);
  assert.deepEqual(sd.subs['michael-carter'].map(s => s.chat_id), [6]);
});

test('hito individual llega al suscriptor del caso, con texto HTML seguro', () => {
  const sd = { subs: { 'michael-carter': [{ chat_id: 111, owner: 'client' }] } };
  const payload = real['michael-carter'][0];
  const out = run('route.js', { body: payload }, sd);
  assert.equal(out.length, 1);
  assert.equal(out[0].json.chat_id, 111);
  assert.match(out[0].json.text, /<b>.+<\/b>/);
  assert.ok(out[0].json.text.includes(payload.message_plain.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')));
  assert.ok(out[0].json.text.length <= 4096);
});

test('"Owner B" solo avisa a B (y a quien se suscribió como client), no a A', () => {
  const sd = { subs: { 'timothy-melanie-weah': [
    { chat_id: 1, owner: 'A' }, { chat_id: 2, owner: 'B' }, { chat_id: 3, owner: 'client' },
  ] } };
  const forB = real['timothy-melanie-weah'].find(n => /Owner B/.test(n.target_owner));
  assert.ok(forB, 'el caso Weah debe tener un aviso para Owner B');
  const out = run('route.js', { body: forB }, sd);
  assert.deepEqual(out.map(o => o.json.chat_id).sort(), [2, 3]);
});

test('shock macro se envía a todo el hogar con titular y mensaje anti-pánico', () => {
  const sd = { subs: { 'michael-carter': [{ chat_id: 1, owner: 'A' }, { chat_id: 2, owner: 'B' }] } };
  const out = run('route.js', { body: real.shock }, sd);
  assert.equal(out.length, 2);
  assert.match(out[0].json.text, /^📻 <b>/);
});

test('reintento del mismo aviso no duplica el mensaje (idempotencia)', () => {
  const sd = { subs: { 'michael-carter': [{ chat_id: 1, owner: 'client' }] } };
  const body = real['michael-carter'][0];
  assert.equal(run('route.js', { body }, sd).length, 1);
  assert.equal(run('route.js', { body }, sd).length, 0);
});

test('sin suscriptores o sin case_id no se envía nada y se escapa el HTML', () => {
  assert.deepEqual(run('route.js', { body: real['michael-carter'][0] }, {}), []);
  assert.deepEqual(run('route.js', { body: { title: 'x' } }, {}), []);
  const sd = { subs: { c: [{ chat_id: 9, owner: 'client' }] } };
  const out = run('route.js', { body: { case_id: 'c', notification_id: 'x', severity: 'critical', title: '<script>', message_plain: 'a & b', day: 3 } }, sd);
  assert.match(out[0].json.text, /&lt;script&gt;/);
  assert.match(out[0].json.text, /a &amp; b/);
  assert.match(out[0].json.text, /^🚨/);
});

test('el JSON del workflow es consistente y trae el código de los nodos', () => {
  execFileSync('node', [join(here, 'build_workflow.mjs')]);
  const w = JSON.parse(readFileSync(join(here, 'sherpas-telegram-radio.workflow.json'), 'utf8'));
  const names = new Set(w.nodes.map(n => n.name));
  for (const [from, v] of Object.entries(w.connections)) {
    assert.ok(names.has(from));
    for (const o of v.main.flat()) assert.ok(names.has(o.node));
  }
  const byName = n => w.nodes.find(x => x.name === n);
  assert.equal(byName('Registrar suscripción').parameters.jsCode, load('register.js'));
  assert.equal(byName('Formatear y enrutar').parameters.jsCode, load('route.js'));
  assert.equal(byName('Webhook Sherpas').parameters.authentication, 'headerAuth');
  assert.equal(byName('Enviar por Telegram').parameters.additionalFields.appendAttribution, false);
});
