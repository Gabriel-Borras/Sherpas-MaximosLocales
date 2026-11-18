(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(root);
  else root.SherpaPostCima = factory(root);
})(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  'use strict';
  if (root.document) root.document.title = 'Sherpa Basecamp × Run IRL';

  const expedition = root.SherpaExpedicion || (typeof require === 'function' ? require('./expedicion.js') : null);
  const cases = root.SherpaCasesData || (typeof require === 'function' ? require('./cases-data.js') : null);
  const ids = cases.listCases().map(x => x.meta.slug);

  const owners = {
    'michael-carter': ['Michael'],
    'samantha-lewis': ['Samantha'],
    'timothy-melanie-weah': ['Timothy', 'Melanie'],
    'daniel-emily-johnson': ['Daniel', 'Emily']
  };

  const documentedInertia = {
    ES: {
      'michael-carter': '$3,500 Amex al 20% APR + $1,800/año ahorro fiscal 401(k) + $527/año tax drag JNK',
      'samantha-lewis': '$900,000 vivienda y $80,000 Porsche sin póliza registrada + $3,032/año tax drag',
      'timothy-melanie-weah': '$3,240/año en intereses de tarjeta al 18% APR ($18,000) frente a $150,800 en efectivo al 0.09% + $5,760/año ahorro fiscal 401(k)',
      'daniel-emily-johnson': '$18,000 en tarjeta al 24.9% APR + 0/20 en protección + $11,760/año ahorro fiscal 401(k)'
    },
    EN: {
      'michael-carter': '$3,500 Amex at 20% APR + $1,800/yr 401(k) tax savings + $527/yr JNK tax drag',
      'samantha-lewis': '$900,000 home and $80,000 Porsche with no policy on record + $3,032/yr tax drag',
      'timothy-melanie-weah': '$3,240/yr card interest at 18% APR ($18,000) vs. $150,800 cash at 0.09% + $5,760/yr 401(k) tax savings',
      'daniel-emily-johnson': '$18,000 card at 24.9% APR + 0/20 protection + $11,760/yr 401(k) tax savings'
    }
  };

  const plans = {
    ES: {
      'michael-carter': [
        'Paga el saldo Amex de $3,500 al 20% APR con los $27,000 de efectivo bancario.',
        'Aumenta las aportaciones 401(k) en $7,500 para ahorrar $1,800/año en impuestos y revisa el coste fiscal de JNK de $527/año.'
      ],
      'samantha-lewis': [
        'Confirma la póliza de vivienda de $900,000 y la póliza Porsche de $80,000.',
        'Añade $24,500 al 401(k), $4,400 a la HSA y aborda el coste fiscal anual de $3,032.'
      ],
      'timothy-melanie-weah': [
        'Melanie: paga el saldo de tarjeta de $18,000 al 18% APR.',
        'Timothy: reduce la exposición UPRO 3x y activa el 401(k), con $5,760/año de ahorro fiscal.'
      ],
      'daniel-emily-johnson': [
        'Juntos: detengan los desvíos a 529 y corretaje, aborden la tarjeta de $18,000 al 24.9% APR y pidan cotizaciones de seguro de vida.',
        'Activen aportaciones al 401(k), con $11,760/año de ahorro fiscal.'
      ]
    },
    EN: {
      'michael-carter': [
        'Pay off the Amex balance of $3,500 at 20% APR using the $27,000 bank cash.',
        'Raise 401(k) contributions by $7,500 for $1,800 yearly tax savings and review JNK tax drag of $527 a year.'
      ],
      'samantha-lewis': [
        'Confirm the $900,000 home policy and $80,000 Porsche policy.',
        'Add $24,500 to the 401(k), $4,400 to the HSA, and address $3,032 yearly tax drag.'
      ],
      'timothy-melanie-weah': [
        'Melanie: pay the $18,000 card balance at 18% APR.',
        'Timothy: reduce UPRO 3x exposure and activate 401(k), with $5,760 yearly tax savings.'
      ],
      'daniel-emily-johnson': [
        'Together: stop 529 and brokerage diversions, address the $18,000 card at 24.9% APR, and request life insurance quotes.',
        'Activate 401(k) contributions, with $11,760 yearly tax savings.'
      ]
    }
  };

  const esc = x => String(x == null ? '' : x).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const clean = x => esc(String(x == null ? '' : x).replace(/\*\*/g, '').replace(/^\s*#{1,6}\s+/gm, '').replace(/^\s*-\s+/gm, ''));
  const dataFor = id => cases.getCaseData(id);
  const langOf = s => (s && s.lang === 'EN' ? 'EN' : 'ES');
  const viewName = (key, lang, irlDay) => expedition.viewName(key, lang, irlDay);
  const viewKey = v => expedition.viewKey(v);
  const t = (s, k) => expedition.text[langOf(s)][k] || k;
  const money = n => {
    const value = Number(n);
    return Number.isFinite(value) ? (value < 0 ? '-$' : '$') + Math.abs(value).toLocaleString('en-US') : '—';
  };

  const ui = {
    ES: {
      run: 'Run IRL', day: 'Día', today: 'Acción inmediata · 3 minutos',
      completed: 'Pasos inmediatos completados', completedText: 'Todos los pasos inmediatos están al día para la revisión con tu asesor.',
      owner: 'Responsable', complete: 'Completar paso', step: 'Paso #', bucket: 'Categoría',
      current: 'Actual', target: 'Objetivo óptimo', delta: 'Diferencia', overdue: 'Inercia acumulada',
      inertia: 'Coste documentado de inercia', exact: 'Ver cálculo exacto',
      nextDay3: 'Día 3', nextDay14: 'Día 14', nextDay30: 'Día 30', nextMilestone: 'Próximo hito',
      radio: 'La Radio del Sherpa', download: 'Descargar calendario .ics', historical: 'Shock histórico',
      simulate: 'Simular caída bursátil hoy', through: 'Los activos atravesaron',
      historic: 'shocks de 2023 a 2026. La caída histórica es comparable; el plan ayuda a mantener la calma.',
      calm: 'Alerta de calma', fell: 'La cartera del hogar cayó', recovered: 'y se recuperó',
      hold: 'Mantén el plan y evita vender en el mínimo.', householdDrop: 'Caída del hogar',
      back: 'La cartera volvió a su nivel', benchmark: 'Referencia', recovery: 'recuperación',
      divergence: 'Divergencia', source: 'Fuente', maxDrop: 'Máxima caída a 3 años',
      prioritized: 'Top-3 preocupaciones y termómetro', subjective: 'Duda o inquietud subjetiva',
      contrast: 'Contraste: Preocupación #1 vs. Impacto cuantitativo',
      team: 'Diagnóstico, perfil de riesgo y pacto de pareja',
      selected: 'Top-3 elegido', priority: 'enfoque', noPriority: 'Sin enfoque seleccionado',
      none: 'ninguno', irl: 'Estado IRL e inercia', questions: 'Dudas para el asesor',
      housing: 'Hitos y transiciones', copy: 'Copiar resumen en texto plano',
      noQuestions: 'Sin dudas enviadas.', noDays: 'con recuperación en curso (sin días cerrados aún)'
    },
    EN: {
      run: 'Run IRL', day: 'Day', today: 'Immediate action · 3 minutes',
      completed: 'Immediate steps complete', completedText: 'All immediate steps are up to date for your advisor review.',
      owner: 'Owner', complete: 'Complete step', step: 'Step #', bucket: 'Bucket',
      current: 'Current', target: 'Optimal target', delta: 'Delta', overdue: 'Accumulated inertia',
      inertia: 'Documented cost of inertia', exact: 'See exact math',
      nextDay3: 'Day 3', nextDay14: 'Day 14', nextDay30: 'Day 30', nextMilestone: 'Next milestone',
      radio: 'Sherpa Radio', download: 'Download .ics calendar', historical: 'Historical shock',
      simulate: 'Simulate market drop today', through: 'Assets moved through',
      historic: 'shocks from 2023 to 2026. The historical decline is comparable; the plan helps preserve calm.',
      calm: 'Calm alert', fell: 'The household portfolio fell', recovered: 'and recovered',
      hold: 'Keep the plan and avoid selling at the low.', householdDrop: 'Household drawdown',
      back: 'The portfolio returned to its prior level', benchmark: 'Benchmark', recovery: 'recovery',
      divergence: 'Divergence', source: 'Source', maxDrop: 'Three-year maximum drawdown',
      prioritized: 'Top-3 concerns and thermometer', subjective: 'Open question or subjective note',
      contrast: 'Contrast: Priority #1 vs. Quantitative impact',
      team: 'Couple diagnosis, risk profile, and pact',
      selected: 'Top-3 picked', priority: 'focus', noPriority: 'No focus selected',
      none: 'none', irl: 'IRL state and inertia', questions: 'Questions for the advisor',
      housing: 'Milestones and transitions', copy: 'Copy plain-text summary',
      noQuestions: 'No questions sent.', noDays: 'recovery still underway (no closed day count)'
    }
  };
  const u = (s, k) => ui[langOf(s)][k];

  const initial = id => {
    const base = expedition.createInitialState(id);
    return Object.assign(base, {
      irlDay: 0,
      step: 0,
      checks: {},
      shock: 0,
      simulatedShock: false,
      view: viewName('expedition', langOf(base), 0),
      summit: false
    });
  };

  function dates(data, lang) {
    const found = new Map();
    const raw = ((data.persona && data.persona.transitionAlerts) || '').replace(/\*\*/g, '');
    const months = { January: 0, February: 1, March: 2, April: 3, May: 4, June: 5, July: 6, August: 7, September: 8, October: 9, November: 10, December: 11 };
    for (const m of raw.matchAll(/(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d{2})[^.\n]*/g)) {
      const date = new Date(Date.UTC(Number(m[2]), months[m[1]], 1)).toISOString().slice(0, 10);
      found.set(date, eventTitle(m[0], lang, date));
    }
    (((data.goals || {}).chartGoals) || []).forEach(g => {
      const m = JSON.stringify(g).match(/20\d{2}/);
      if (m) {
        const date = m[0] + '-01-01';
        found.set(date, eventTitle(String(g.label || g.title || g.name || ''), lang, date));
      }
    });
    return [...found].sort((a, b) => a[0].localeCompare(b[0])).map(([date, title]) => ({ date, title }));
  }

  function eventTitle(title, lang, date) {
    if (lang === 'EN') return title || `Plan milestone ${date.slice(0, 4)}`;
    const x = String(title).toLowerCase(), year = date.slice(0, 4);
    if (x.includes('home') || x.includes('house')) return 'Compra de vivienda';
    if (x.includes('retir')) {
      const person = ['michael', 'samantha', 'timothy', 'daniel'].find(name => x.includes(name));
      return person ? `Jubilación de ${person[0].toUpperCase() + person.slice(1)}` : 'Jubilación';
    }
    if (x.includes('vacation')) return 'Vacaciones anuales';
    if (x.includes('college') || x.includes('education')) return 'Universidad';
    if (x.includes('vehicle')) return 'Compra de vehículo';
    return `Hito del plan ${year}`;
  }

  function calendar(id, lang) {
    const locale = lang === 'EN' ? 'EN' : 'ES';
    const events = [3, 14, 30].map(n => ({
      date: new Date(Date.UTC(2026, 10, 18 + n)).toISOString().slice(0, 10),
      title: `Run IRL · ${locale === 'ES' ? 'Día' : 'Day'} ${n}`
    })).concat(dates(dataFor(id), locale));
    const escapeIcs = s => String(s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');
    return [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      `PRODID:-//Sherpas//Run IRL//${locale}`,
      ...events.map((e, i) => `BEGIN:VEVENT\r\nUID:sherpas-${id}-${i}@local\r\nDTSTAMP:20261118T120000Z\r\nDTSTART;VALUE=DATE:${e.date.replace(/-/g, '')}\r\nSUMMARY:${escapeIcs(e.title)}\r\nEND:VEVENT`),
      'END:VCALENDAR'
    ].join('\r\n');
  }

  const recovery = (value, missing, lang) => {
    const n = Number(value);
    const valid = (typeof value === 'number' || (typeof value === 'string' && value.trim() !== '')) && Number.isFinite(n);
    return valid ? (lang === 'ES' ? `en ${n} días` : `in ${n} days`) : (missing || (lang === 'ES' ? 'sin días de recuperación cerrados' : 'no closed recovery-day count'));
  };

  function view(state) {
    state = state || initial(ids[0]);
    const lang = langOf(state);
    const key = viewKey(state.view);

    // Delegate Basecamp view (both before and after summit) to expedition.render
    if (key === 'expedition' || key === 'overview') {
      return expedition.render(state);
    }

    const raw = dataFor(state.caseId);
    const d = expedition.localizeData(raw, lang);
    const steps = plans[lang][state.caseId] || [];
    const current = steps[Math.min(state.step, Math.max(0, steps.length - 1))] || '';
    const checks = state.checks[state.step] || [];
    const couple = !!(d.meta && d.meta.isCouple);
    const docInertia = (documentedInertia[lang] && documentedInertia[lang][state.caseId]) || '';
    const record = expedition.riskRecord(state.caseId, lang);
    const campIdx = state.summit ? 3 : (state.irlDay < 14 ? 0 : state.irlDay < 365 ? 1 : 2);
    const campBiome = expedition.biomes[campIdx];
    const contrast = expedition.buildContrastSummary(state, d);
    const rankLabels = expedition.text[lang].rankBadge;
    const top3List = ((state.fearOrder && state.fearOrder.length ? state.fearOrder : ((d.persona.objectiveConcerns || []).slice(0, 3).map(c => c.id))) || []).slice(0, 3);
    const top3Formatted = top3List.map((id, idx) => {
      const found = (d.persona.objectiveConcerns || []).find(c => c.id === id);
      return `${rankLabels[idx] || `#${idx + 1}`}: ${found ? found.title : id}`;
    }).join(' · ');
    const thermoLvl = Math.max(1, Math.min(5, Number(state.thermometer) || 3));
    const thermoText = (expedition.thermoLabels && expedition.thermoLabels[lang] && expedition.thermoLabels[lang][thermoLvl]) || `${thermoLvl}/5`;

    // Full-bleed permanent 100vw x 100vh Sumi-e Mountain Wallpaper behind Día X, Brief, and Radio
    const wallpaper = `<div class="mountain-stage mountain-fullscreen" data-biome="${campBiome.id}">
      ${expedition.svgMarkup(campBiome.offset, campBiome.point, state.history || [], false, couple, state.votes, record, lang, { stage: campIdx })}
    </div>`;

    let panel = '';
    if (key === 'current') {
      const elapsed = Math.max(0, state.irlDay - (state.stepAt || 0));
      const wf = (d.savingsWaterfall || []).find(x => Number(x.step) === (state.step === 0 ? (state.caseId === 'samantha-lewis' ? 2 : 8) : 13)) || {};
      const done = state.step >= steps.length;
      const inertiaText = `${elapsed} ${lang === 'ES' ? 'días con paso pendiente ·' : 'days with pending step ·'} ${docInertia}.`;
      const peopleList = owners[state.caseId] || ((d.meta && d.meta.owners) || []).map(o => o.name) || ['A'];

      panel = `<aside class="floating-panel post-view">
        <article class="focus-card">
          <p class="eyebrow">${u(state, 'run')} · ${u(state, 'day')} ${state.irlDay}</p>
          <div class="irl-eval-recap">
            <p class="preview"><strong>${esc(top3Formatted)}</strong> · <span>${esc(thermoText)}</span></p>
            <p class="preview">${esc(contrast.blindSpotText)}</p>
          </div>
          ${done
            ? `<h2>${u(state, 'completed')}</h2><p>${u(state, 'completedText')}</p>`
            : `<p class="eyebrow">${u(state, 'today')}</p>
               <h2>${esc(current)}</h2>
               <div class="owner-split">${peopleList.map((n, i) => `<label><input type="checkbox" data-owner="${i}" ${checks.includes(i) ? 'checked' : ''}> ${u(state, 'owner')} ${i ? 'B' : 'A'} · ${esc(n)}</label>`).join('')}</div>
               <div class="button-row"><button class="primary" data-action="done" ${checks.length < (couple ? 2 : 1) ? 'disabled' : ''}>${u(state, 'complete')} (${checks.length}/${couple ? 2 : 1})</button></div>`}
          ${elapsed ? `<aside class="inertia-alert"><strong>${u(state, 'overdue')}</strong><p>${esc(inertiaText)}</p></aside>` : ''}
          <details class="exact-math">
            <summary>${u(state, 'exact')}</summary>
            <dl class="waterfall-detail">
              <dt>${u(state, 'step')}</dt><dd>${esc(wf.step ?? '—')}</dd>
              <dt>${u(state, 'bucket')}</dt><dd>${esc(wf.bucket ?? '—')}</dd>
              <dt>${u(state, 'current')}</dt><dd>${money(wf.current)}</dd>
              <dt>${u(state, 'target')}</dt><dd>${money(wf.target)}</dd>
              <dt>${u(state, 'delta')}</dt><dd>${money(wf.delta)}</dd>
              <dt>${u(state, 'inertia')}</dt><dd>${esc(docInertia)}</dd>
            </dl>
          </details>
        </article>
        <section class="irl-timeline">
          <p class="eyebrow">${u(state, 'day')} 0 → ${u(state, 'day')} 3 → ${u(state, 'day')} 14 → ${u(state, 'day')} 30 → ${lang === 'ES' ? 'Hito' : 'Milestone'}</p>
          ${[[3, u(state, 'nextDay3')], [14, u(state, 'nextDay14')], [30, u(state, 'nextDay30')], [365, u(state, 'nextMilestone')]].map(x => `<button data-action="day" data-day="${x[0]}">${x[1]}</button>`).join('')}
        </section>
      </aside>`;
    } else if (key === 'radio') {
      const sh = d.shocks || [];
      const s = sh[state.shock] || {};
      const dd = s.drawdown || {};
      const hh = dd.household || {};
      const bench = dd.sameRiskBenchmark || {};
      const pct = n => {
        const x = Number(n || 0);
        const v = Math.abs(x * 100) < 0.1 ? 0 : Math.round(x * 1000) / 10;
        return v.toFixed(1) + '%';
      };

      panel = `<aside class="floating-panel panel-wide post-view">
        <p class="eyebrow">${u(state, 'radio')}</p>
        <h1>${u(state, 'radio')}</h1>
        <div class="radio-box">
          <div class="radio-controls">
            <div class="button-row">
              <button data-action="ics">${u(state, 'download')}</button>
              <button class="primary" data-action="simulate-shock">${u(state, 'simulate')}</button>
            </div>
            <label>${u(state, 'historical')}
              <select data-shock class="shock-picker">${sh.map((x, i) => `<option value="${i}" ${i === state.shock ? 'selected' : ''}>${esc(x.dateLabel || '')} · ${esc(x.name || '')}</option>`).join('')}</select>
            </label>
          </div>
          <p>${u(state, 'through')} ${sh.length} ${u(state, 'historic')}</p>
          ${state.simulatedShock ? `<aside class="calm-alert" data-simulated-shock="true"><strong>${u(state, 'calm')}: ${esc(s.name || '')}</strong><p>${u(state, 'fell')} ${pct(hh.drawdownPct)} ${u(state, 'recovered')} ${esc(recovery(hh.recoveryDays, u(state, 'noDays'), lang))}. ${u(state, 'hold')}</p></aside>` : ''}
          <div class="shock-detail">
            <h2>${esc(s.name || u(state, 'historical'))}</h2>
            <p>${esc(s.dateLabel || '')} · ${esc(s.portfolioImpact || '')} · ${u(state, 'householdDrop')}: ${pct(hh.drawdownPct)} (${u(state, 'back')} ${esc(recovery(hh.recoveryDays, u(state, 'noDays'), lang))}).</p>
            <p>${clean(s.description)}</p>
            ${state.caseId === 'timothy-melanie-weah' ? `<p>UPRO ${lang === 'ES' ? 'añade exposición apalancada 3x.' : 'adds 3x leveraged exposure.'}</p>` : ''}
            <details class="exact-math">
              <summary>${u(state, 'exact')}</summary>
              <ul>
                <li><strong>${u(state, 'benchmark')}:</strong> ${pct(bench.drawdownPct)} (${u(state, 'recovery')} ${esc(recovery(bench.recoveryDays, '', lang))})</li>
                <li><strong>${u(state, 'divergence')}:</strong> ${(Number(dd.divergencePp || 0) * 100).toFixed(1)} pp</li>
                <li><strong>Sharpe 3y:</strong> ${Number((d.performanceSummary.benchmark && d.performanceSummary.benchmark.sharpe3y) || d.performanceSummary.sharpe3y || 0).toFixed(2)}</li>
                <li><strong>${u(state, 'maxDrop')}:</strong> ${pct(d.performanceSummary.maxDrawdown3y)} (${u(state, 'recovery')} ${esc(recovery(d.performanceSummary.maxDrawdownRecoveryDays, '', lang))})</li>
                <li><strong>${u(state, 'source')}:</strong> analysis.events / perEventDrawdowns</li>
              </ul>
            </details>
          </div>
        </div>
      </aside>`;
    } else {
      const priority = {
        crecimiento: lang === 'ES' ? 'Priorizar crecimiento patrimonial' : 'Prioritize long-term growth',
        'deuda-proteccion': lang === 'ES' ? 'Priorizar liquidez, deuda y protección' : 'Prioritize liquidity, debt, and protection',
        'liquidez-vivienda': lang === 'ES' ? 'Asegurar liquidez y vivienda' : 'Secure liquidity and housing'
      };
      const peopleList = owners[state.caseId] || ((d.meta && d.meta.owners) || []).map(o => o.name) || ['A', 'B'];
      panel = `<aside class="floating-panel panel-wide post-view">
        <p class="eyebrow">${t(state, 'brief')}</p>
        <h1>${t(state, 'brief')}</h1>
        <div class="brief-grid">
          <section>
            <h2>${u(state, 'prioritized')}</h2>
            <p><strong>${esc(top3Formatted)}</strong></p>
            <p><strong>${t(state, 'thermometerTitle')}:</strong> ${esc(thermoText)}</p>
            <h2>${u(state, 'contrast')}</h2>
            <p>${esc(contrast.blindSpotText)}</p>
            <h2>${u(state, 'subjective')}</h2>
            <p>${clean(state.subjectiveConcern || d.persona.subjectiveConcerns)}</p>
            <h2>${u(state, 'team')}</h2>
            <p>${clean(d.persona.D6 || '')}</p>
            <p><strong>${t(state, 'profileSplitTitle')}:</strong> ${esc(d.persona.D4Human || '')}</p>
            ${couple ? ['A', 'B'].map((k, i) => {
              const vote = (state.votes && state.votes[k]) || {};
              const fears = (vote.fears || []).map((id, rIdx) => {
                const c = (d.persona.objectiveConcerns || []).find(x => x.id === id);
                return `${rankLabels[rIdx] || `#${rIdx + 1}`} ${c ? c.title : id}`;
              });
              const vThermo = vote.thermometer ? ((expedition.thermoLabels && expedition.thermoLabels[lang][vote.thermometer]) || `${vote.thermometer}/5`) : thermoText;
              return `<p><strong>${esc(peopleList[i] || k)}:</strong> ${u(state, 'selected')} (${fears.length ? esc(fears.join(', ')) : u(state, 'none')}) · ${esc(vThermo)} · ${u(state, 'priority')}: ${esc(priority[vote.priority] || u(state, 'noPriority'))}.</p>`;
            }).join('') : ''}
            ${(d.persona.tensions || []).map(x => `<p>${clean(x.detail)}</p>`).join('')}
          </section>
          <section>
            <h2>${t(state, 'discarded')}</h2>
            ${(state.history || []).map(h => `<p><strong>${esc((h.campLabel && h.campLabel[lang]) || expedition.biomes[h.stage || 0][lang])}:</strong> ${esc((h.decisionChosen && h.decisionChosen[lang]) || t(state, 'ignore'))} → ${esc(record.label)}</p>`).join('') || `<p>${t(state, 'noDiscarded')}</p>`}
            <h2>${u(state, 'irl')}</h2>
            <p>${u(state, 'day')} ${state.irlDay} · ${state.step + 1}/${steps.length} · ${esc(docInertia)}</p>
            <h2>${u(state, 'questions')}</h2>
            ${(state.advisorDoubts || []).map(x => `<p>${clean(x)}</p>`).join('') || `<p>${u(state, 'noQuestions')}</p>`}
            <h2>${u(state, 'housing')}</h2>
            <p>${clean(d.persona.transitionAlerts || '')}</p>
          </section>
        </div>
        <details class="exact-math">
          <summary>${u(state, 'exact')}</summary>
          ${expedition.yearlyMarkup(d, lang)}
        </details>
        <div class="button-row"><button data-action="copy">${u(state, 'copy')}</button></div>
      </aside>`;
    }

    return `${expedition.renderHeader(state, d)}<main class="page-shell page-mountain-full">${wallpaper}${panel}</main>`;
  }

  function mount(target, opts) {
    const el = typeof target === 'string' ? root.document.querySelector(target) : target;
    if (!el) throw Error('Sherpa container was not found');
    let state = initial((opts && opts.caseId) || ids[0]);
    const syncViewport = () => {
      if (root.document && root.document.body) {
        root.document.body.classList.add('is-mountain-viewport');
      }
    };
    let unsubRoom = null;
    const attachRoom = () => {
      if (unsubRoom) { try { unsubRoom(); } catch (_) {} unsubRoom = null; }
      const raw = dataFor(state.caseId) || {};
      if (raw.meta && raw.meta.isCouple && state.roomId && expedition.CoupleRoomSync) {
        expedition.CoupleRoomSync.createRoom(state.caseId, state.roomId);
        unsubRoom = expedition.CoupleRoomSync.subscribe(state.roomId, state.caseId, roomData => {
          expedition.applyRoomSnapshot(state, roomData, el, render, summit);
        });
      }
    };
    const render = () => {
      el.innerHTML = view(state);
      syncViewport();
      bind();
    };
    function summit() {
      state.summit = true;
      state.phase = 'summit';
      state.irlDay = 0;
      state.stepAt = 0;
      state.view = viewName('current', langOf(state), state.irlDay);
      if (expedition.SherpasAI) {
        expedition.SherpasAI.request('brief', {
          case_id: state.caseId,
          fear_ranking: state.fearOrder || [],
          subjective_concerns: state.subjectiveConcern || ''
        }, { mode: 'deterministic' });
      }
      render();
    }
    function bind() {
      el.querySelectorAll('[data-action]').forEach(b => b.onclick = (ev) => {
        if (b.tagName === 'A' && ev && ev.preventDefault) ev.preventDefault();
        const a = b.dataset.action;
        if (expedition.handleMountainAction(a, b, el, state, render, summit)) return;
        if (a === 'doubt') {
          state.advisorDoubts.push(b.dataset.doubt || '');
        } else if (a === 'nav') {
          state.view = b.dataset.view;
          const vk = viewKey(state.view);
          if (vk === 'brief' && expedition.SherpasAI) {
            expedition.SherpasAI.request('brief', {
              case_id: state.caseId,
              fear_ranking: state.fearOrder || [],
              subjective_concerns: state.subjectiveConcern || ''
            }, { mode: 'deterministic' });
          }
          if (vk === 'expedition' || vk === 'overview') {
            if (state.summit || vk === 'overview') {
              state.cameraMode = 'panoramic';
              state.dialogVisible = false;
              state.initialViewBox = expedition.fullCamera.slice();
            } else if (state.phase === 'expedition' || state.phase === 'blocked') {
              state.dialogVisible = true;
              state.initialViewBox = expedition.campCamera(state.focusedNode != null ? state.focusedNode : state.stage);
            }
          }
        } else if (a === 'mode') {
          state.mode = b.dataset.mode;
        } else if (a === 'lang') {
          state.lang = b.dataset.lang === 'EN' ? 'EN' : 'ES';
          expedition.persistLanguage(state.lang);
          state.view = viewName(viewKey(state.view), state.lang, state.irlDay);
        } else if (a === 'repeat') {
          const lang = state.lang;
          state = initial(state.caseId);
          state.lang = lang;
        } else if (a === 'day') {
          if (b.dataset.day === '365') {
            const base = new Date(Date.UTC(2026, 10, 18 + state.irlDay));
            const next = dates(dataFor(state.caseId), langOf(state)).map(x => new Date(x.date + 'T00:00:00Z')).find(x => x > base);
            state.irlDay = next ? Math.round((next - new Date(Date.UTC(2026, 10, 18))) / 86400000) : state.irlDay + 365;
          } else {
            state.irlDay = Number(b.dataset.day);
          }
          if (viewKey(state.view) === 'current') {
            state.view = viewName('current', langOf(state), state.irlDay);
          }
        } else if (a === 'done') {
          state.step++;
          state.stepAt = state.irlDay;
          state.checks[state.step] = [];
        } else if (a === 'ics') {
          const blob = new Blob([calendar(state.caseId, langOf(state))], { type: 'text/calendar' });
          const link = document.createElement('a');
          link.href = URL.createObjectURL(blob);
          link.download = 'sherpas-run-irl.ics';
          link.click();
        } else if (a === 'simulate-shock') {
          state.shock = (state.shock + 1) % (dataFor(state.caseId).shocks || []).length;
          state.simulatedShock = true;
        } else if (a === 'copy') {
          const pv = el.querySelector('.post-view');
          if (pv && root.navigator && root.navigator.clipboard) {
            root.navigator.clipboard.writeText(pv.innerText);
          }
        }
        render();
        state.initialViewBox = null;
      });
      const c = el.querySelector('[data-case]');
      if (c) c.onchange = () => {
        const lang = state.lang;
        state = initial(c.value);
        state.lang = lang;
        attachRoom();
        render();
      };
      const s = el.querySelector('[data-shock]');
      if (s) s.onchange = () => {
        state.shock = Number(s.value);
        render();
      };
      el.querySelectorAll('[data-owner]').forEach(chk => chk.onchange = () => {
        const a = state.checks[state.step] || [];
        const v = Number(chk.dataset.owner);
        state.checks[state.step] = chk.checked ? [...new Set([...a, v])] : a.filter(x => x !== v);
        render();
      });
      el.querySelectorAll('[data-fear]').forEach(chk => chk.onchange = () => {
        state.fearOrder = [...el.querySelectorAll('[data-fear]:checked')].map(x => x.dataset.fear).slice(0, 3);
      });
      el.querySelectorAll('[data-priority]').forEach(n => n.onchange = () => {
        const raw = dataFor(state.caseId) || {};
        if (raw.meta && raw.meta.isCouple) {
          const turn = state.voteTurn === 'B' ? 'B' : 'A';
          state.votes = state.votes || {};
          state.votes[turn] = Object.assign({ fears: [], thermometer: 3 }, state.votes[turn], { priority: n.value });
        }
        state.priorityFocus = n.value;
        render();
      });
      const th = el.querySelector('[data-thermometer]');
      if (th) th.oninput = () => {
        const lvl = Math.max(1, Math.min(5, Number(th.value) || 3));
        state.thermometer = lvl;
        const raw = dataFor(state.caseId) || {};
        if (raw.meta && raw.meta.isCouple && state.phase === 'fears') {
          const turn = state.voteTurn === 'B' ? 'B' : 'A';
          state.votes = state.votes || {};
          state.votes[turn] = Object.assign({ fears: [] }, state.votes[turn], { thermometer: lvl });
        }
        render();
      };
      const sub = el.querySelector('[data-subjective]');
      if (sub) sub.oninput = () => {
        const raw = dataFor(state.caseId) || {};
        if (raw.meta && raw.meta.isCouple && state.phase === 'fears') {
          const turn = state.voteTurn === 'B' ? 'B' : 'A';
          state.votes = state.votes || {};
          state.votes[turn] = Object.assign({ fears: [], thermometer: 3 }, state.votes[turn], { subjective: sub.value });
        } else {
          state.subjectiveConcern = sub.value;
        }
      };
      el.querySelectorAll('[name="route"]').forEach(r => r.onchange = () => {
        const p = el.querySelector('[data-preview]');
        if (p) p.textContent = expedition.preview(state, expedition.localizeData(dataFor(state.caseId), langOf(state)), r.value);
      });
    }
    attachRoom();
    render();
    return {
      getState: () => state,
      setState(next) { state = next; attachRoom(); render(); return state; },
      dispatch(a, v) {
        if (a === 'nav') state.view = v;
        else if (a === 'mode') state.mode = v;
        else if (a === 'lang') {
          state.lang = v === 'EN' ? 'EN' : 'ES';
          expedition.persistLanguage(state.lang);
          state.view = viewName(viewKey(state.view), state.lang, state.irlDay);
        } else if (a === 'summit') {
          state.summit = true;
          state.phase = 'summit';
          state.view = viewName('current', langOf(state), state.irlDay);
        }
        render();
        return state;
      },
      unmount() {
        if (unsubRoom) { try { unsubRoom(); } catch (_) {} unsubRoom = null; }
        el.innerHTML = '';
        if (root.document && root.document.body) root.document.body.classList.remove('is-mountain-viewport');
      }
    };
  }

  return { createInitialState: initial, render: view, mount, makeIcs: calendar };
});
