// node --test frontend/test_dia_a_dia.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const DD = require('./dia-a-dia.js');

const plan = {
  case_id: 'x', is_couple: true, horizon_days: 30,
  members: [{ id: 'A', name: 'Timothy' }, { id: 'B', name: 'Melanie' }],
  steps: [
    { step_id: 's0', day: 0, title: 'Paso <0>', action_plain: 'Hacer & cosa', why: 'Cuesta $1', required_members: ['B'] },
    { step_id: 's3', day: 3, title: 'Paso 3', action_plain: 'Otra', why: '', required_members: ['A', 'B'] },
  ],
};

test('el sendero va del Día 0 (base) al Día 30 (cima) como en el Basecamp', () => {
  assert.deepEqual(DD.dayPoint(0).map(Math.round), [255, 552]);
  assert.deepEqual(DD.dayPoint(30).map(Math.round), [858, 145]);
  for (let d = 1; d <= 30; d++) assert.ok(DD.dayPoint(d)[1] <= DD.dayPoint(d - 1)[1] + 15, 'sube');
});

test('la cámara sigue al nodo y no se sale de la montaña', () => {
  for (const d of [0, 15, 30]) {
    const [x, y, w, h] = DD.cameraFor(d);
    assert.ok(x >= 0 && y >= 0 && x + w <= 1200 && y + h <= 750);
  }
});

test('montaña sin biomas: solo la ilustración base y un nodo por día', () => {
  const svg = DD.svg(plan, 4, {}, 'ES');
  assert.match(svg, /assets\/mountain-sumi\.jpg/);
  assert.doesNotMatch(svg, /mountain-biome-/);
  assert.equal((svg.match(/class="dd-node /g) || []).length, 31);
  assert.match(svg, /dd-task is-late/); // Día 0 sin hacer y ya pasado
});

test('tarjeta: solo pinta los textos del plan (escapados), con el porqué', () => {
  const html = DD.card({ lang: 'ES', day: 0, plan, completed: {}, status: { mode: 'task', today: [plan.steps[0]], pending: [], next_day: 3, reminder_due: false } });
  assert.match(html, /Paso &lt;0&gt;/);
  assert.match(html, /Hacer &amp; cosa/);
  assert.match(html, /Por qué:<\/span> Cuesta \$1/);
  assert.match(html, /data-dd-member="B"/);
  assert.doesNotMatch(html, /data-dd-member="A"/);
});

test('día vacío: esperar si todo está hecho; recordatorio si falta algo', () => {
  const wait = DD.card({ lang: 'ES', day: 5, plan, completed: {}, status: { mode: 'wait', today: [], pending: [], next_day: 14, reminder_due: false } });
  assert.match(wait, /Hoy toca esperar/);
  assert.match(wait, /Día 14/);
  const pend = { ...plan.steps[1], missing_names: ['Melanie'], days_late: 2 };
  const rem = DD.card({ lang: 'ES', day: 5, plan, completed: { s3: ['A'] }, status: { mode: 'pending', today: [], pending: [pend], next_day: 14, reminder_due: true } });
  assert.match(rem, /Falta: Melanie · hace 2 días/);
  assert.match(rem, /cada 2 días/);
});

test('sin n8n configurado no se muestra estado de Telegram', () => {
  const st = { mode: 'wait', today: [], pending: [], next_day: null, reminder_due: false };
  assert.doesNotMatch(DD.card({ lang: 'ES', day: 30, plan, status: st, notification: { sent: false, configured: false, title: 'x' } }), /Telegram/);
  assert.match(DD.card({ lang: 'ES', day: 30, plan, status: st, notification: { sent: true, configured: true, title: 'x' } }), /Enviado a Telegram/);
});

test('zoom: la cámara admite anchos entre 300 y la montaña entera, sin salirse', () => {
  assert.equal(DD.MIN_W, 300);
  assert.equal(DD.MAX_W, 1200);
  for (const w of [100, 300, 660, 1200, 5000]) {
    const [x, y, bw, bh] = DD.cameraFor(15, w);
    assert.ok(bw >= 300 && bw <= 1200, `ancho ${w} -> ${bw}`);
    assert.ok(x >= 0 && y >= 0 && x + bw <= 1200 + 1e-6 && y + bh <= 750 + 1e-6);
    assert.ok(Math.abs(bw / bh - 660 / 412) < 1e-6, 'mantiene la proporción');
  }
});

test('el svg arranca con el zoom guardado', () => {
  const m = DD.svg(plan, 10, {}, 'ES', 400).match(/viewBox="([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)"/);
  assert.equal(Number(m[3]), 400);
  assert.ok(Math.abs(Number(m[3]) / Number(m[4]) - 660 / 412) < 0.01, 'mantiene la proporción');
});
