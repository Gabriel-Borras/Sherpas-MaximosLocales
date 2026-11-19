// Modo Día a Día: montaña sumi-e (la del Basecamp, sin biomas) con un nodo por día (0 → 30)
// y una tarjeta con lo que toca hoy. Los textos de los pasos vienen tal cual del backend
// (/api/dia-a-dia/*, motor IRL del caso): aquí no se inventa ningún dato.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.SherpaDiaADia = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  // Mismo sendero que la montaña del Basecamp (expedicion.js · TRAIL_PATH).
  const TRAIL_PATH = 'M 255 552 Q 285 516 312 491 Q 368 498 432 479 Q 504 442 564 382 Q 624 378 684 319 Q 744 295 804 209 Q 836 168 858 145';
  const FULL = [0, 0, 1200, 750];
  const CAM_W = 660, CAM_H = 412;
  const HORIZON = 30;

  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  // --- Geometría del sendero: muestreo por longitud de arco de las curvas Q ---
  function parseTrail(d) {
    const nums = d.match(/-?\d+(\.\d+)?/g).map(Number);
    const start = [nums[0], nums[1]];
    const segs = [];
    let p0 = start;
    for (let i = 2; i + 3 < nums.length + 1; i += 4) {
      const c = [nums[i], nums[i + 1]], p1 = [nums[i + 2], nums[i + 3]];
      segs.push([p0, c, p1]);
      p0 = p1;
    }
    return segs;
  }
  const qAt = ([a, c, b], t) => [
    (1 - t) * (1 - t) * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0],
    (1 - t) * (1 - t) * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]
  ];
  const TRAIL = (function () {
    const fine = [];
    parseTrail(TRAIL_PATH).forEach((seg, si) => {
      for (let k = si === 0 ? 0 : 1; k <= 60; k++) fine.push(qAt(seg, k / 60));
    });
    const acc = [0];
    for (let i = 1; i < fine.length; i++) acc.push(acc[i - 1] + Math.hypot(fine[i][0] - fine[i - 1][0], fine[i][1] - fine[i - 1][1]));
    return { fine, acc, length: acc[acc.length - 1] };
  })();

  function pointAt(fraction) {
    const target = Math.max(0, Math.min(1, fraction)) * TRAIL.length;
    let i = TRAIL.acc.findIndex(v => v >= target);
    if (i <= 0) return TRAIL.fine[Math.max(0, i)].slice();
    const span = TRAIL.acc[i] - TRAIL.acc[i - 1] || 1;
    const t = (target - TRAIL.acc[i - 1]) / span;
    const a = TRAIL.fine[i - 1], b = TRAIL.fine[i];
    return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
  }
  const dayPoint = day => pointAt(day / HORIZON);

  const MIN_W = 300, MAX_W = FULL[2];            // de ~4x de aumento a la montaña entera
  const clampW = w => Math.max(MIN_W, Math.min(MAX_W, Number(w) || CAM_W));

  function cameraFor(day, width) {
    const w = clampW(width || CAM_W), h = w * CAM_H / CAM_W;
    const [cx, cy] = dayPoint(day);
    const x = Math.max(0, Math.min(FULL[2] - w, cx - w * 0.5));
    const y = Math.max(0, Math.min(FULL[3] - h, cy - h * 0.5));
    return [x, y, w, h];
  }

  // --- Estado de cada paso a partir de lo marcado como hecho ---
  const missing = (step, completed) => step.required_members.filter(m => !((completed || {})[step.step_id] || []).includes(m));
  const isDone = (step, completed) => missing(step, completed).length === 0;

  // --- Montaña ---
  function svg(plan, day, completed, lang, zoomW) {
    const steps = (plan && plan.steps) || [];
    const byDay = {};
    steps.forEach(s => { (byDay[s.day] = byDay[s.day] || []).push(s); });
    const couple = !!(plan && plan.is_couple);
    const [x, y] = dayPoint(day);
    const progress = TRAIL.length * (1 - day / HORIZON);
    const dayWord = lang === 'EN' ? 'Day' : 'Día';

    const nodes = [];
    for (let d = 0; d <= HORIZON; d++) {
      const [nx, ny] = dayPoint(d);
      const list = byDay[d];
      if (list) {
        const done = list.every(s => isDone(s, completed));
        const late = !done && d < day;
        const cls = `dd-node dd-task${done ? ' is-done' : ''}${late ? ' is-late' : ''}${d === day ? ' is-today' : ''}`;
        nodes.push(`<g class="${cls}" transform="translate(${nx.toFixed(1)} ${ny.toFixed(1)})">
          <circle class="dd-node-ring" r="6.2"/>
          <path class="dd-node-tent" d="M -2.6 1.6 L 0 -3 L 2.6 1.6 Z"/>
          <text y="12" text-anchor="middle">${dayWord} ${d}</text>
        </g>`);
      } else {
        nodes.push(`<circle class="dd-node dd-dot${d <= day ? ' is-passed' : ''}" cx="${nx.toFixed(1)}" cy="${ny.toFixed(1)}" r="1.7"/>`);
      }
    }
    const climber = couple
      ? `<g id="ddClimber" class="dd-climber" transform="translate(${x.toFixed(1)} ${y.toFixed(1)})">
          <circle cx="-4" r="4" fill="var(--partner-a)" stroke="#fff" stroke-width="1.1"/>
          <circle cx="4" r="4" fill="var(--partner-b)" stroke="#fff" stroke-width="1.1"/>
        </g>`
      : `<g id="ddClimber" class="dd-climber" transform="translate(${x.toFixed(1)} ${y.toFixed(1)})">
          <circle r="7" fill="#141414" opacity=".14"/>
          <circle r="3.6" fill="#141414" stroke="#fff" stroke-width="1.2"/>
        </g>`;

    return `<svg class="mountain-svg dd-mountain" viewBox="${cameraFor(day, zoomW).map(n => n.toFixed(1)).join(' ')}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="${lang === 'EN' ? `Day-by-day climb, day ${day} of ${HORIZON}` : `Escalada día a día, día ${day} de ${HORIZON}`}" data-day="${day}">
      <defs>
        <filter id="ddDryBrush" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="3" result="noise"/>
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="1.8" xChannelSelector="R" yChannelSelector="G"/>
        </filter>
      </defs>
      <image class="mountain-art-base" href="assets/mountain-sumi.jpg" x="0" y="38" width="1200" height="675" preserveAspectRatio="xMidYMid meet"/>
      <path class="route-guide" d="${TRAIL_PATH}" stroke-width="1.4" filter="url(#ddDryBrush)"/>
      <path id="ddTrail" class="route-ink" d="${TRAIL_PATH}" stroke-width="2.5" stroke-dasharray="${TRAIL.length.toFixed(1)}" stroke-dashoffset="${progress.toFixed(1)}" filter="url(#ddDryBrush)"/>
      ${nodes.join('\n      ')}
      ${climber}
    </svg>`;
  }

  const readBox = svgEl => (svgEl.getAttribute('viewBox') || FULL.join(' ')).trim().split(/\s+/).map(Number);
  const clampBox = ([x, y, w, h]) => [
    Math.max(0, Math.min(FULL[2] - w, x)),
    Math.max(0, Math.min(FULL[3] - h, y)), w, h
  ];
  const writeBox = (svgEl, box) => svgEl.setAttribute('viewBox', box.map(n => n.toFixed(1)).join(' '));

  // Mover la cámara suavemente de una caja a otra (p. ej. recentrar con doble clic).
  function glide(svgEl, toBox, ms) {
    if (!svgEl || typeof requestAnimationFrame !== 'function') { if (svgEl) writeBox(svgEl, toBox); return; }
    const from = readBox(svgEl), t0 = performance.now(), dur = ms || 450;
    const token = (svgEl._ddAnim = (svgEl._ddAnim || 0) + 1);
    (function frame(now) {
      if (svgEl._ddAnim !== token || svgEl._ddDragging) return;
      const k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      writeBox(svgEl, from.map((v, i) => v + (toBox[i] - v) * e));
      if (k < 1) requestAnimationFrame(frame);
    })(t0);
  }

  // Ampliar/alejar la cámara. (cx, cy) = punto de pantalla que se queda fijo (null = centro).
  function zoomAt(svgEl, factor, cx, cy, onChange) {
    if (!svgEl) return null;
    svgEl._ddAnim = (svgEl._ddAnim || 0) + 1;
    const rect = svgEl.getBoundingClientRect();
    const box = readBox(svgEl);
    const rw = rect.width || 1, rh = rect.height || 1;
    const px = (cx == null ? rect.left + rw / 2 : cx) - (rect.left + rw / 2);
    const py = (cy == null ? rect.top + rh / 2 : cy) - (rect.top + rh / 2);
    const s = Math.min(box[2] / rw, box[3] / rh);                 // unidades de viewBox por píxel (slice)
    const w2 = clampW(box[2] * factor), h2 = w2 * box[3] / box[2];
    const s2 = s * (w2 / box[2]);
    const pointX = box[0] + box[2] / 2 + px * s, pointY = box[1] + box[3] / 2 + py * s;
    const next = clampBox([pointX - px * s2 - w2 / 2, pointY - py * s2 - h2 / 2, w2, h2]);
    writeBox(svgEl, next);
    if (onChange) onChange(next);
    return next;
  }

  // Arrastrar con el ratón (o el dedo) para recorrer la montaña. Doble clic: volver al escalador.
  function enablePan(svgEl, onChange) {
    if (!svgEl || svgEl._ddPan || typeof svgEl.addEventListener !== 'function') return;
    svgEl._ddPan = true;
    let drag = null;
    svgEl.addEventListener('wheel', ev => {
      ev.preventDefault();
      zoomAt(svgEl, Math.exp(ev.deltaY * 0.0015), ev.clientX, ev.clientY, onChange);
    }, { passive: false });
    svgEl.addEventListener('pointerdown', ev => {
      if (ev.button !== 0) return;
      const rect = svgEl.getBoundingClientRect();
      const box = readBox(svgEl);
      // preserveAspectRatio="slice": unidades de viewBox por píxel de pantalla.
      const scale = Math.min(box[2] / (rect.width || 1), box[3] / (rect.height || 1));
      drag = { x: ev.clientX, y: ev.clientY, box, scale, id: ev.pointerId };
      svgEl._ddDragging = true;
      svgEl._ddAnim = (svgEl._ddAnim || 0) + 1; // corta cualquier animación en curso
      svgEl.classList.add('is-dragging');
      if (svgEl.setPointerCapture) svgEl.setPointerCapture(ev.pointerId);
      ev.preventDefault();
    });
    svgEl.addEventListener('pointermove', ev => {
      if (!drag || ev.pointerId !== drag.id) return;
      const dx = (ev.clientX - drag.x) * drag.scale, dy = (ev.clientY - drag.y) * drag.scale;
      writeBox(svgEl, clampBox([drag.box[0] - dx, drag.box[1] - dy, drag.box[2], drag.box[3]]));
    });
    const end = ev => {
      if (!drag || (ev && ev.pointerId !== drag.id)) return;
      drag = null;
      svgEl._ddDragging = false;
      svgEl.classList.remove('is-dragging');
      if (onChange) onChange(readBox(svgEl));
    };
    svgEl.addEventListener('pointerup', end);
    svgEl.addEventListener('pointercancel', end);
    svgEl.addEventListener('dblclick', () => {
      const day = Number(svgEl.getAttribute('data-day')) || 0;
      const w = readBox(svgEl)[2];
      glide(svgEl, cameraFor(day, w));
      if (onChange) onChange(null, w);
    });
  }

  // Sube el nodo (y la cámara) del día anterior al nuevo.
  function animate(svgEl, fromDay, toDay, ms, fromBox, zoomW) {
    if (!svgEl || fromDay === toDay || typeof requestAnimationFrame !== 'function') return;
    const climber = svgEl.querySelector('#ddClimber');
    const trail = svgEl.querySelector('#ddTrail');
    const t0 = performance.now(), dur = ms || 650;
    const ease = t => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
    const fromCam = fromBox || cameraFor(fromDay, zoomW), toCam = cameraFor(toDay, zoomW);
    const token = (svgEl._ddAnim = (svgEl._ddAnim || 0) + 1);
    function frame(now) {
      if (svgEl._ddAnim !== token || svgEl._ddDragging) return;
      const k = ease(Math.min(1, (now - t0) / dur));
      const d = fromDay + (toDay - fromDay) * k;
      const [px, py] = dayPoint(d);
      if (climber) climber.setAttribute('transform', `translate(${px.toFixed(1)} ${py.toFixed(1)})`);
      if (trail) trail.setAttribute('stroke-dashoffset', (TRAIL.length * (1 - d / HORIZON)).toFixed(1));
      svgEl.setAttribute('viewBox', fromCam.map((v, i) => (v + (toCam[i] - v) * k).toFixed(1)).join(' '));
      if (k < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  // --- Tarjeta ---
  const T = {
    ES: {
      eyebrow: 'Día a día', of: 'de', today: 'Hoy te toca', noNew: 'Hoy no hay paso nuevo',
      pendingIntro: 'Pero sigue pendiente:', alsoPending: 'También sigue pendiente:',
      wait: 'Hoy toca esperar', waitNext: d => `Ya hiciste tu último paso. El siguiente llega el Día ${d}.`,
      waitEnd: 'Has completado todos los pasos del mes.', why: 'Por qué', missing: 'Falta', late: n => `hace ${n} ${n === 1 ? 'día' : 'días'}`,
      done: 'Hecho', reminder: 'Hoy te llega un recordatorio por Telegram: insistimos cada 2 días mientras siga pendiente.',
      sent: 'Enviado a Telegram', queued: 'Telegram no respondió: queda en cola', prev: '← Día anterior', next: 'Día siguiente →',
      loading: 'Cargando tu plan…', offline: 'El modo Día a Día necesita el servidor de Sherpas.', min: 'min'
    },
    EN: {
      eyebrow: 'Day by day', of: 'of', today: 'Today\'s step', noNew: 'No new step today',
      pendingIntro: 'Still pending:', alsoPending: 'Also still pending:',
      wait: 'Today you just wait', waitNext: d => `You completed your last step. The next one arrives on Day ${d}.`,
      waitEnd: 'You completed every step of the month.', why: 'Why', missing: 'Missing', late: n => `${n} ${n === 1 ? 'day' : 'days'} late`,
      done: 'Done', reminder: 'A Telegram reminder goes out today: we nudge every 2 days while it stays pending.',
      sent: 'Sent to Telegram', queued: 'Telegram did not answer: queued', prev: '← Previous day', next: 'Next day →',
      loading: 'Loading your plan…', offline: 'Day-by-day mode needs the Sherpas server.', min: 'min'
    }
  };

  function checks(step, plan, completed, L) {
    const names = {};
    ((plan && plan.members) || []).forEach(m => { names[m.id] = m.name; });
    const done = (completed || {})[step.step_id] || [];
    return `<div class="owner-split">${step.required_members.map(m => `<label><input type="checkbox" data-dd-step="${esc(step.step_id)}" data-dd-member="${esc(m)}" ${done.includes(m) ? 'checked' : ''}> ${esc(plan.is_couple ? names[m] || m : L.done)}</label>`).join('')}</div>`;
  }

  function stepBlock(step, plan, completed, L, extra, compact) {
    return `<div class="dd-step${isDone(step, completed) ? ' is-done' : ''}">
      <p class="dd-step-title"><strong>${esc(step.title)}</strong></p>
      ${compact ? '' : `<p>${esc(step.action_plain)}</p>`}
      ${extra || ''}
      ${step.why ? `<p class="dd-why"><span>${L.why}:</span> ${esc(step.why)}</p>` : ''}
      ${checks(step, plan, completed, L)}
    </div>`;
  }

  function card(ctx) {
    const lang = ctx.lang === 'EN' ? 'EN' : 'ES';
    const L = T[lang];
    const day = ctx.day;
    const head = `<p class="eyebrow">${L.eyebrow} · ${lang === 'EN' ? 'Day' : 'Día'} ${day} ${L.of} ${HORIZON}</p>`;
    const nav = `<div class="button-row dd-nav">
        <button type="button" data-action="dd-prev" ${day <= 0 ? 'disabled' : ''}>${L.prev}</button>
        <button type="button" class="primary" data-action="dd-next" ${day >= HORIZON ? 'disabled' : ''}>${L.next}</button>
      </div>`;
    let body;
    if (ctx.error) body = `<p>${L.offline}</p>`;
    else if (!ctx.plan || !ctx.status) body = `<p>${L.loading}</p>`;
    else {
      const st = ctx.status, plan = ctx.plan, completed = ctx.completed || {};
      const pendingBlocks = st.pending.map(p => stepBlock(p, plan, completed, L,
        `<p class="dd-late">${L.missing}: ${esc(p.missing_names.join(', '))} · ${L.late(p.days_late)}</p>`, true)).join('');
      if (st.mode === 'task') {
        body = `<h2>${L.today}</h2>${st.today.map(s => stepBlock(s, plan, completed, L)).join('')}
          ${st.pending.length ? `<p class="dd-sub">${L.alsoPending}</p>${pendingBlocks}` : ''}`;
      } else if (st.mode === 'pending') {
        body = `<h2>${L.noNew}</h2><p class="dd-sub">${L.pendingIntro}</p>${pendingBlocks}
          ${st.reminder_due ? `<aside class="inertia-alert"><p>📨 ${L.reminder}</p></aside>` : ''}`;
      } else {
        body = `<h2>${L.wait}</h2><p>${st.next_day != null ? L.waitNext(st.next_day) : L.waitEnd}</p>`;
      }
      if (ctx.notification && ctx.notification.configured) {
        body += `<p class="dd-telegram" data-tone="${ctx.notification.sent ? 'ok' : 'warn'}">📨 ${ctx.notification.sent ? L.sent : L.queued}: ${esc(ctx.notification.title)}</p>`;
      }
    }
    return `<aside class="floating-panel post-view dd-panel"><article class="focus-card">${head}${body}${nav}</article></aside>`;
  }

  return { svg, card, animate, enablePan, zoomAt, glide, clampBox, MIN_W, MAX_W, dayPoint, cameraFor, isDone, HORIZON, TRAIL_LENGTH: TRAIL.length };
});
