// Panel de demo de La Radio del Sherpa: cada botón manda UN mensaje real a Telegram.
// Solo aparece si el backend tiene SHERPAS_ENABLE_TELEGRAM_TEST=1 (GET /api/telegram/config).
(function () {
  'use strict';
  if (typeof document === 'undefined' || typeof fetch === 'undefined') return;

  const DAYS = [0, 3, 14, 30];

  function currentCase() {
    const sel = document.querySelector('select[data-case]');
    if (sel && sel.value) return sel.value;
    return new URLSearchParams(window.location.search || '').get('case') || 'michael-carter';
  }

  function post(path, body) {
    return fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }).then(r => r.json().then(data => ({ ok: r.ok, data })));
  }

  function build() {
    const panel = document.createElement('div');
    panel.className = 'radio-demo';
    panel.setAttribute('role', 'group');
    panel.setAttribute('aria-label', 'Demo La Radio del Sherpa');
    panel.innerHTML =
      '<span class="radio-demo-title">📻 Radio</span>' +
      DAYS.map(d => `<button type="button" data-demo-day="${d}">Día ${d}</button>`).join('') +
      '<button type="button" class="radio-demo-shock" data-demo-shock>📉 Cae la bolsa</button>' +
      '<span class="radio-demo-status" aria-live="polite"></span>';
    document.body.appendChild(panel);

    const status = panel.querySelector('.radio-demo-status');
    const show = (text, tone) => { status.textContent = text; status.dataset.tone = tone || ''; };

    panel.addEventListener('click', ev => {
      const btn = ev.target.closest('button');
      if (!btn) return;
      const caseId = currentCase();
      const isShock = btn.hasAttribute('data-demo-shock');
      const req = isShock
        ? post('/api/telegram/demo/shock', { case_id: caseId, drop_pct: 8 })
        : post('/api/telegram/demo/day', { case_id: caseId, day: Number(btn.dataset.demoDay) });
      panel.querySelectorAll('button').forEach(b => { b.disabled = true; });
      show('Enviando…');
      req.then(({ ok, data }) => {
        if (ok && data.sent) show('Enviado ✓', 'ok');
        else if (ok) show('n8n no respondió (queda en cola)', 'warn');
        else show((data && data.message) || 'Error', 'error');
      }).catch(() => show('Sin conexión con el backend', 'error'))
        .finally(() => { panel.querySelectorAll('button').forEach(b => { b.disabled = false; }); });
    });
  }

  function init() {
    fetch('/api/telegram/config')
      .then(r => (r.ok ? r.json() : null))
      .then(cfg => { if (cfg && cfg.demo_buttons) build(); })
      .catch(() => {});
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
