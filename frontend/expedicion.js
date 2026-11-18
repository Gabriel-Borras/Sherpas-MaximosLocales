(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(root);
  else root.SherpaExpedicion = factory(root);
})(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  'use strict';
  if (root.document) root.document.title = 'Sherpa Basecamp × Run IRL';

  const ids = ['michael-carter', 'samantha-lewis', 'timothy-melanie-weah', 'daniel-emily-johnson'];
  const api = root.SherpaCasesData || (typeof require === 'function' ? require('./cases-data.js') : null);
  const esc = x => String(x == null ? '' : x).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const clean = x => esc(x).replace(/^\s*-\s*/, '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  const dataFor = id => (api && api.getCaseData ? api.getCaseData(id) : (api && api.CASES_DATA && api.CASES_DATA[id]));
  const listCases = () => (api && api.listCases ? api.listCases() : ids.map(dataFor).filter(Boolean));
  const langOf = s => (s && s.lang === 'EN' ? 'EN' : 'ES');
  const loadLang = () => { try { return root.localStorage && root.localStorage.getItem('sherpas_lang') === 'EN' ? 'EN' : 'ES'; } catch (_) { return 'ES'; } };
  const persistLanguage = lang => { try { if (root.localStorage) root.localStorage.setItem('sherpas_lang', lang); } catch (_) {} };

  const words = {
    ES: {
      expedition: 'Expedición', current: 'Paso actual', overview: 'Mapa general', brief: 'Resumen para el asesor', radio: 'Radio',
      select: 'Seleccionar hogar', nav: 'Navegación', reading: 'Modo de lectura', plain: 'Simple', math: 'Métricas', plan: 'Plan financiero',
      fears: 'Fase 1A · Consulta de miedos', fearTitle: '¿Qué merece atención primero?',
      fearHelp: 'Ordena tus preocupaciones. Tus respuestas se guardan para el resumen del asesor.', fearAsk: '¿Qué te preocupa hoy?',
      continue: 'Continuar a la cordada', enter: 'Entrar a la montaña',
      team: 'Fase 1B · Cordada a ciegas · 60 segundos', private: 'Voto privado de',
      clock: 'El reloj no bloquea el avance. La otra persona no verá estas respuestas hasta el cruce.',
      growth: 'Priorizar crecimiento', debt: 'Priorizar deuda y protección', time: 'Tiempo disponible',
      save: 'Guardar y pasar a la otra persona', matches: 'Ver coincidencias', cross: 'Cruce de respuestas',
      agree: 'En qué coincidís al 100%', friction: 'Roces para conversar', pact: 'Pacto de flujo de caja',
      blocked: 'Bloqueo en la grieta', stopped: 'La ruta se detiene aquí', impact: 'Consecuencia proyectada',
      context: 'Contexto adicional', tensions: 'Tensiones y sesgo aplicado', rewind: 'Rebobinar',
      phase: 'Fase 2 · Gran expedición', route: 'Una ruta, cuatro campamentos', choose: 'Elige un paso de campamento',
      ignore: 'Seguir sin atender la tensión principal', confirm: 'Confirmar paso', doubt: 'Enviar duda al resumen del asesor',
      trend: 'Tendencia prevista', exact: 'Datos exactos del plan', levers: 'Palancas individuales', none: 'Sin palancas registradas',
      yearly: 'Proyección anual', facts: 'Datos factuales', sources: 'Fuentes', concerns: 'Miedos y preocupaciones',
      noAnswer: 'Sin respuesta registrada.', couple: 'Pacto de pareja', questions: 'Dudas para el asesor',
      noQuestions: 'No hay dudas registradas.', discarded: 'Ramas descartadas', noDiscarded: 'Aún no hay ramas descartadas.',
      complete: 'Expedición completada', continueExpedition: 'Continuar expedición', repeat: 'Repetir expedición',
      next: 'Tu siguiente objetivo inmediato es revisar el paso acordado con tu asesor.',
      mapAria: 'Mapa topográfico de la expedición', risk: 'Ruta en riesgo',
      chart: 'Proyección anual: activos invertibles y patrimonio neto',
      chartAria: 'Comparación anual entre activos invertibles y patrimonio neto',
      blue: 'Azul: activos invertibles', green: 'Verde: patrimonio neto',
      different: 'Prioridad distinta', common: 'No aparece una diferencia de prioridad; revisen juntos las tensiones del plan.',
      panoramic: 'Panorámica', focusActive: 'Volver al campamento activo',
      panoramicHint: 'Toca un micro-campamento para hacer zoom o vuelve al campamento activo.',
      inspectCamp: 'Vista del campamento',
      yearlyToggle: 'Ver proyección anual (activos invertibles vs. patrimonio)'
    },
    EN: {
      expedition: 'Expedition', current: 'Current step', overview: 'Overview map', brief: 'Advisor Brief', radio: 'Radio',
      select: 'Select household', nav: 'Navigation', reading: 'Reading mode', plain: 'Plain', math: 'Math', plan: 'Financial plan',
      fears: 'Phase 1A · Fear quest', fearTitle: 'What deserves attention first?',
      fearHelp: 'Rank your concerns. Your answers are saved for the Advisor Brief.', fearAsk: 'What concerns you today?',
      continue: 'Continue to the rope team', enter: 'Enter the mountain',
      team: 'Phase 1B · Blind rope team · 60 seconds', private: 'Private vote by',
      clock: 'The clock does not block progress. The other person will not see these answers until the cross-check.',
      growth: 'Prioritize growth', debt: 'Prioritize debt and protection', time: 'Time available',
      save: 'Save and pass to the other person', matches: 'See matches', cross: 'Cross-check',
      agree: 'Where you agree 100%', friction: 'Tensions to discuss', pact: 'Cash-flow pact',
      blocked: 'Blocked at the crevasse', stopped: 'The route stops here', impact: 'Projected consequence',
      context: 'Additional context', tensions: 'Tensions and applied bias', rewind: 'Rewind',
      phase: 'Phase 2 · Grand expedition', route: 'One route, four camps', choose: 'Choose a camp step',
      ignore: 'Continue without addressing the main tension', confirm: 'Confirm step', doubt: 'Send question to Advisor Brief',
      trend: 'Expected trend', exact: 'Exact plan data', levers: 'Individual levers', none: 'No recorded levers',
      yearly: 'Yearly projection', facts: 'Facts', sources: 'Sources', concerns: 'Fears and concerns',
      noAnswer: 'No answer recorded.', couple: 'Couple pact', questions: 'Questions for the advisor',
      noQuestions: 'No questions recorded.', discarded: 'Discarded branches', noDiscarded: 'No discarded branches yet.',
      complete: 'Expedition complete', continueExpedition: 'Continue expedition', repeat: 'Repeat expedition',
      next: 'Your next immediate goal is to review the agreed step with your advisor.',
      mapAria: 'Topographic expedition map', risk: 'Route at risk',
      chart: 'Yearly projection: investable assets and net worth',
      chartAria: 'Yearly comparison of investable assets and net worth',
      blue: 'Blue: investable assets', green: 'Green: net worth',
      different: 'Different priority', common: 'No priority difference appears; review the plan tensions together.',
      panoramic: 'Overview', focusActive: 'Focus active camp',
      panoramicHint: 'Click a micro-camp to zoom in or return to the active camp.',
      inspectCamp: 'Camp preview',
      yearlyToggle: 'View yearly projection (investable assets vs. net worth)'
    }
  };
  const campShorts = { ES: ['Base', 'C1', 'C2', 'Cima'], EN: ['Base', 'C1', 'C2', 'Summit'] };
  const t = (s, k) => words[langOf(s)][k] || k;
  const viewName = (key, lang) => words[lang === 'EN' ? 'EN' : 'ES'][key];
  const viewKey = value => ['expedition', 'current', 'overview', 'brief', 'radio'].find(k => value === words.ES[k] || value === words.EN[k]) || 'expedition';

  const TRAIL_PATH = 'M 190 610 Q 285 552 390 465 Q 505 385 620 295 Q 725 222 830 130';
  const TRAIL_LENGTH = 800;
  const fullCamera = [0, 0, 1200, 750];

  const biomes = [
    { id: 'forest', point: [190, 610], offset: 800, ES: 'Campamento Base · Bosque · 2.800 m', EN: 'Basecamp · Forest · 2,800 m' },
    { id: 'rock', point: [390, 465], offset: 553, ES: 'Campo 1 · Roca y niebla · 4.600 m', EN: 'Camp 1 · Rock and fog · 4,600 m' },
    { id: 'snow', point: [620, 295], offset: 267, ES: 'Campo 2 · Glaciar · 6.900 m', EN: 'Camp 2 · Glacier · 6,900 m' },
    { id: 'summit', point: [830, 130], offset: 0, ES: 'La Cima · Meta alcanzada · 8.848 m', EN: 'Summit · Goal reached · 8,848 m' }
  ];
  const biome = (i, lang) => Object.assign({}, biomes[i], { label: biomes[i][lang] });

  const specs = {
    'michael-carter': {
      ES: { people: ['Michael'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Revisa las medidas documentadas del plan antes de avanzar.', pact: 'Acordar el siguiente paso con el asesor.', events: [] },
      EN: { people: ['Michael'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Review the plan’s documented moves before advancing.', pact: 'Agree the next step with the advisor.', events: [] }
    },
    'samantha-lewis': {
      ES: { people: ['Samantha'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Revisa las medidas documentadas del plan antes de avanzar.', pact: 'Acordar el siguiente paso con el asesor.', events: [] },
      EN: { people: ['Samantha'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Review the plan’s documented moves before advancing.', pact: 'Agree the next step with the advisor.', events: [] }
    },
    'timothy-melanie-weah': {
      ES: { people: ['Timothy', 'Melanie'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Revisa las medidas documentadas del plan antes de avanzar.', pact: 'Acordar el siguiente paso con el asesor.', events: [] },
      EN: { people: ['Timothy', 'Melanie'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Review the plan’s documented moves before advancing.', pact: 'Agree the next step with the advisor.', events: [] }
    },
    'daniel-emily-johnson': {
      ES: { people: ['Daniel', 'Emily'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Revisa las medidas documentadas del plan antes de avanzar.', pact: 'Acordar el siguiente paso con el asesor.', events: [] },
      EN: { people: ['Daniel', 'Emily'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Review the plan’s documented moves before advancing.', pact: 'Agree the next step with the advisor.', events: [] }
    }
  };

  const moveTitles = {
    'Add umbrella cover': 'Añadir cobertura paraguas',
    'Lower the withdrawal rate': 'Reducir la tasa de retiro',
    'Raise growth allocation toward glide': 'Ajustar el crecimiento a la senda objetivo',
    'Close a coverage gap': 'Cerrar una brecha de cobertura',
    'Reduce single-name concentration': 'Reducir la concentración en una posición',
    'Reduce growth allocation toward glide': 'Ajustar el crecimiento a la senda objetivo',
    'Pay down revolving card': 'Reducir la tarjeta revolvente',
    'Add life cover': 'Añadir cobertura de vida',
    'Raise mortality coverage': 'Aumentar la cobertura por fallecimiento',
    'Raise annual savings': 'Aumentar el ahorro anual'
  };

  const buckets = {
    'Build minimum emergency threshold (3 months)': 'Construir el mínimo de emergencia (3 meses)',
    'Address essential insurance gaps': 'Cubrir brechas esenciales de seguro',
    'Set aside cash for near-term goals': 'Separar efectivo para metas cercanas',
    'Maximize employer match — primary plan': 'Maximizar aporte empresarial — plan principal',
    'Maximize employer match — secondary plan': 'Maximizar aporte empresarial — plan secundario',
    'Maximize HSA match': 'Maximizar aporte equivalente de HSA',
    'Maximize ESPP (Employee Stock Purchase Plan)': 'Maximizar ESPP (plan de compra de acciones para empleados)',
    'Pay high-interest debt (>7%)': 'Pagar deuda de alto interés (>7%)',
    'Build toward maximum emergency threshold (6 months)': 'Avanzar hacia el máximo de emergencia (6 meses)',
    'Contribute to Roth IRA': 'Aportar a IRA Roth',
    'Maximize HSA': 'Maximizar HSA',
    'Contribute to 529 accounts': 'Aportar a cuentas 529',
    'Maximize 401k / employer plans': 'Maximizar 401(k) / planes empresariales',
    'Invest in taxable brokerage': 'Invertir en cuenta de corretaje imponible',
    'Pay low-interest debt (personal, auto)': 'Pagar deuda de bajo interés (personal, automóvil)',
    'Make extra mortgage payments': 'Realizar pagos hipotecarios adicionales'
  };

  const shockNames = [
    'Última subida de la Fed a 5.25–5.50%',
    'Giro de la Fed — gráfico de puntos de diciembre de 2023',
    'Venta global — VIX supera 60',
    'Primer recorte de la Fed — 50 pb',
    'Victoria electoral de Trump',
    'Choque de IA DeepSeek',
    'Anuncio de aranceles del Día de la Liberación',
    'Rally por pausa arancelaria de 90 días',
    'Tregua arancelaria EE. UU.-China en Ginebra',
    'El Tribunal Supremo anula los aranceles del Día de la Liberación',
    'Operación Furia Épica — ataques de EE. UU. e Israel contra Irán'
  ];

  const figures = value => {
    const found = String(value == null ? '' : value).match(/\$[\d,.]+(?:[BMKT])?|\b\d+(?:\.\d+)?%|\b\d+(?:,\d{3})*(?:\.\d+)?\b/g) || [];
    return [...new Set(found)].join(', ');
  };

  const spanishDetail = (id, type, value) => {
    const n = figures(value);
    const base = type === 'concern'
      ? 'Preocupación prioritaria del plan.'
      : type === 'tension'
        ? 'Tensión que requiere una decisión conjunta.'
        : type === 'transition'
          ? 'Hito y transición del plan.'
          : type === 'persona'
            ? 'Lectura provisional del plan.'
            : 'Resumen del plan.';
    return `${base}${n ? ` Cifras declaradas: ${n}.` : ''}`;
  };

  const severityES = value => {
    const found = String(value || '').match(/CRITICAL|SIGNIFICANT|MODERATE|MINOR|HIGH|MEDIUM|LOW/);
    return found ? ({ CRITICAL: 'CRÍTICO', SIGNIFICANT: 'SIGNIFICATIVO', MODERATE: 'MODERADO', MINOR: 'MENOR', HIGH: 'ALTA', MEDIUM: 'MEDIA', LOW: 'BAJA' }[found[0]] || '') : '';
  };

  function localizeData(data, lang) {
    if (!data || lang !== 'ES') return data;
    const score = data.score || {}, persona = data.persona || {};
    const action = (value, index) => `Acción prioritaria ${index + 1}.${figures(value) ? ` Cifras del paso: ${figures(value)}.` : ''}`;
    return Object.assign({}, data, {
      score: Object.assign({}, score, {
        pillars: (score.pillars || []).map(p => Object.assign({}, p, {
          pillar: { 'Savings and cash flow': 'Ahorro y flujo de caja', Debt: 'Deuda', Investments: 'Inversiones', 'Liquidity and emergency fund': 'Liquidez y fondo de emergencia', 'Insurance and protection': 'Seguros y protección' }[p.pillar] || p.pillar
        })),
        top_moves: (score.top_moves || []).map((m, i) => Object.assign({}, m, {
          title: moveTitles[m.title] || `Medida prioritaria ${i + 1}`,
          action: action(m.action, i),
          note: spanishDetail('', 'move', m.note)
        })),
        combined_moves: (score.combined_moves || []).map((m, i) => Object.assign({}, m, {
          title: `Medidas combinadas ${i + 1}`,
          action: action(m.action, i),
          moves: (m.moves || []).map((x, j) => moveTitles[x] || `Medida ${j + 1}`),
          note: spanishDetail('', 'move', m.note)
        })),
        message: spanishDetail('', 'score', score.message),
        explainer: spanishDetail('', 'score', score.explainer)
      }),
      persona: Object.assign({}, persona, {
        D6: spanishDetail('', 'persona', persona.D6),
        D3: spanishDetail('', 'persona', persona.D3),
        subjectiveConcerns: spanishDetail('', 'persona', persona.subjectiveConcerns),
        transitionAlerts: spanishDetail('', 'transition', persona.transitionAlerts),
        objectiveConcerns: (persona.objectiveConcerns || []).map(x => Object.assign({}, x, {
          detail: `- **${x.id}${severityES(x.detail) ? ' ' + severityES(x.detail) : ''}:** ${spanishDetail('', 'concern', x.detail)}`
        })),
        tensions: (persona.tensions || []).map(x => Object.assign({}, x, {
          detail: `- **${x.id}${severityES(x.detail) ? ' (' + severityES(x.detail) + ')' : ''}:** ${spanishDetail('', 'tension', x.detail)}`
        }))
      }),
      savingsWaterfall: (data.savingsWaterfall || []).map(x => Object.assign({}, x, {
        bucket: buckets[x.bucket] || x.bucket,
        status: { Filled: 'Cubierto', 'Partially filled': 'Parcialmente cubierto', Empty: 'Pendiente' }[x.status] || x.status
      })),
      shocks: (data.shocks || []).map((x, i) => Object.assign({}, x, {
        name: shockNames[i] || 'Evento histórico',
        portfolioImpact: { Mixed: 'Mixto', Negative: 'Negativo', Positive: 'Positivo', 'Rates-driven': 'Tipos de interés' }[x.portfolioImpact] || x.portfolioImpact,
        description: `Contexto del evento histórico.${figures(x.description) ? ` Cifras declaradas: ${figures(x.description)}.` : ''}`
      }))
    });
  }

  const detail = (id, value, lang) => {
    const html = clean(lang === 'ES'
      ? String(value).replace(/CRITICAL/g, 'CRÍTICO').replace(/SIGNIFICANT/g, 'SIGNIFICATIVO').replace(/MODERATE/g, 'MODERADO').replace(/MINOR/g, 'MENOR').replace(/HIGH/g, 'ALTA').replace(/MEDIUM/g, 'MEDIA').replace(/LOW/g, 'BAJA')
      : value);
    return html.match(new RegExp('^<strong>' + id)) ? html : `<strong>${esc(id)}</strong> ${html}`;
  };

  function exactMoney(value) {
    if (value == null) return '—';
    const n = Number(value);
    if (!Number.isFinite(n)) return '—';
    return (n < 0 ? '-$' : '$') + Math.abs(n).toLocaleString('en-US', { maximumFractionDigits: 2 });
  }

  function riskRecord(caseId, lang) {
    const rows = (((dataFor(caseId) || {}).projections || {}).yearly || []);
    const index = rows.findIndex(row => Number(row.investable_assets) < 0);
    const es = lang !== 'EN';
    if (index < 0) {
      const label = es ? 'Sin registro anual de activos invertibles negativos.' : 'No yearly negative-investable-assets record.';
      return { caseId, hasExhaustion: false, label, toString() { return label; } };
    }
    const row = rows[index];
    const age = row.age_client != null ? row.age_client : row.age_co_client;
    const parts = [String(row.year)];
    if (age != null) parts.push(es ? `edad ${age}` : `age ${age}`);
    parts.push(es ? `activos invertibles ${exactMoney(row.investable_assets)}` : `investable assets ${exactMoney(row.investable_assets)}`);
    if (row.net_worth != null) parts.push(es ? `patrimonio neto ${exactMoney(row.net_worth)}` : `net worth ${exactMoney(row.net_worth)}`);
    if (row.total_debts != null) parts.push(es ? `deuda total ${exactMoney(row.total_debts)}` : `total debt ${exactMoney(row.total_debts)}`);
    const label = parts.join(' · ');
    return {
      caseId, hasExhaustion: true, index, length: rows.length, row, year: row.year, age,
      investable_assets: row.investable_assets, net_worth: row.net_worth, total_debts: row.total_debts,
      label, toString() { return label; }
    };
  }

  const failTags = new Proxy({}, { get: (_, caseId) => new Proxy({}, { get: (_u, lang) => riskRecord(caseId, lang) }) });

  function riskCoordinates(record, stagePoint) {
    const [sx, sy] = stagePoint || biomes[0].point;
    if (!record || !record.hasExhaustion) {
      return { sx, sy, x: Math.min(1140, sx + 32), y: Math.min(685, sy + 10), wall: true };
    }
    const share = record.length > 1 ? record.index / (record.length - 1) : 0;
    const rx = Math.round(190 + (830 - 190) * share);
    const ry = Math.round(610 - (610 - 130) * share);
    const bx = Math.min(1120, Math.max(sx + 38, rx));
    const by = Math.min(690, Math.max(sy + 48, ry + 78));
    return { sx, sy, x: bx, y: by, wall: false };
  }

  function blockedCopy(id, mode, persona, state) {
    const lang = langOf(state), record = riskRecord(id, lang);
    if (!record.hasExhaustion) {
      return lang === 'ES'
        ? 'No existe un registro anual de activos invertibles negativos para fijar una edad o saldo de caída.'
        : 'There is no yearly negative-investable-assets record from which to set a failure age or balance.';
    }
    const row = record.row, es = lang === 'ES', details = [`${es ? 'Año' : 'Year'} ${row.year}`];
    if (record.age != null) details.push(`${es ? 'edad' : 'age'} ${record.age}`);
    details.push(`${es ? 'activos invertibles' : 'investable assets'} ${exactMoney(row.investable_assets)}`);
    if (row.net_worth != null) details.push(`${es ? 'patrimonio neto' : 'net worth'} ${exactMoney(row.net_worth)}`);
    if (row.total_debts != null) details.push(`${es ? 'deuda total' : 'total debt'} ${exactMoney(row.total_debts)}`);
    return details.join(' · ');
  }

  function mathSummary(data, state) {
    const score = data.score || {};
    const rows = (data.projections || {}).yearly || [];
    const moves = [...(score.top_moves || []), ...(score.combined_moves || [])];
    const last = rows[rows.length - 1] || {};
    const es = langOf(state) === 'ES';
    const moveText = moves.slice(0, 5).map(m => {
      const label = m.title || (m.moves || []).join(' + ') || (es ? 'Medida' : 'Move');
      const before = m.score_before != null ? m.score_before : score.published_score;
      const after = m.score_after != null ? m.score_after : score.published_score;
      const delta = before != null && after != null ? ` (${esc(before)} → ${esc(after)})` : '';
      return `${esc(label)}${delta}`;
    }).join('; ') || t(state, 'none');
    return `<details open><summary>${t(state, 'exact')}</summary><ul><li><strong>${t(state, 'levers')}:</strong> ${moveText}.</li><li><strong>${t(state, 'facts')}:</strong> ${es ? 'registros factuales cargados' : 'loaded factual records'}.</li><li><strong>${t(state, 'yearly')}:</strong> ${rows.length} ${es ? 'años; último' : 'years; last'} ${esc(last.year || '—')}, ${es ? 'activos invertibles' : 'investable assets'} ${esc(last.investable_assets == null ? '—' : exactMoney(last.investable_assets))}, ${es ? 'patrimonio neto' : 'net worth'} ${esc(last.net_worth == null ? '—' : exactMoney(last.net_worth))}.</li></ul><p>${t(state, 'sources')}: ${es ? 'datos de medidas, proyecciones y hechos cargados.' : 'score.top_moves, score.combined_moves, projections.yearly.'}</p></details>`;
  }

  function stepGoodOption(state, data, s, stageIdx) {
    const moves = (data.score && data.score.top_moves) || [];
    if (stageIdx < moves.length && moves[stageIdx]) {
      const m = moves[stageIdx];
      return {
        label: m.action || m.title || s.pact,
        trend: `${t(state, 'trend')}: ${m.action || m.title} (${langOf(state) === 'ES' ? 'puntaje' : 'score'} ${m.score_before} → ${m.score_after}).`
      };
    }
    const combined = (data.score && data.score.combined_moves) || [];
    if (combined.length) {
      const best = combined.reduce((a, b) => ((b.moves || []).length >= (a.moves || []).length ? b : a), combined[0]);
      const baseScore = data.score && data.score.published_score;
      const comboLabel = (best.moves || []).join(' + ') || best.title || s.pact;
      const before = best.score_before != null ? best.score_before : baseScore;
      return {
        label: `${comboLabel}${best.score_after != null ? ` (${before} → ${best.score_after})` : ''}`,
        trend: `${t(state, 'trend')}: ${comboLabel} (${langOf(state) === 'ES' ? 'puntaje' : 'score'} ${before} → ${best.score_after}).`
      };
    }
    return { label: s.pact, trend: `${t(state, 'trend')}: ${s.pact}` };
  }

  function preview(state, data, route) {
    if (route !== 'bad') return stepGoodOption(state, data, specs[state.caseId][langOf(state)], Number(state.stage) || 0).trend;
    const rec = riskRecord(state.caseId, langOf(state));
    return rec.hasExhaustion
      ? `${t(state, 'trend')}: ${rec.label}`
      : (langOf(state) === 'ES' ? 'No hay un punto anual de agotamiento registrado para esta ruta.' : 'No yearly exhaustion point is recorded for this route.');
  }

  function strictCasePayload(caseId, lang, node) {
    const source = dataFor(caseId) || {};
    const stage = Math.max(0, Math.min(Number(node) || 0, 3));
    return {
      strict_zero_inference: true, case_id: caseId, language: lang, stage, case_data: source,
      node_data: {
        top_move: ((source.score || {}).top_moves || [])[stage] || null,
        combined_moves: ((source.score || {}).combined_moves || []),
        yearly: ((source.projections || {}).yearly || [])
      }
    };
  }

  function createInitialState(id) {
    const lang = loadLang();
    return {
      caseId: ids.includes(id) ? id : ids[0],
      view: viewName('expedition', lang),
      phase: 'fears',
      mode: 'Plain',
      lang,
      fearOrder: [],
      subjectiveConcern: '',
      votes: {},
      voteTurn: 'A',
      timerStartedAt: null,
      stage: 0,
      focusedNode: 0,
      cameraMode: 'camp',
      dialogVisible: true,
      blocked: false,
      history: [],
      advisorDoubts: [],
      summit: false
    };
  }

  const isMountainPhase = state => !!state && viewKey(state.view) === 'expedition' && !state.summit && (state.phase === 'expedition' || state.phase === 'blocked');

  // Extreme 8x camera (150 x 93.75 inside 1200 x 750) keeping the micro-camp above the floating bottom-right dialog
  function campCamera(stage) {
    const idx = Math.max(0, Math.min(3, Number(stage) || 0));
    const pt = biomes[idx].point;
    const w = 150, h = 93.75;
    const cx = idx === 3 ? pt[0] + 18 : pt[0];
    const cy = idx === 3 ? pt[1] - 16 : pt[1];
    const x = Math.max(0, Math.min(fullCamera[2] - w, cx - w * 0.36));
    const y = Math.max(0, Math.min(fullCamera[3] - h, cy - h * 0.38));
    return [x, y, w, h];
  }

  function riskCameraBox(record, stagePoint) {
    const coord = riskCoordinates(record, stagePoint);
    const w = 160, h = 100;
    const x = Math.max(0, Math.min(fullCamera[2] - w, coord.x - w * 0.42));
    const y = Math.max(0, Math.min(fullCamera[3] - h, coord.y - h * 0.42));
    return [x, y, w, h];
  }

  function normalizePointAndOffset(offset, point) {
    const legacy = [[120, 465], [185, 375], [295, 245], [380, 108]];
    if (point) {
      const idx = legacy.findIndex(p => Math.abs(p[0] - point[0]) <= 6 && Math.abs(p[1] - point[1]) <= 6);
      if (idx >= 0) return { point: biomes[idx].point, offset: biomes[idx].offset, stage: idx };
      const bIdx = biomes.findIndex(b => Math.abs(b.point[0] - point[0]) <= 2 && Math.abs(b.point[1] - point[1]) <= 2);
      if (bIdx >= 0) return { point: biomes[bIdx].point, offset: offset == null ? biomes[bIdx].offset : offset, stage: bIdx };
    }
    const offMap = { 480: 0, 340: 1, 165: 2, 0: 3 };
    if (offset in offMap && !point) {
      const i = offMap[offset];
      return { point: biomes[i].point, offset: biomes[i].offset, stage: i };
    }
    return { point: point || biomes[0].point, offset: offset == null ? TRAIL_LENGTH : Number(offset), stage: 0 };
  }

  function svgMarkup(offset, point, history, blocked, couple, votes, failTag, lang, opts) {
    const norm = normalizePointAndOffset(offset, point);
    const [x, y] = norm.point;
    const activeStage = opts && opts.stage != null ? Number(opts.stage) : norm.stage;
    const activeOffset = Math.max(0, Math.min(TRAIL_LENGTH, Number(norm.offset) || 0));
    const record = failTag && typeof failTag === 'object' ? failTag : null;
    const showRisk = !!(blocked || (history && history.length && record && record.hasExhaustion));
    const diverged = !!((history && history.length) || (votes && votes.A && votes.B && votes.A.priority && votes.B.priority && votes.A.priority !== votes.B.priority));
    const initialBox = (opts && opts.initialViewBox) ? opts.initialViewBox.map(n => Math.round(n * 100) / 100).join(' ') : fullCamera.join(' ');
    const shortLabels = campShorts[lang === 'EN' ? 'EN' : 'ES'];

    let riskMarkup = '';
    if (showRisk) {
      const originIdx = blocked ? activeStage : Math.max(0, Math.min(3, Number((history[history.length - 1] || {}).stage) || 0));
      const originPt = biomes[originIdx].point;
      const coord = riskCoordinates(record, originPt);
      if (record && record.hasExhaustion) {
        const d = `M ${coord.sx} ${coord.sy} Q ${coord.sx + 22} ${coord.sy + 26} ${coord.x} ${coord.y}`;
        riskMarkup = `<g class="risk-group"><path class="risk-path" data-risk-break="${coord.x},${coord.y}" data-exhaustion="true" data-year="${record.year}" data-age="${record.age == null ? '' : record.age}" data-investable-assets="${record.investable_assets}" d="${d}" stroke-width="2.4"/><circle cx="${coord.x}" cy="${coord.y}" r="2.2" fill="#C83A2B"/><path d="M ${coord.x - 3} ${coord.y - 3} L ${coord.x + 3} ${coord.y + 3} M ${coord.x + 3} ${coord.y - 3} L ${coord.x - 3} ${coord.y + 3}" stroke="#C83A2B" stroke-width="0.65"/><text x="${coord.x + 4.5}" y="${coord.y - 3}" fill="#C83A2B" font-size="3.6" font-weight="600" font-family="system-ui">${esc(record.label)}</text></g>`;
      } else if (blocked) {
        const d = `M ${coord.sx} ${coord.sy} L ${coord.x} ${coord.y}`;
        const wall = `M ${coord.x} ${coord.y - 10} L ${coord.x} ${coord.y + 10}`;
        riskMarkup = `<g class="risk-group"><path class="risk-path" data-risk-break="${coord.x},${coord.y}" data-exhaustion="false" d="${d}" stroke-width="2.4"/><path d="${wall}" stroke="#C83A2B" stroke-width="1.2" stroke-linecap="round"/><text x="${coord.x + 3.5}" y="${coord.y - 3.5}" fill="#C83A2B" font-size="3.4" font-weight="600" font-family="system-ui">${esc(record ? record.label : t({ lang }, 'risk'))}</text></g>`;
      }
    }

    const partners = couple
      ? `<path class="partner-rope" d="${TRAIL_PATH}" transform="translate(-1.8 -1.2)" stroke="var(--partner-a)" stroke-width="1.4" opacity=".82"/><path class="partner-rope" d="${TRAIL_PATH}" transform="translate(1.8 1.2)" stroke="var(--partner-b)" stroke-width="1.4" opacity=".82"/>${diverged ? '<path class="partner-rope" d="M 390 465 Q 455 442 505 426 T 620 295" stroke="#C83A2B" stroke-dasharray="3 3" stroke-width="1.2" opacity=".7"/>' : ''}`
      : '';

    const campNodes = [
      // Camp 0: Basecamp · pines + A-frame tent + stone cairn
      `<g class="micro-camp ${activeStage === 0 ? 'is-active' : ''} ${activeStage > 0 ? 'is-reached' : ''}" data-action="focus-node" data-node="0" transform="translate(190 610)">
        <circle class="camp-hit" cx="0" cy="0" r="18" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="8.5"/>
        <path d="M -11 2 L -9.2 -4.5 L -7.4 2 Z M -8 2.2 L -6.5 -2.6 L -5 2.2 Z" fill="#141311" opacity=".78"/>
        <path class="camp-tent" d="M -3.5 2 L 0 -4.2 L 3.5 2 Z" fill="#FBF9F5" stroke="#141311" stroke-width="0.55" stroke-linejoin="round"/>
        <path d="M 0 -4.2 L 0 2 M 5.2 2 A 1.2 1.2 0 1 0 7.6 2 Z" fill="none" stroke="#141311" stroke-width="0.45"/>
        <text x="0" y="7.5" text-anchor="middle" font-size="3.2" font-family="system-ui" font-weight="600" fill="#141311" opacity=".8">${esc(shortLabels[0])} · 2,800m</text>
      </g>`,
      // Camp 1: Rock bivy · ledge + twin tents + piton marker
      `<g class="micro-camp ${activeStage === 1 ? 'is-active' : ''} ${activeStage > 1 ? 'is-reached' : ''}" data-action="focus-node" data-node="1" transform="translate(390 465)">
        <circle class="camp-hit" cx="0" cy="0" r="18" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="8.5"/>
        <path d="M -7.5 2.4 L 7.5 2.4" stroke="#141311" stroke-width="0.6" stroke-linecap="round"/>
        <path class="camp-tent" d="M -5.2 2.2 L -2.6 -2.8 L 0 2.2 Z M 0.8 2.2 L 3.2 -2.2 L 5.6 2.2 Z" fill="#FBF9F5" stroke="#141311" stroke-width="0.5" stroke-linejoin="round"/>
        <path d="M -6.2 2.2 V -4.5 L -4.2 -3.6 L -6.2 -2.7" fill="#4565d6" stroke="#141311" stroke-width="0.35"/>
        <text x="0" y="7.5" text-anchor="middle" font-size="3.2" font-family="system-ui" font-weight="600" fill="#141311" opacity=".8">${esc(shortLabels[1])} · 4,600m</text>
      </g>`,
      // Camp 2: High glacier · dome tent + ice axe
      `<g class="micro-camp ${activeStage === 2 ? 'is-active' : ''} ${activeStage > 2 ? 'is-reached' : ''}" data-action="focus-node" data-node="2" transform="translate(620 295)">
        <circle class="camp-hit" cx="0" cy="0" r="18" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="8.5"/>
        <path class="camp-tent" d="M -4.2 2 Q 0 -4.8 4.2 2 Z" fill="#FBF9F5" stroke="#141311" stroke-width="0.55"/>
        <path d="M 6.2 2 V -4.5 M 4.4 -3.6 L 8 -2.8" stroke="#141311" stroke-width="0.5" stroke-linecap="round"/>
        <text x="0" y="7.5" text-anchor="middle" font-size="3.2" font-family="system-ui" font-weight="600" fill="#141311" opacity=".8">${esc(shortLabels[2])} · 6,900m</text>
      </g>`,
      // Camp 3: Summit · cairn + Sherpas Flag
      `<g class="micro-camp ${activeStage === 3 ? 'is-active' : ''}" data-action="focus-node" data-node="3" transform="translate(830 130)">
        <circle class="camp-hit" cx="8" cy="-12" r="24" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="8.5"/>
        <g class="sherpas-flag" aria-label="Sherpas">
          <path d="M 0 1 V -42" fill="none" stroke="#141311" stroke-width="1.3" stroke-linecap="round"/>
          <path d="M 0.5 -41 L 46 -30 L 0.5 -17 Z" fill="#141311"/>
          <path d="M 8 -29 L 15 -34.5 L 22 -29 L 15 -24 Z" fill="#FBF9F5"/>
          <text x="5.5" y="-20.5" fill="#FBF9F5" font-size="4.8" font-family="system-ui" font-weight="700" letter-spacing=".6">SHERPAS</text>
        </g>
        <text x="0" y="7.5" text-anchor="middle" font-size="3.2" font-family="system-ui" font-weight="700" fill="#141311" opacity=".88">${esc(shortLabels[3])} · 8,848m</text>
      </g>`
    ].join('');

    const climber = couple
      ? `<g id="climberMarker" class="climber-rig" transform="translate(${x} ${y})" data-cx="${x}" data-cy="${y}">
          <circle cx="0" cy="0" r="0.1" fill="none"/>
          <path d="M -3.4 0 Q 0 1.4 3.4 0" fill="none" stroke="#141311" stroke-width="0.45"/>
          <circle cx="-3.4" cy="-3.8" r="1.25" fill="var(--partner-a)" stroke="#FBF9F5" stroke-width="0.4"/>
          <path d="M -3.4 -2.5 V 0.2" stroke="var(--partner-a)" stroke-width="0.9" stroke-linecap="round"/>
          <circle cx="3.4" cy="-3.8" r="1.25" fill="var(--partner-b)" stroke="#FBF9F5" stroke-width="0.4"/>
          <path d="M 3.4 -2.5 V 0.2" stroke="var(--partner-b)" stroke-width="0.9" stroke-linecap="round"/>
        </g>`
      : `<g id="climberMarker" class="climber-rig" transform="translate(${x} ${y})" data-cx="${x}" data-cy="${y}">
          <circle cx="0" cy="0" r="5.5" fill="none" stroke="#4565d6" stroke-width="0.45" opacity=".5"/>
          <circle cx="0" cy="-4.2" r="1.45" fill="#141311" stroke="#FBF9F5" stroke-width="0.45"/>
          <path d="M 0 -2.6 V 0.6 M -1.8 -0.8 L 2.2 -1.8 M 2.4 -3.2 L 2.4 1.2" stroke="#141311" stroke-width="0.85" stroke-linecap="round"/>
        </g>`;

    return `<svg class="mountain-svg" data-camera="mountain" viewBox="${initialBox}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="${lang === 'EN' ? 'Sumi-e mountain route with Sherpas summit flag' : 'Ruta de montaña sumi-e con bandera Sherpas en la cima'}">
      <defs>
        <filter id="sumi-brush" x="-8%" y="-10%" width="116%" height="120%">
          <feTurbulence type="fractalNoise" baseFrequency=".014 .18" numOctaves="2" seed="8" result="grain"/>
          <feDisplacementMap in="SourceGraphic" in2="grain" scale="1.65" xChannelSelector="R" yChannelSelector="G"/>
        </filter>
        <linearGradient id="wash-far" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#141311" stop-opacity=".13"/>
          <stop offset="72%" stop-color="#141311" stop-opacity=".04"/>
          <stop offset="100%" stop-color="#FBF9F5" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="wash-mid" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#141311" stop-opacity=".22"/>
          <stop offset="80%" stop-color="#141311" stop-opacity=".06"/>
          <stop offset="100%" stop-color="#FBF9F5" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="wash-main" x1=".2" y1="0" x2=".8" y2="1">
          <stop offset="0%" stop-color="#141311" stop-opacity=".18"/>
          <stop offset="55%" stop-color="#2c2a27" stop-opacity=".09"/>
          <stop offset="100%" stop-color="#FBF9F5" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <g id="cameraRig">
        <path id="layerBack" d="M -60 660 L 120 470 250 530 430 315 560 390 735 190 925 320 1070 245 1260 590 V 760 H -60 Z" fill="url(#wash-far)"/>
        <path id="layerMid" d="M -40 700 L 95 540 210 580 375 385 495 445 685 215 845 330 980 260 1240 665 V 760 H -40 Z" fill="url(#wash-mid)"/>
        <path id="mistRibbon" d="M 0 545 Q 280 515 560 555 T 1200 520 L 1200 605 Q 860 630 560 595 T 0 615 Z" fill="#FBF9F5" opacity=".55"/>
        <path id="layerMain" d="M 35 705 L 115 645 L 190 610 L 265 558 L 335 512 L 390 465 L 468 398 L 540 355 L 620 295 L 705 225 L 765 190 L 830 130 L 885 220 L 955 345 L 1035 470 L 1165 705 Z" fill="url(#wash-main)"/>
        <path d="M 745 205 L 830 130 L 902 248 L 856 226 L 826 248 L 792 214 Z" fill="#FFFFFF" opacity=".82"/>
        <path class="sumi-spine" d="M 35 705 L 115 645 L 190 610 L 265 558 L 335 512 L 390 465 L 468 398 L 540 355 L 620 295 L 705 225 L 765 190 L 830 130 L 885 220 L 955 345 L 1035 470 L 1165 705" fill="none" stroke-width="5.5"/>
        <path class="rock-edge" d="M 190 610 L 235 660 M 265 558 L 302 612 M 390 465 L 430 532 L 468 398 M 540 355 L 585 438 L 620 295 M 705 225 L 748 315 M 830 130 L 814 278 L 885 220 M 955 345 L 912 435" fill="none" stroke-width="1.6"/>
        <path class="contour-ink" d="M 90 665 Q 360 585 640 445 T 1090 545 M 160 645 Q 430 520 695 360 T 1015 445 M 290 550 Q 520 420 755 255 T 935 335" stroke-width="1"/>
        <path class="route-guide" d="${TRAIL_PATH}" stroke-width="1.5"/>
        <path id="activeTrail" class="route-ink" d="${TRAIL_PATH}" stroke-width="3.2" stroke-dasharray="${TRAIL_LENGTH}" stroke-dashoffset="${activeOffset}"/>
        ${partners}
        ${riskMarkup}
        ${campNodes}
        ${climber}
      </g>
    </svg>`;
  }

  function yearlyMarkup(data, lang) {
    const rows = (data.projections || {}).yearly || [];
    if (!rows.length) return '';
    const sample = rows.filter((_, i) => i % Math.max(1, Math.floor(rows.length / 24)) === 0).slice(0, 24);
    const values = sample.flatMap(r => [Number(r.investable_assets) || 0, Number(r.net_worth) || 0]);
    const min = Math.min(0, ...values), max = Math.max(1, ...values), span = max - min || 1;
    const y = v => 172 - ((v - min) / span) * 140;
    const line = k => sample.map((r, i) => `${i ? 'L' : 'M'} ${20 + i * (560 / Math.max(1, sample.length - 1))} ${y(Number(r[k]) || 0)}`).join(' ');
    const es = lang !== 'EN';
    return `<div class="preview"><p>${es ? 'Proyección anual: activos invertibles y patrimonio neto' : 'Yearly projection: investable assets and net worth'}</p><svg class="yearly-chart" viewBox="0 0 600 200" role="img" aria-label="${es ? 'Comparación anual entre activos invertibles y patrimonio neto' : 'Yearly comparison of investable assets and net worth'}"><path d="M20 ${y(0)} H580" fill="none" stroke="#94a3b8" stroke-dasharray="4 4"/><text x="24" y="${y(0) - 5}" fill="#64748b" font-size="12">$0</text><path d="${line('investable_assets')}" fill="none" stroke="#4565d6" stroke-width="3"/><path d="${line('net_worth')}" fill="none" stroke="#0d9488" stroke-width="3"/></svg><p>${es ? 'Azul: activos invertibles · Verde: patrimonio neto' : 'Blue: investable assets · Green: net worth'} · ${esc(sample[0].year)}–${esc(sample[sample.length - 1].year)}</p></div>`;
  }

  function render(state) {
    state = state || createInitialState();
    const lang = langOf(state);
    const raw = dataFor(state.caseId) || {};
    const data = localizeData(raw, lang);
    const score = data.score || {};
    const persona = data.persona || {};
    const s = specs[state.caseId][lang];
    const couple = !!(data.meta && data.meta.isCouple);
    const stageIdx = Math.max(0, Math.min(3, Number(state.stage) || 0));
    const focusedIdx = state.focusedNode != null ? Math.max(0, Math.min(3, Number(state.focusedNode) || 0)) : stageIdx;
    const stage = biome(stageIdx, lang);
    const view = viewKey(state.view);
    const isMath = state.mode === 'Math';
    const mountainMode = isMountainPhase(state);
    const dialogVisible = state.dialogVisible !== false;
    const fail = failTags[state.caseId][lang];
    const shortLabels = campShorts[lang];

    const pillars = (score.pillars || []).map(p => `<div class="pillar"><span>${esc(p.pillar)}</span><span>${esc(p.points_shown_in_app)}</span><progress max="100" value="${Math.max(0, Math.min(100, Number(p.score) || 0))}"></progress></div>`).join('');
    const options = ids.map(id => `<option value="${id}" ${id === state.caseId ? 'selected' : ''}>${esc((dataFor(id).meta || {}).household || id)}</option>`).join('');

    let body = '';
    if (view === 'brief') {
      body = `<section class="workspace-section"><h1>${t(state, 'brief')}</h1><div class="advisor-brief"><h2>${t(state, 'concerns')}</h2><p>${esc(state.subjectiveConcern || persona.subjectiveConcerns || t(state, 'noAnswer'))}</p><p>${(state.fearOrder || []).map(esc).join(' · ')}</p></div><div class="advisor-brief"><h2>${t(state, 'couple')}</h2><p>${esc(s.pact)}</p></div><div class="advisor-brief"><h2>${t(state, 'questions')}</h2>${(state.advisorDoubts || []).map(x => `<p>${esc(x)}</p>`).join('') || `<p>${t(state, 'noQuestions')}</p>`}</div><div class="advisor-brief"><h2>${t(state, 'discarded')}</h2>${(state.history || []).map(x => `<p>${esc(x.detailKey === 'D3' ? persona.D3 : x.detail)}</p>`).join('') || `<p>${t(state, 'noDiscarded')}</p>`}</div></section>`;
    } else if (view === 'overview' || view === 'current' || state.summit) {
      const b = state.summit ? biome(3, lang) : stage;
      const hasHistory = (state.history || []).length > 0;
      body = `<section class="workspace-section"><h1>${view === 'overview' ? t(state, 'overview') : view === 'current' ? t(state, 'current') : t(state, 'complete')}</h1><p class="body-copy">${esc(s.pact)}</p><div class="mountain-stage post-mountain" data-biome="${b.id}"><span class="biome-pill">${b.label}</span>${svgMarkup(state.summit ? 0 : b.offset, state.summit ? biomes[3].point : b.point, state.history || [], hasHistory, couple, state.votes, fail, lang, { stage: state.summit ? 3 : stageIdx })}</div><div class="button-row"><button data-action="nav" data-view="${viewName('expedition', lang)}">${t(state, 'continueExpedition')}</button><button data-action="repeat">${t(state, 'repeat')}</button></div>${view === 'current' ? `<p>${t(state, 'next')}</p>` : ''}</section>`;
    } else if (state.phase === 'fears') {
      body = `<section class="workspace-section"><p class="eyebrow">${t(state, 'fears')}</p><h1>${t(state, 'fearTitle')}</h1><p class="body-copy">${t(state, 'fearHelp')}</p><div class="choice-list">${(persona.objectiveConcerns || []).map(c => `<label class="choice"><input type="checkbox" data-fear="${esc(c.id)}" ${(state.fearOrder || []).includes(c.id) ? 'checked' : ''}><span>${detail(c.id, c.detail, lang)}</span></label>`).join('')}</div><label for="subjective">${t(state, 'fearAsk')}</label><textarea id="subjective" data-subjective>${esc(state.subjectiveConcern || '')}</textarea><div class="button-row"><button class="primary" data-action="next-fears">${couple ? t(state, 'continue') : t(state, 'enter')}</button></div></section>`;
    } else if (state.phase === 'cordada') {
      body = `<section class="workspace-section"><p class="eyebrow">${t(state, 'team')}</p><h1>${t(state, 'private')} ${esc((state.voters || s.people)[state.voteTurn === 'A' ? 0 : 1])}</h1><p>${t(state, 'clock')}</p><div class="choice-list">${(persona.objectiveConcerns || []).map(c => `<label class="choice"><input type="checkbox" data-vote-fear="${esc(c.id)}"><span>${detail(c.id, c.detail, lang)}</span></label>`).join('')}<label class="choice"><input type="radio" name="priority" value="crecimiento" data-priority><span>${t(state, 'growth')}</span></label><label class="choice"><input type="radio" name="priority" value="deuda-proteccion" data-priority><span>${t(state, 'debt')}</span></label></div><p class="eyebrow">${t(state, 'time')}: ${Math.max(0, 60 - Math.floor((Date.now() - (state.timerStartedAt || Date.now())) / 1000))} s</p><button class="primary" data-action="submit-vote">${state.voteTurn === 'A' ? t(state, 'save') : t(state, 'matches')}</button></section>`;
    } else if (state.phase === 'cross') {
      const a = state.votes.A || {}, b = state.votes.B || {};
      const common = (a.fears || []).filter(id => (b.fears || []).includes(id));
      const shared = common.length ? common.map(id => { const x = (persona.objectiveConcerns || []).find(c => c.id === id); return `<li>${x ? detail(id, x.detail, lang) : esc(id)}</li>`; }).join('') : `<li>${lang === 'ES' ? 'D6: proteger a los hijos.' : 'D6: protect the children.'}</li>`;
      const fr = [...(a.priority && b.priority && a.priority !== b.priority ? [`<p><strong>${t(state, 'different')}:</strong> ${t(state, a.priority === 'crecimiento' ? 'growth' : 'debt')} ${lang === 'ES' ? 'frente a' : 'versus'} ${t(state, b.priority === 'crecimiento' ? 'growth' : 'debt')}.</p>`] : []), ...(persona.tensions || []).slice(0, 2).map(x => `<p>${detail(x.id, x.detail, lang)}</p>`)].join('') || `<p>${t(state, 'common')}</p>`;
      body = `<section class="workspace-section"><p class="eyebrow">${t(state, 'cross')}</p><h1>${t(state, 'agree')}</h1><ul>${shared}</ul><h2>${t(state, 'friction')}</h2>${fr}<p class="reframe">${t(state, 'pact')}: ${esc(s.pact)}</p><button class="primary" data-action="start-expedition">${t(state, 'enter')}</button></section>`;
    } else if (state.phase === 'blocked') {
      const initBox = state.initialViewBox || (dialogVisible ? riskCameraBox(fail, stage.point) : fullCamera);
      const hudCamps = shortLabels.map((lbl, idx) => `<button class="${idx === stageIdx ? 'active' : ''}" data-action="focus-node" data-node="${idx}">${esc(lbl)}</button>`).join('');
      body = `<div class="mountain-stage mountain-fullscreen storm-shake" data-biome="${stage.id}" data-dialog-ready="${dialogVisible ? 'true' : 'false'}">
        <div class="mountain-hud"><span class="biome-pill">${esc(stage.label)}</span><div class="camp-pills">${hudCamps}</div><button class="hud-zoom-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
        ${svgMarkup(stage.offset, stage.point, state.history || [], true, couple, state.votes, fail, lang, { stage: stageIdx, initialViewBox: initBox })}
        <aside class="floating-dialog ${dialogVisible ? '' : 'is-dialog-hidden'}" data-dialog="blocked" ${dialogVisible ? '' : 'hidden'}>
          <div class="floating-dialog-head"><div><p class="eyebrow">${t(state, 'blocked')}</p><h2>${t(state, 'stopped')}</h2></div><button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
          <div class="crack"><strong>${t(state, 'impact')}</strong><div class="blocked-impact">${esc(blockedCopy(state.caseId, state.mode, persona, state))}</div>${isMath ? '' : `<details><summary>${t(state, 'context')}</summary><p>${esc(s.blocked)}</p></details>`}<details><summary>${t(state, 'tensions')}</summary>${(persona.tensions || []).map(x => `<p>${detail(x.id, x.detail, lang)}</p>`).join('')}</details></div>
          <button class="primary" data-action="rewind">${t(state, 'rewind')}</button>
        </aside>
        <div class="floating-overview-cta ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'is-hidden'}" ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'hidden'}><span>${t(state, 'panoramicHint')}</span><button class="primary" data-action="focus-active">${t(state, 'focusActive')}</button></div>
      </div>`;
    } else {
      const inspectingOther = focusedIdx !== stageIdx;
      const focusedBiome = biome(focusedIdx, lang);
      const focusedMove = stepGoodOption(state, data, s, focusedIdx);
      const activeMove = stepGoodOption(state, data, s, stageIdx);
      const initBox = state.initialViewBox || (state.cameraMode === 'panoramic' ? fullCamera : (dialogVisible ? campCamera(focusedIdx) : fullCamera));
      const hudCamps = shortLabels.map((lbl, idx) => `<button class="${idx === focusedIdx ? 'active' : ''}" data-action="focus-node" data-node="${idx}">${esc(lbl)}</button>`).join('');
      const dialogContent = inspectingOther
        ? `<div class="floating-dialog-head"><div><p class="eyebrow">${t(state, 'inspectCamp')} · ${esc(focusedBiome.label)}</p><h2>${esc(shortLabels[focusedIdx])}</h2></div><button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
           <p class="reframe">${esc(focusedMove.label)}</p>
           <p class="preview">${esc(focusedMove.trend)}</p>
           <div class="button-row"><button class="primary" data-action="focus-active">${t(state, 'focusActive')}</button></div>`
        : `<div class="floating-dialog-head"><div><p class="eyebrow">${t(state, 'phase')} · ${esc(stage.label)}</p><h2>${t(state, 'choose')}</h2></div><button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
           <p class="reframe">${esc(s.reframe)}</p>
           <div class="choice-list">
             <label class="choice"><input type="radio" name="route" value="good" checked><span>${esc(activeMove.label)}</span></label>
             <label class="choice"><input type="radio" name="route" value="bad"><span>${stageIdx === 1 && s.events.length ? esc(s.events[0]) : t(state, 'ignore')}</span></label>
           </div>
           <p class="preview" data-preview>${esc(preview(state, data, 'good'))}</p>
           ${isMath ? mathSummary(data, state) : ''}
           <details ${isMath ? 'open' : ''}><summary>${t(state, 'yearlyToggle')}</summary>${yearlyMarkup(data, lang)}</details>
           ${s.events.map(e => `<div class="fear-note"><p>${esc(e)}</p><button data-action="doubt" data-doubt="${esc(e)}">${t(state, 'doubt')}</button></div>`).join('')}
           <div class="button-row"><button class="primary" data-action="advance">${t(state, 'confirm')}</button></div>`;
      body = `<div class="mountain-stage mountain-fullscreen" data-biome="${stage.id}" data-dialog-ready="${dialogVisible ? 'true' : 'false'}">
        <div class="mountain-hud"><span class="biome-pill">${esc(focusedBiome.label)}</span><div class="camp-pills">${hudCamps}</div><button class="hud-zoom-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
        ${svgMarkup(stage.offset, stage.point, state.history || [], false, couple, state.votes, fail, lang, { stage: stageIdx, initialViewBox: initBox })}
        <aside class="floating-dialog ${dialogVisible ? '' : 'is-dialog-hidden'}" data-dialog="decision" ${dialogVisible ? '' : 'hidden'}>${dialogContent}</aside>
        <div class="floating-overview-cta ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'is-hidden'}" ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'hidden'}><span>${t(state, 'panoramicHint')}</span><button class="primary" data-action="focus-active">${t(state, 'focusActive')}</button></div>
      </div>`;
    }

    const nav = ['expedition', 'current', 'overview', 'brief'].map(k => `<button class="${view === k ? 'active' : ''}" data-action="nav" data-view="${viewName(k, lang)}">${viewName(k, lang)}</button>`).join('');
    const rail = mountainMode ? '' : `<aside class="left-rail"><p class="eyebrow">${t(state, 'plan')} · ${esc((data.meta || {}).household || '')}</p><div class="score">${esc(score.published_score || 0)}<span class="eyebrow">/100</span></div><div>${pillars}</div><div class="reframe">${esc(isMath ? score.explainer : score.message)}</div>${isMath ? mathSummary(data, state) : ''}</aside>`;
    return `<header class="site-header ${mountainMode ? 'header-floating' : ''}"><a class="brand" href="#">sherpas</a><select class="case-select" aria-label="${t(state, 'select')}" data-case>${options}</select><nav class="site-nav" aria-label="${t(state, 'nav')}">${nav}</nav><div class="toggle" aria-label="${t(state, 'reading')}"><button data-action="mode" data-mode="Plain" class="${!isMath ? 'active' : ''}">${t(state, 'plain')}</button><button data-action="mode" data-mode="Math" class="${isMath ? 'active' : ''}">${t(state, 'math')}</button></div><div class="language-toggle" aria-label="${lang === 'ES' ? 'Idioma' : 'Language'}"><button data-action="lang" data-lang="ES" class="${lang === 'ES' ? 'active' : ''}">ES</button><button data-action="lang" data-lang="EN" class="${lang === 'EN' ? 'active' : ''}">EN</button></div></header><main class="page-shell ${mountainMode ? 'page-mountain-full' : ''}"><div class="open-flow ${mountainMode ? 'is-mountain-phase' : ''}">${rail}<div>${body}</div></div></main>`;
  }

  function createSherpasAI() {
    if (root.SherpasAI) return root.SherpasAI;
    const mark = mode => { if (root.document) root.document.documentElement.dataset.sherpasAi = mode; };
    const client = {
      mode: 'deterministic',
      last: null,
      request(kind, payload, fallback) {
        const local = fallback == null ? { mode: 'deterministic', kind } : fallback;
        client.mode = 'deterministic';
        client.last = local;
        mark('deterministic');
        return Promise.resolve(local);
      }
    };
    root.SherpasAI = client;
    mark('deterministic');
    return client;
  }
  const SherpasAI = createSherpasAI();

  const parseViewBox = svg => (svg && svg.getAttribute('viewBox') || '0 0 1200 750').trim().split(/[ ,]+/).map(Number);
  const setViewBox = (svg, box) => svg && svg.setAttribute('viewBox', box.map(n => Math.round(n * 100) / 100).join(' '));
  const easeOut = p => 1 - Math.pow(1 - p, 3);
  const easeInOut = p => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
  const prefersReducedMotion = () => !!(root.matchMedia && root.matchMedia('(prefers-reduced-motion: reduce)').matches);
  const hasRaf = () => typeof root.requestAnimationFrame === 'function' && !prefersReducedMotion();

  let activeToken = 0;
  let activeRaf = null;
  const cancelMotion = () => {
    activeToken++;
    if (activeRaf && typeof root.cancelAnimationFrame === 'function') {
      root.cancelAnimationFrame(activeRaf);
      activeRaf = null;
    }
  };

  function animateSteps(duration, token, onFrame, onDone) {
    if (!hasRaf() || duration <= 0) {
      onFrame(1);
      if (onDone) onDone();
      return;
    }
    const raf = root.requestAnimationFrame;
    const start = root.performance && root.performance.now ? root.performance.now() : Date.now();
    const tick = now => {
      if (token !== activeToken) return;
      const p = Math.min(1, (now - start) / duration);
      onFrame(p);
      if (p < 1) activeRaf = raf(tick);
      else {
        activeRaf = null;
        if (onDone) onDone();
      }
    };
    activeRaf = raf(tick);
  }

  function animateViewBox(svg, from, to, duration, done, token) {
    if (!svg) { if (done) done(); return; }
    const tk = token == null ? ++activeToken : token;
    animateSteps(duration, tk, p => {
      const e = easeOut(p);
      setViewBox(svg, from.map((n, i) => n + (to[i] - n) * e));
    }, done);
  }

  function trailPointAt(svg, fraction) {
    const path = svg && svg.querySelector('#activeTrail');
    if (path && typeof path.getTotalLength === 'function' && typeof path.getPointAtLength === 'function') {
      const len = path.getTotalLength();
      const pt = path.getPointAtLength(Math.max(0, Math.min(1, fraction)) * len);
      return [pt.x, pt.y];
    }
    const seg = Math.min(2, Math.floor(fraction * 3));
    const localT = (fraction * 3) - seg;
    const p0 = biomes[seg].point, p2 = biomes[seg + 1].point;
    const ctrl = [[285, 552], [505, 385], [725, 222]][seg];
    const mt = 1 - localT;
    return [mt * mt * p0[0] + 2 * mt * localT * ctrl[0] + localT * localT * p2[0], mt * mt * p0[1] + 2 * mt * localT * ctrl[1] + localT * localT * p2[1]];
  }

  function revealDialog(el, state) {
    state.dialogVisible = true;
    const stageEl = el.querySelector('.mountain-stage');
    if (stageEl) stageEl.dataset.dialogReady = 'true';
    const dlg = el.querySelector('[data-dialog]');
    if (dlg) { dlg.hidden = false; dlg.classList.remove('is-dialog-hidden'); }
    const cta = el.querySelector('.floating-overview-cta');
    if (cta) { cta.hidden = true; cta.classList.add('is-hidden'); }
  }

  function hideDialogs(el, state) {
    state.dialogVisible = false;
    const stageEl = el.querySelector('.mountain-stage');
    if (stageEl) stageEl.dataset.dialogReady = 'false';
    el.querySelectorAll('[data-dialog]').forEach(d => { d.hidden = true; d.classList.add('is-dialog-hidden'); });
  }

  function showOverviewCta(el, state) {
    state.cameraMode = 'panoramic';
    const cta = el.querySelector('.floating-overview-cta');
    if (cta) { cta.hidden = false; cta.classList.remove('is-hidden'); }
  }

  function runCamera(svg, intent, done) {
    if (!svg) { if (done) done(); return; }
    const tk = ++activeToken;
    const type = (intent && intent.type) || 'focus';
    const stage = intent && intent.stage != null ? Number(intent.stage) : 0;
    const target = campCamera(stage);
    const from = parseViewBox(svg);

    if (type === 'overview') {
      animateViewBox(svg, from, fullCamera.slice(), 480, done, tk);
      return;
    }
    if (type === 'risk') {
      const risk = svg.querySelector('.risk-path');
      if (!risk) { if (done) done(); return; }
      const pts = String(risk.dataset.riskBreak || '620,295').split(',').map(Number);
      const crash = [Math.max(0, Math.min(fullCamera[2] - 160, pts[0] - 66)), Math.max(0, Math.min(fullCamera[3] - 100, pts[1] - 42)), 160, 100];
      const len = risk.getTotalLength ? risk.getTotalLength() : 200;
      risk.style.strokeDasharray = String(len);
      risk.style.strokeDashoffset = String(len);
      animateViewBox(svg, from, fullCamera.slice(), 360, () => {
        animateSteps(880, tk, p => {
          const e = easeInOut(p);
          risk.style.strokeDashoffset = String(len * (1 - e));
          setViewBox(svg, fullCamera.map((n, i) => n + (crash[i] - n) * e));
        }, done);
      }, tk);
      return;
    }
    if (type === 'enter') {
      setViewBox(svg, fullCamera);
      animateViewBox(svg, fullCamera.slice(), target, 720, done, tk);
      return;
    }
    if (type === 'advance') {
      const fromStage = Math.max(0, Math.min(3, Number(intent.fromStage != null ? intent.fromStage : Math.max(0, stage - 1))));
      const toStage = Math.max(0, Math.min(3, Number(intent.toStage != null ? intent.toStage : stage)));
      const fromOff = biomes[fromStage].offset;
      const toOff = biomes[toStage].offset;
      const fromFrac = 1 - fromOff / TRAIL_LENGTH;
      const toFrac = 1 - toOff / TRAIL_LENGTH;
      const trailEl = svg.querySelector('#activeTrail');
      const markerEl = svg.querySelector('#climberMarker');
      animateViewBox(svg, from, fullCamera.slice(), 420, () => {
        animateSteps(580, tk, p => {
          const e = easeInOut(p);
          if (trailEl) trailEl.setAttribute('stroke-dashoffset', String(fromOff + (toOff - fromOff) * e));
          if (markerEl) {
            const [mx, my] = trailPointAt(svg, fromFrac + (toFrac - fromFrac) * e);
            markerEl.setAttribute('transform', `translate(${mx.toFixed(2)} ${my.toFixed(2)})`);
          }
        }, () => {
          animateViewBox(svg, fullCamera.slice(), campCamera(toStage), 640, done, tk);
        });
      }, tk);
      return;
    }
    if (type === 'rewind') {
      const risk = svg.querySelector('.risk-path');
      const len = risk && risk.getTotalLength ? risk.getTotalLength() : 0;
      animateSteps(400, tk, p => {
        const e = easeOut(p);
        setViewBox(svg, from.map((n, i) => n + (fullCamera[i] - n) * e));
        if (risk && len) risk.style.strokeDashoffset = String(len * e);
      }, () => {
        animateViewBox(svg, fullCamera.slice(), target, 580, done, tk);
      });
      return;
    }
    const zoomedElsewhere = from[2] < 600 && (Math.abs(from[0] - target[0]) > 40 || Math.abs(from[1] - target[1]) > 40);
    if (zoomedElsewhere) {
      animateViewBox(svg, from, fullCamera.slice(), 320, () => animateViewBox(svg, fullCamera.slice(), target, 540, done, tk), tk);
    } else {
      animateViewBox(svg, from, target, 620, done, tk);
    }
  }

  function handleMountainAction(action, trigger, el, state, rerender, onSummit) {
    const syncViewportClass = () => {
      if (root.document && root.document.body) {
        root.document.body.classList.toggle('is-mountain-viewport', isMountainPhase(state));
      }
    };

    if (action === 'next-fears') {
      state.fearOrder = [...el.querySelectorAll('[data-fear]:checked')].map(x => x.dataset.fear);
      state.subjectiveConcern = (el.querySelector('[data-subjective]') || {}).value || '';
      const isCouple = !!(dataFor(state.caseId) && dataFor(state.caseId).meta && dataFor(state.caseId).meta.isCouple);
      state.phase = isCouple ? 'cordada' : 'expedition';
      state.timerStartedAt = Date.now();
      state.voters = specs[state.caseId][langOf(state)].people;
      if (!isCouple) {
        state.cameraMode = 'camp';
        state.focusedNode = state.stage || 0;
        state.dialogVisible = !hasRaf();
        state.initialViewBox = hasRaf() ? fullCamera.slice() : campCamera(state.focusedNode);
      }
      rerender();
      syncViewportClass();
      if (!isCouple && hasRaf()) {
        const svg = el.querySelector('.mountain-svg[data-camera]');
        runCamera(svg, { type: 'enter', stage: state.focusedNode }, () => { state.initialViewBox = null; revealDialog(el, state); });
      }
      return true;
    }

    if (action === 'start-expedition') {
      state.phase = 'expedition';
      state.view = viewName('expedition', langOf(state));
      state.cameraMode = 'camp';
      state.focusedNode = state.stage || 0;
      state.dialogVisible = !hasRaf();
      state.initialViewBox = hasRaf() ? fullCamera.slice() : campCamera(state.focusedNode);
      SherpasAI.request('pact', strictCasePayload(state.caseId, langOf(state), state.stage), { mode: 'deterministic' });
      rerender();
      syncViewportClass();
      if (hasRaf()) {
        const svg = el.querySelector('.mountain-svg[data-camera]');
        runCamera(svg, { type: 'enter', stage: state.focusedNode }, () => { state.initialViewBox = null; revealDialog(el, state); });
      }
      return true;
    }

    if (action === 'advance') {
      const route = (el.querySelector('[name="route"]:checked') || {}).value || 'good';
      const svg = el.querySelector('.mountain-svg[data-camera]');
      const prevBox = svg ? parseViewBox(svg) : fullCamera.slice();
      SherpasAI.request('reframe', Object.assign({ action, route }, strictCasePayload(state.caseId, langOf(state), state.stage)), { mode: 'deterministic' });

      if (route === 'bad') {
        state.history.push({ stage: state.stage, detailKey: 'D3', detail: dataFor(state.caseId).persona.D3 });
        state.blocked = true;
        state.phase = 'blocked';
        state.cameraMode = 'camp';
        state.dialogVisible = !hasRaf();
        state.initialViewBox = hasRaf() ? prevBox : riskCameraBox(riskRecord(state.caseId, langOf(state)), biomes[state.stage].point);
        rerender();
        syncViewportClass();
        if (hasRaf()) {
          const nextSvg = el.querySelector('.mountain-svg[data-camera]');
          runCamera(nextSvg, { type: 'risk', stage: state.stage }, () => { state.initialViewBox = null; revealDialog(el, state); });
        }
        return true;
      }

      const fromStage = Number(state.stage) || 0;
      const isSummitStep = fromStage >= 3;
      const toStage = isSummitStep ? 3 : fromStage + 1;
      hideDialogs(el, state);
      if (hasRaf() && svg) {
        runCamera(svg, { type: 'advance', fromStage, toStage }, () => {
          if (isSummitStep) {
            setTimeout(() => {
              state.initialViewBox = null;
              onSummit();
              syncViewportClass();
            }, 380);
          } else {
            state.stage = toStage;
            state.focusedNode = toStage;
            state.cameraMode = 'camp';
            state.dialogVisible = true;
            state.initialViewBox = campCamera(toStage);
            rerender();
            state.initialViewBox = null;
            syncViewportClass();
          }
        });
      } else {
        if (isSummitStep) onSummit();
        else {
          state.stage = toStage;
          state.focusedNode = toStage;
          state.dialogVisible = true;
          state.initialViewBox = campCamera(toStage);
          rerender();
          state.initialViewBox = null;
        }
        syncViewportClass();
      }
      return true;
    }

    if (action === 'rewind') {
      const svg = el.querySelector('.mountain-svg[data-camera]');
      const prevBox = svg ? parseViewBox(svg) : fullCamera.slice();
      hideDialogs(el, state);
      if (hasRaf() && svg) {
        runCamera(svg, { type: 'rewind', stage: state.stage }, () => {
          state.blocked = false;
          state.phase = 'expedition';
          state.focusedNode = state.stage;
          state.cameraMode = 'camp';
          state.dialogVisible = true;
          state.initialViewBox = campCamera(state.stage);
          rerender();
          state.initialViewBox = null;
          syncViewportClass();
        });
      } else {
        state.blocked = false;
        state.phase = 'expedition';
        state.focusedNode = state.stage;
        state.dialogVisible = true;
        state.initialViewBox = campCamera(state.stage);
        rerender();
        state.initialViewBox = null;
        syncViewportClass();
      }
      return true;
    }

    if (action === 'focus-node' || action === 'focus-active') {
      if (!isMountainPhase(state)) return true;
      const targetStage = action === 'focus-active' ? (Number(state.stage) || 0) : Number(trigger.dataset.node || 0);
      const svg = el.querySelector('.mountain-svg[data-camera]');
      const prevBox = svg ? parseViewBox(svg) : fullCamera.slice();
      state.focusedNode = targetStage;
      state.cameraMode = 'camp';
      state.dialogVisible = !hasRaf();
      state.initialViewBox = hasRaf() ? prevBox : campCamera(targetStage);
      rerender();
      syncViewportClass();
      if (hasRaf()) {
        const nextSvg = el.querySelector('.mountain-svg[data-camera]');
        runCamera(nextSvg, { type: 'focus', stage: targetStage }, () => { state.initialViewBox = null; revealDialog(el, state); });
      }
      return true;
    }

    if (action === 'zoom-out') {
      if (!isMountainPhase(state)) return true;
      const svg = el.querySelector('.mountain-svg[data-camera]');
      hideDialogs(el, state);
      showOverviewCta(el, state);
      if (hasRaf() && svg) {
        runCamera(svg, { type: 'overview' }, () => {
          state.initialViewBox = null;
        });
      } else if (svg) {
        setViewBox(svg, fullCamera);
      }
      return true;
    }

    return false;
  }

  function mount(target, options) {
    const el = typeof target === 'string' && root.document ? root.document.querySelector(target) : target;
    if (!el) throw Error('Sherpa Expedition container was not found');
    let state = (options && options.state) || createInitialState(options && options.caseId);
    const syncViewportClass = () => {
      if (root.document && root.document.body) {
        root.document.body.classList.toggle('is-mountain-viewport', isMountainPhase(state));
      }
    };
    const update = () => {
      cancelMotion();
      el.innerHTML = render(state);
      syncViewportClass();
      bind();
    };
    const onSummit = () => {
      state.summit = true;
      state.phase = 'summit';
      state.view = viewName('current', langOf(state));
      update();
    };
    function bind() {
      el.querySelectorAll('[data-case]').forEach(n => n.onchange = () => {
        const next = createInitialState(n.value);
        next.lang = state.lang;
        next.mode = state.mode;
        state = next;
        update();
      });
      el.querySelectorAll('[data-action]').forEach(n => n.onclick = () => {
        const a = n.dataset.action;
        if (handleMountainAction(a, n, el, state, () => { el.innerHTML = render(state); syncViewportClass(); bind(); }, onSummit)) return;
        if (a === 'nav') {
          state.view = n.dataset.view;
          if (viewKey(state.view) === 'expedition' && !state.summit && (state.phase === 'expedition' || state.phase === 'blocked')) {
            state.dialogVisible = true;
            state.initialViewBox = campCamera(state.focusedNode != null ? state.focusedNode : state.stage);
          }
        } else if (a === 'mode') state.mode = n.dataset.mode;
        else if (a === 'lang') { state.lang = n.dataset.lang === 'EN' ? 'EN' : 'ES'; persistLanguage(state.lang); state.view = viewName(viewKey(state.view), state.lang); }
        else if (a === 'submit-vote') {
          state.votes[state.voteTurn] = { fears: [...el.querySelectorAll('[data-vote-fear]:checked')].map(x => x.dataset.voteFear), priority: (el.querySelector('[data-priority]:checked') || {}).value || '' };
          if (state.voteTurn === 'A') state.voteTurn = 'B';
          else state.phase = 'cross';
        } else if (a === 'doubt') state.advisorDoubts.push(n.dataset.doubt || '');
        else if (a === 'repeat') { const next = createInitialState(state.caseId); next.lang = state.lang; next.mode = state.mode; state = next; }
        update();
        state.initialViewBox = null;
      });
      el.querySelectorAll('[data-fear]').forEach(n => n.onchange = () => { state.fearOrder = [...el.querySelectorAll('[data-fear]:checked')].map(x => x.dataset.fear); });
      el.querySelectorAll('[name="route"]').forEach(n => n.onchange = () => {
        const p = el.querySelector('[data-preview]');
        if (p) p.textContent = preview(state, localizeData(dataFor(state.caseId), langOf(state)), n.value);
      });
      const sub = el.querySelector('[data-subjective]');
      if (sub) sub.oninput = () => { state.subjectiveConcern = sub.value; };
    }

    if (isMountainPhase(state) && hasRaf()) {
      state.dialogVisible = false;
      state.initialViewBox = fullCamera.slice();
    }
    update();
    if (isMountainPhase(state) && hasRaf()) {
      const svg = el.querySelector('.mountain-svg[data-camera]');
      runCamera(svg, { type: 'enter', stage: state.focusedNode || 0 }, () => { state.initialViewBox = null; revealDialog(el, state); });
    }

    return {
      state,
      getState: () => state,
      render: () => render(state),
      setState(next) { state = next; update(); return state; },
      dispatch(a, v) {
        if (a === 'mode') state.mode = v;
        else if (a === 'nav') state.view = v;
        else if (a === 'lang') { state.lang = v === 'EN' ? 'EN' : 'ES'; persistLanguage(state.lang); state.view = viewName(viewKey(state.view), state.lang); }
        else if (a === 'summit') { state.summit = true; state.phase = 'summit'; state.view = viewName('current', langOf(state)); }
        update();
        return state;
      },
      unmount() { cancelMotion(); el.innerHTML = ''; if (root.document && root.document.body) root.document.body.classList.remove('is-mountain-viewport'); }
    };
  }

  return {
    listCases,
    getScenario: id => { const data = dataFor(id); return data ? { id, data, spec: specs[id] } : null; },
    createInitialState,
    render,
    mount,
    biomes,
    svgMarkup,
    yearlyMarkup,
    localizeData,
    viewName,
    viewKey,
    text: words,
    failTags,
    persistLanguage,
    SherpasAI,
    runCamera,
    campCamera,
    fullCamera,
    isMountainPhase,
    handleMountainAction,
    preview,
    riskRecord,
    strictCasePayload
  };
});
