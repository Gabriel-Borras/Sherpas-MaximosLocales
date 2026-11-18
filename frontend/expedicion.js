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
      basecamp: 'Basecamp', expedition: 'Basecamp', current: 'Día 0', overview: 'Basecamp',
      brief: 'Resumen para el asesor', radio: 'Radio / Shocks',
      select: 'Seleccionar hogar', nav: 'Navegación', plan: 'Plan financiero',
      fears: 'Fase 1A · Consulta de miedos', fearTitle: '¿Qué merece atención primero?',
      fearHelp: 'Ordena tus preocupaciones. Tus respuestas se guardan para el resumen del asesor.', fearAsk: '¿Qué te preocupa hoy?',
      continue: 'Continuar a la cordada', enter: 'Entrar a la montaña',
      team: 'Fase 1B · Cordada a ciegas · 60 segundos', private: 'Voto privado de',
      clock: 'El reloj no bloquea el avance. La otra persona no verá estas respuestas hasta el cruce.',
      growth: 'Priorizar crecimiento', debt: 'Priorizar deuda y protección', time: 'Tiempo disponible',
      save: 'Guardar y pasar a la otra persona', matches: 'Ver coincidencias', cross: 'Cruce de respuestas',
      agree: 'En qué coincidís al 100%', friction: 'Roces para conversar', pact: 'Pacto de flujo de caja',
      blocked: 'Desvío detectado en la ruta', stopped: 'Análisis del camino erróneo', impact: 'Consecuencia proyectada',
      context: 'Contexto adicional', tensions: 'Por qué ocurre (tensiones y hechos)', rewind: 'Rebobinar al campamento',
      phase: 'Basecamp · Ruta de ascenso', route: 'Una ruta, cuatro campamentos', choose: 'Elige el paso en este campamento',
      ignore: 'Seguir sin atender la tensión principal', confirm: 'Confirmar paso', doubt: 'Enviar duda al asesor',
      trend: 'Impacto directo', exact: 'Ver cálculo exacto', levers: 'Palancas individuales', none: 'Sin palancas registradas',
      yearly: 'Proyección anual', facts: 'Datos factuales', sources: 'Fuentes', concerns: 'Miedos y preocupaciones',
      noAnswer: 'Sin respuesta registrada.', couple: 'Pacto de pareja', questions: 'Dudas para el asesor',
      noQuestions: 'No hay dudas registradas.', discarded: 'Decisiones erróneas exploradas', noDiscarded: 'Aún no hay caminos erróneos explorados.',
      complete: 'Cima alcanzada', continueExpedition: 'Volver a Basecamp', repeat: 'Reiniciar ruta',
      next: 'Revisa los pasos del Día 0 o toca cualquier campamento y nodo rojo en Basecamp.',
      mapAria: 'Montaña sumi-e de la expedición Sherpas', risk: 'Desvío en riesgo',
      chart: 'Proyección anual: activos invertibles y patrimonio neto',
      chartAria: 'Comparación anual entre activos invertibles y patrimonio neto',
      blue: 'Azul: activos invertibles', green: 'Verde: patrimonio neto',
      different: 'Prioridad distinta', common: 'No aparece una diferencia de prioridad; revisen juntos las tensiones del plan.',
      panoramic: 'Vista general', focusActive: 'Ir al campamento activo',
      panoramicHint: 'Toca cualquier campamento o nodo rojo en la montaña para hacer zoom e inspeccionar.',
      inspectCamp: 'Inspección de campamento',
      inspectRiskTitle: 'Inspección de nodo rojo',
      whereTaken: 'a) Campamento donde se tomó',
      whatDecision: 'b) Qué decisión fue',
      whatCaused: 'c) Qué ocasionó (yearly literal / brecha)',
      whyHappened: 'd) Por qué (tensiones y hechos)',
      recommendedWas: 'Medida recomendada omitida'
    },
    EN: {
      basecamp: 'Basecamp', expedition: 'Basecamp', current: 'Day 0', overview: 'Basecamp',
      brief: 'Advisor Brief', radio: 'Radio / Shocks',
      select: 'Select household', nav: 'Navigation', plan: 'Financial plan',
      fears: 'Phase 1A · Fear quest', fearTitle: 'What deserves attention first?',
      fearHelp: 'Rank your concerns. Your answers are saved for the Advisor Brief.', fearAsk: 'What concerns you today?',
      continue: 'Continue to the rope team', enter: 'Enter the mountain',
      team: 'Phase 1B · Blind rope team · 60 seconds', private: 'Private vote by',
      clock: 'The clock does not block progress. The other person will not see these answers until the cross-check.',
      growth: 'Prioritize growth', debt: 'Prioritize debt and protection', time: 'Time available',
      save: 'Save and pass to the other person', matches: 'See matches', cross: 'Cross-check',
      agree: 'Where you agree 100%', friction: 'Tensions to discuss', pact: 'Cash-flow pact',
      blocked: 'Route deviation detected', stopped: 'Failed path analysis', impact: 'Projected consequence',
      context: 'Additional context', tensions: 'Why it happens (tensions and facts)', rewind: 'Rewind to camp',
      phase: 'Basecamp · Ascent route', route: 'One route, four camps', choose: 'Choose the step at this camp',
      ignore: 'Continue without addressing the main tension', confirm: 'Confirm step', doubt: 'Send question to Advisor Brief',
      trend: 'Direct impact', exact: 'See exact math', levers: 'Individual levers', none: 'No recorded levers',
      yearly: 'Yearly projection', facts: 'Facts', sources: 'Sources', concerns: 'Fears and concerns',
      noAnswer: 'No answer recorded.', couple: 'Couple pact', questions: 'Questions for the advisor',
      noQuestions: 'No questions recorded.', discarded: 'Explored wrong decisions', noDiscarded: 'No wrong paths explored yet.',
      complete: 'Summit reached', continueExpedition: 'Back to Basecamp', repeat: 'Restart route',
      next: 'Review Day 0 steps or click any camp and red node on Basecamp.',
      mapAria: 'Sherpas sumi-e expedition mountain', risk: 'Route at risk',
      chart: 'Yearly projection: investable assets and net worth',
      chartAria: 'Yearly comparison of investable assets and net worth',
      blue: 'Blue: investable assets', green: 'Green: net worth',
      different: 'Different priority', common: 'No priority difference appears; review the plan tensions together.',
      panoramic: 'Full mountain', focusActive: 'Go to active camp',
      panoramicHint: 'Click any camp or red failure node on the mountain to zoom in and inspect.',
      inspectCamp: 'Camp inspection',
      inspectRiskTitle: 'Red node inspection',
      whereTaken: 'a) Camp where decision was taken',
      whatDecision: 'b) What decision was taken',
      whatCaused: 'c) What it caused (literal yearly / gap)',
      whyHappened: 'd) Why (tensions and facts)',
      recommendedWas: 'Recommended move skipped'
    }
  };

  const campShorts = { ES: ['Base', 'C1', 'C2', 'Cima'], EN: ['Base', 'C1', 'C2', 'Summit'] };
  const t = (s, k) => words[langOf(s)][k] || k;
  const dayLabel = (lang, irlDay) => `${lang === 'EN' ? 'Day' : 'Día'} ${Number.isFinite(Number(irlDay)) ? Number(irlDay) : 0}`;
  const viewName = (key, lang, irlDay) => {
    const l = lang === 'EN' ? 'EN' : 'ES';
    if (key === 'current') return dayLabel(l, irlDay);
    if (key === 'expedition' || key === 'basecamp' || key === 'overview') return 'Basecamp';
    return words[l][key] || 'Basecamp';
  };
  const viewKey = value => {
    const v = String(value == null ? '' : value).trim();
    if (!v || v === 'Basecamp' || v === 'basecamp' || v === 'expedition' || v === 'Expedición' || v === 'Expedition') return 'expedition';
    if (v === 'overview' || v === 'Mapa general' || v === 'Overview map') return 'overview';
    if (v === 'current' || v === 'Paso actual' || v === 'Current step' || /^(D[ií]a|Day)\s+\d+/i.test(v)) return 'current';
    if (v === 'brief' || v === words.ES.brief || v === words.EN.brief) return 'brief';
    if (v === 'radio' || v === 'Radio' || v === words.ES.radio || v === words.EN.radio) return 'radio';
    return 'expedition';
  };

  const TRAIL_PATH = 'M 190 610 Q 285 552 390 465 Q 505 385 620 295 Q 725 222 830 130';
  const TRAIL_CTRLS = [[285, 552], [505, 385], [725, 222]];
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
      ES: { people: ['Michael'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Prioriza liquidez, cobertura paraguas y tasa de retiro sostenibile.', pact: 'Ejecutar medidas prioritarias de deuda, retiro y cobertura.', events: [] },
      EN: { people: ['Michael'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Prioritize liquidity, umbrella coverage, and a sustainable withdrawal rate.', pact: 'Execute priority debt, withdrawal, and coverage moves.', events: [] }
    },
    'samantha-lewis': {
      ES: { people: ['Samantha'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Cierra la brecha de cobertura patrimonial y reduce la concentración en VTI.', pact: 'Asegurar vivienda/vehículo y diversificar exposición.', events: [] },
      EN: { people: ['Samantha'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Close the property coverage gap and reduce single-name VTI concentration.', pact: 'Insure home/vehicle and diversify exposure.', events: [] }
    },
    'timothy-melanie-weah': {
      ES: { people: ['Timothy', 'Melanie'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Liquida la tarjeta al 18% APR con efectivo ocioso y añade cobertura de vida.', pact: 'Cancelar deuda rotativa y proteger a la familia.', events: [] },
      EN: { people: ['Timothy', 'Melanie'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Pay off the 18% APR revolving card with idle cash and add life coverage.', pact: 'Eliminate revolving debt and protect the household.', events: [] }
    },
    'daniel-emily-johnson': {
      ES: { people: ['Daniel', 'Emily'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Cubre el déficit crítico de seguro de vida y redirige ahorro hacia deuda y 401(k).', pact: 'Activar protección familiar y optimizar ahorro anual.', events: [] },
      EN: { people: ['Daniel', 'Emily'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Close the critical mortality coverage gap and redirect savings to debt and 401(k).', pact: 'Activate family protection and optimize annual savings.', events: [] }
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

  // Evaluate exact point along the mountain ascent curve for any fraction in [0, 1]
  function trailPointAtFraction(fraction) {
    const f = Math.max(0, Math.min(1, Number(fraction) || 0));
    const seg = Math.min(2, Math.floor(f * 3));
    const localT = Math.max(0, Math.min(1, (f * 3) - seg));
    const p0 = biomes[seg].point;
    const p2 = biomes[seg + 1].point;
    const ctrl = TRAIL_CTRLS[seg];
    const mt = 1 - localT;
    const x = mt * mt * p0[0] + 2 * mt * localT * ctrl[0] + localT * localT * p2[0];
    const y = mt * mt * p0[1] + 2 * mt * localT * ctrl[1] + localT * localT * p2[1];
    return [Math.round(x * 10) / 10, Math.round(y * 10) / 10];
  }

  // Build logical failure path: climbs along the mountain route up to the exhaustion age/year fraction, then drops to the bad point
  function riskCoordinates(record, stagePoint, stageIdx) {
    const idx = Math.max(0, Math.min(3, Number(stageIdx) || 0));
    const [sx, sy] = stagePoint || biomes[idx].point;
    if (!record || !record.hasExhaustion) {
      const bx = Math.min(1140, Math.round(sx + 42 + idx * 6));
      const by = Math.min(685, Math.round(sy + 14));
      return { sx, sy, rx: sx, ry: sy, x: bx, y: by, wall: true, d: `M ${sx} ${sy} L ${bx} ${by}` };
    }
    const startFrac = idx / 3;
    const exhaustFrac = record.length > 1 ? record.index / (record.length - 1) : startFrac;
    const climbFrac = Math.max(startFrac + 0.05, Math.min(0.96, exhaustFrac));
    const steps = 8;
    const climbPts = [];
    for (let i = 0; i <= steps; i++) {
      const f = startFrac + (climbFrac - startFrac) * (i / steps);
      climbPts.push(trailPointAtFraction(f));
    }
    const [rx, ry] = climbPts[climbPts.length - 1];
    const offsetSpread = idx * 18;
    const bx = Math.min(1130, Math.round(rx + 64 + offsetSpread));
    const by = Math.min(690, Math.round(ry + 82 + idx * 10));
    const ctrlX = Math.round(rx + (bx - rx) * 0.55);
    const ctrlY = Math.round(ry + 14);
    const climbD = climbPts.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${pt[0]} ${pt[1]}`).join(' ');
    const d = `${climbD} Q ${ctrlX} ${ctrlY} ${bx} ${by}`;
    return { sx, sy, rx, ry, x: bx, y: by, wall: false, climbFrac, exhaustFrac, d };
  }

  function blockedCopy(id, mode, persona, state) {
    const lang = langOf(state), record = riskRecord(id, lang);
    if (!record.hasExhaustion) {
      return lang === 'ES'
        ? 'Sin activos invertibles negativos en la proyección anual; el desvío mantiene una brecha de puntuación y liquidez/protección sin agotar la cartera.'
        : 'No negative investable assets in the yearly projection; the deviation leaves a score and liquidity/protection gap without exhausting the portfolio.';
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
    const first = rows[0] || {};
    const last = rows[rows.length - 1] || {};
    const rec = riskRecord(state.caseId, langOf(state));
    const es = langOf(state) === 'ES';
    const moveText = moves.slice(0, 5).map(m => {
      const label = m.title || (m.moves || []).join(' + ') || (es ? 'Medida' : 'Move');
      const before = m.score_before != null ? m.score_before : score.published_score;
      const after = m.score_after != null ? m.score_after : score.published_score;
      const delta = before != null && after != null ? ` (${esc(before)} → ${esc(after)})` : '';
      return `${esc(label)}${delta}`;
    }).join('; ') || t(state, 'none');
    return `<details class="exact-math"><summary>${t(state, 'exact')}</summary><ul><li><strong>Score:</strong> ${esc(score.published_score ?? '—')}/100 (${esc(score.band || '—')}).</li><li><strong>${t(state, 'levers')}:</strong> ${moveText}.</li><li><strong>${t(state, 'yearly')}:</strong> ${rows.length} ${es ? 'años' : 'years'} (${esc(first.year || '—')} ${esc(exactMoney(first.investable_assets))} → ${esc(last.year || '—')} ${esc(exactMoney(last.investable_assets))}; ${es ? 'patrimonio neto final' : 'final net worth'} ${esc(exactMoney(last.net_worth))}).</li><li><strong>${es ? 'Punto crítico yearly' : 'Yearly critical point'}:</strong> ${esc(rec.label)}</li></ul>${yearlyMarkup(data, langOf(state))}<p class="preview">${t(state, 'sources')}: score.pillars, score.top_moves, score.combined_moves, projections.yearly, persona.tensions.</p></details>`;
  }

  function stepGoodOption(state, data, s, stageIdx) {
    const moves = (data.score && data.score.top_moves) || [];
    if (stageIdx < moves.length && moves[stageIdx]) {
      const m = moves[stageIdx];
      return {
        label: m.action || m.title || s.pact,
        title: m.title || m.action || s.pact,
        scoreBefore: m.score_before,
        scoreAfter: m.score_after,
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
        title: comboLabel,
        scoreBefore: before,
        scoreAfter: best.score_after,
        trend: `${t(state, 'trend')}: ${comboLabel} (${langOf(state) === 'ES' ? 'puntaje' : 'score'} ${before} → ${best.score_after}).`
      };
    }
    const pub = (data.score && data.score.published_score) || 0;
    return { label: s.pact, title: s.pact, scoreBefore: pub, scoreAfter: pub, trend: `${t(state, 'trend')}: ${s.pact}` };
  }

  function preview(state, data, route) {
    if (route !== 'bad') return stepGoodOption(state, data, specs[state.caseId][langOf(state)], Number(state.stage) || 0).trend;
    const rec = riskRecord(state.caseId, langOf(state));
    return rec.hasExhaustion
      ? `${t(state, 'trend')}: ${rec.label}`
      : (langOf(state) === 'ES' ? 'Sin agotamiento anual de activos invertibles; persiste la brecha de puntuación del campamento.' : 'No yearly investable-asset exhaustion; the camp score gap persists.');
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
      view: viewName('expedition', lang, 0),
      phase: 'fears',
      mode: 'Plain',
      lang,
      irlDay: 0,
      fearOrder: [],
      subjectiveConcern: '',
      votes: {},
      voteTurn: 'A',
      timerStartedAt: null,
      stage: 0,
      focusedNode: 0,
      inspectedRisk: null,
      cameraMode: 'camp',
      dialogVisible: true,
      blocked: false,
      history: [],
      advisorDoubts: [],
      summit: false
    };
  }

  // The Sumi-e mountain is ALWAYS the 100vw x 100vh full-bleed background across the entire web app
  const isMountainPhase = state => !!state && (viewKey(state.view) === 'expedition' || viewKey(state.view) === 'overview') && (state.phase === 'expedition' || state.phase === 'blocked' || state.summit);

  // Camera framing a camp while leaving room on the left/bottom for the floating card
  function campCamera(stage) {
    const idx = Math.max(0, Math.min(3, Number(stage) || 0));
    const pt = biomes[idx].point;
    const w = 165, h = 103.125;
    const cx = idx === 3 ? pt[0] + 14 : pt[0];
    const cy = idx === 3 ? pt[1] - 14 : pt[1];
    const x = Math.max(0, Math.min(fullCamera[2] - w, cx - w * 0.58));
    const y = Math.max(0, Math.min(fullCamera[3] - h, cy - h * 0.42));
    return [x, y, w, h];
  }

  function riskCameraBox(record, stagePoint, stageIdx) {
    const coord = riskCoordinates(record, stagePoint, stageIdx);
    const w = 185, h = 115.625;
    const x = Math.max(0, Math.min(fullCamera[2] - w, coord.x - w * 0.56));
    const y = Math.max(0, Math.min(fullCamera[3] - h, coord.y - h * 0.44));
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

  function buildHistoryEntries(history, blocked, activeStage) {
    const list = Array.isArray(history) ? history.map((h, idx) => Object.assign({ index: idx, stage: Number(h && h.stage) || 0 }, h)) : [];
    if (blocked && !list.some(h => h.stage === activeStage)) {
      list.push({ index: list.length, stage: activeStage });
    }
    return list;
  }

  function svgMarkup(offset, point, history, blocked, couple, votes, failTag, lang, opts) {
    const norm = normalizePointAndOffset(offset, point);
    const [x, y] = norm.point;
    const activeStage = opts && opts.stage != null ? Number(opts.stage) : norm.stage;
    const activeOffset = Math.max(0, Math.min(TRAIL_LENGTH, Number(norm.offset) || 0));
    const record = failTag && typeof failTag === 'object' ? failTag : null;
    const entries = buildHistoryEntries(history, blocked, activeStage);
    const diverged = !!(entries.length || (votes && votes.A && votes.B && votes.A.priority && votes.B.priority && votes.A.priority !== votes.B.priority));
    const initialBox = (opts && opts.initialViewBox) ? opts.initialViewBox.map(n => Math.round(n * 100) / 100).join(' ') : fullCamera.join(' ');
    const shortLabels = campShorts[lang === 'EN' ? 'EN' : 'ES'];
    const inspectedIdx = opts && opts.inspectedRisk != null ? Number(opts.inspectedRisk) : null;

    // Render ALL persistent red failure paths and interactive red nodes at their ends
    const riskMarkup = entries.map((entry, idx) => {
      const originIdx = Math.max(0, Math.min(3, Number(entry.stage) || 0));
      const originPt = biomes[originIdx].point;
      const coord = riskCoordinates(record, originPt, originIdx);
      const isLatest = idx === entries.length - 1;
      const isInspected = inspectedIdx === idx || (blocked && isLatest);
      const nodeLabel = record && record.hasExhaustion
        ? `${shortLabels[originIdx]} → ${record.year}${record.age != null ? ` (${lang === 'EN' ? 'age' : 'edad'} ${record.age})` : ''} · ${exactMoney(record.investable_assets)}`
        : `${shortLabels[originIdx]} · ${lang === 'EN' ? 'Score gap' : 'Brecha del plan'}`;
      const stopWall = coord.wall
        ? `<path d="M ${coord.x} ${coord.y - 9} L ${coord.x} ${coord.y + 9}" stroke="#C83A2B" stroke-width="1.35" stroke-linecap="round"/>`
        : `<circle cx="${coord.rx}" cy="${coord.ry}" r="2.1" fill="#C83A2B" opacity=".85"/>`;
      return `<g class="risk-group" data-risk-stage="${originIdx}" data-risk-index="${idx}">
        <path class="risk-path" data-active-risk="${isLatest ? 'true' : 'false'}" data-risk-break="${coord.x},${coord.y}" data-exhaustion="${record && record.hasExhaustion ? 'true' : 'false'}" data-year="${record && record.year ? record.year : ''}" data-age="${record && record.age != null ? record.age : ''}" data-investable-assets="${record && record.investable_assets != null ? record.investable_assets : ''}" d="${coord.d}" stroke-width="${isInspected ? '2.6' : '2.1'}" opacity="${isInspected ? '0.96' : '0.82'}"/>
        ${stopWall}
        <g class="risk-node ${isInspected ? 'is-active' : ''}" data-action="inspect-risk" data-risk-index="${idx}" data-risk-stage="${originIdx}" transform="translate(${coord.x} ${coord.y})" role="button" tabindex="0" aria-label="${esc(nodeLabel)}">
          <circle class="risk-hit" cx="0" cy="0" r="16" fill="transparent"/>
          <circle class="risk-node-halo" cx="0" cy="0" r="${isInspected ? '6.5' : '5'}" fill="#C83A2B" opacity="${isInspected ? '0.28' : '0.18'}"/>
          <circle cx="0" cy="0" r="3.1" fill="#C83A2B" stroke="#FBF9F5" stroke-width="0.9"/>
          <text x="5.5" y="1.2" fill="#C83A2B" font-size="3.4" font-weight="600" font-family="system-ui">${esc(nodeLabel)}</text>
        </g>
      </g>`;
    }).join('');

    const partners = couple
      ? `<path class="partner-rope" d="${TRAIL_PATH}" transform="translate(-1.6 -1.1)" stroke="var(--partner-a)" stroke-width="1.25" opacity=".78"/><path class="partner-rope" d="${TRAIL_PATH}" transform="translate(1.6 1.1)" stroke="var(--partner-b)" stroke-width="1.25" opacity=".78"/>${diverged ? '<path class="partner-rope" d="M 390 465 Q 455 442 505 426 T 620 295" stroke="#C83A2B" stroke-dasharray="3 3" stroke-width="1.1" opacity=".68"/>' : ''}`
      : '';

    const campNodes = [
      `<g class="micro-camp ${activeStage === 0 ? 'is-active' : ''} ${activeStage > 0 ? 'is-reached' : ''}" data-action="focus-node" data-node="0" transform="translate(190 610)">
        <circle class="camp-hit" cx="0" cy="0" r="18" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="7.5"/>
        <path class="camp-tent" d="M -3.2 1.8 L 0 -3.8 L 3.2 1.8 Z" fill="#FBF9F5" stroke="#141311" stroke-width="0.55" stroke-linejoin="round"/>
        <text x="0" y="7.2" text-anchor="middle" font-size="3.1" font-family="system-ui" font-weight="600" fill="#141311" opacity=".82">${esc(shortLabels[0])} · 2,800m</text>
      </g>`,
      `<g class="micro-camp ${activeStage === 1 ? 'is-active' : ''} ${activeStage > 1 ? 'is-reached' : ''}" data-action="focus-node" data-node="1" transform="translate(390 465)">
        <circle class="camp-hit" cx="0" cy="0" r="18" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="7.5"/>
        <path class="camp-tent" d="M -3.2 1.8 L 0 -3.8 L 3.2 1.8 Z" fill="#FBF9F5" stroke="#141311" stroke-width="0.55" stroke-linejoin="round"/>
        <text x="0" y="7.2" text-anchor="middle" font-size="3.1" font-family="system-ui" font-weight="600" fill="#141311" opacity=".82">${esc(shortLabels[1])} · 4,600m</text>
      </g>`,
      `<g class="micro-camp ${activeStage === 2 ? 'is-active' : ''} ${activeStage > 2 ? 'is-reached' : ''}" data-action="focus-node" data-node="2" transform="translate(620 295)">
        <circle class="camp-hit" cx="0" cy="0" r="18" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="7.5"/>
        <path class="camp-tent" d="M -3.4 1.8 Q 0 -4.2 3.4 1.8 Z" fill="#FBF9F5" stroke="#141311" stroke-width="0.55"/>
        <text x="0" y="7.2" text-anchor="middle" font-size="3.1" font-family="system-ui" font-weight="600" fill="#141311" opacity=".82">${esc(shortLabels[2])} · 6,900m</text>
      </g>`,
      `<g class="micro-camp ${activeStage === 3 ? 'is-active' : ''}" data-action="focus-node" data-node="3" transform="translate(830 130)">
        <circle class="camp-hit" cx="8" cy="-12" r="24" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="7.5"/>
        <g class="sherpas-flag" aria-label="Sherpas">
          <path d="M 0 1 V -42" fill="none" stroke="#141311" stroke-width="1.3" stroke-linecap="round"/>
          <path d="M 0.5 -41 L 46 -30 L 0.5 -17 Z" fill="#141311"/>
          <path d="M 8 -29 L 15 -34.5 L 22 -29 L 15 -24 Z" fill="#FBF9F5"/>
          <text x="5.5" y="-20.5" fill="#FBF9F5" font-size="4.8" font-family="system-ui" font-weight="700" letter-spacing=".6">SHERPAS</text>
        </g>
        <text x="0" y="7.2" text-anchor="middle" font-size="3.1" font-family="system-ui" font-weight="700" fill="#141311" opacity=".88">${esc(shortLabels[3])} · 8,848m</text>
      </g>`
    ].join('');

    // Minimalist explorer point (#climberMarker)
    const climber = couple
      ? `<g id="climberMarker" class="climber-rig" transform="translate(${x} ${y})" data-cx="${x}" data-cy="${y}">
          <circle cx="-2.4" cy="0" r="4.2" fill="#4565d6" opacity=".18"/>
          <circle cx="2.4" cy="0" r="4.2" fill="#0d9488" opacity=".18"/>
          <circle cx="-2.4" cy="0" r="2.5" fill="#4565d6" stroke="#FBF9F5" stroke-width="1.1"/>
          <circle cx="2.4" cy="0" r="2.5" fill="#0d9488" stroke="#FBF9F5" stroke-width="1.1"/>
        </g>`
      : `<g id="climberMarker" class="climber-rig" transform="translate(${x} ${y})" data-cx="${x}" data-cy="${y}">
          <circle cx="0" cy="0" r="5.2" fill="#4565d6" opacity=".2"/>
          <circle cx="0" cy="0" r="3" fill="#4565d6" stroke="#FBF9F5" stroke-width="1.2"/>
        </g>`;

    // Sumi-e Japanese ink-wash pine silhouettes on the lower-left slope + tiny flock of ink birds
    const sumiPines = `<g class="sumi-pines" fill="#1e2024" opacity=".76">
      <path d="M 72 608 L 76 582 L 80 608 Z M 70 598 L 76 576 L 82 598 Z M 71 589 L 76 570 L 81 589 Z"/>
      <path d="M 88 614 L 93 578 L 98 614 Z M 86 600 L 93 570 L 100 600 Z M 88 588 L 93 563 L 98 588 Z" opacity=".88"/>
      <path d="M 108 622 L 112 592 L 116 622 Z M 106 610 L 112 585 L 118 610 Z" opacity=".62"/>
      <path d="M 128 626 L 133 586 L 138 626 Z M 126 612 L 133 578 L 140 612 Z M 128 598 L 133 572 L 138 598 Z" opacity=".82"/>
      <path d="M 152 635 L 156 602 L 160 635 Z M 150 622 L 156 595 L 162 622 Z" opacity=".54"/>
      <path d="M 218 648 L 223 610 L 228 648 Z M 216 634 L 223 602 L 230 634 Z" opacity=".68"/>
      <path d="M 244 656 L 248 626 L 252 656 Z M 242 644 L 248 618 L 254 644 Z" opacity=".48"/>
      <path d="M 326 482 Q 329 479 332 482 Q 335 479 338 482 M 344 474 Q 346.5 471.5 349 474 Q 351.5 471.5 354 474 M 362 478 Q 364 476 366 478 Q 368 476 370 478 M 382 468 Q 384.5 465.5 387 468 Q 389.5 465.5 392 468" fill="none" stroke="#2c2e33" stroke-width="0.9" stroke-linecap="round" opacity=".55"/>
    </g>`;

    return `<svg class="mountain-svg" data-camera="mountain" viewBox="${initialBox}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="${lang === 'EN' ? 'Sumi-e mountain route with Sherpas summit flag' : 'Ruta de montaña sumi-e con bandera Sherpas en la cima'}">
      <defs>
        <filter id="sumi-soft" x="-10%" y="-10%" width="120%" height="120%">
          <feGaussianBlur stdDeviation="6"/>
        </filter>
        <filter id="sumi-mist-blur" x="-15%" y="-20%" width="130%" height="140%">
          <feGaussianBlur stdDeviation="18"/>
        </filter>
        <linearGradient id="sumi-distant" x1="0.3" y1="0" x2="0.35" y2="1">
          <stop offset="0%" stop-color="#2c2f36" stop-opacity=".32"/>
          <stop offset="45%" stop-color="#555963" stop-opacity=".14"/>
          <stop offset="82%" stop-color="#FBF9F5" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="sumi-mid-wash" x1="0.45" y1="0" x2="0.5" y2="1">
          <stop offset="0%" stop-color="#1d1f24" stop-opacity=".46"/>
          <stop offset="50%" stop-color="#3d4048" stop-opacity=".2"/>
          <stop offset="88%" stop-color="#FBF9F5" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="sumi-peak-wash" x1="0.5" y1="0" x2="0.48" y2="1">
          <stop offset="0%" stop-color="#141519" stop-opacity=".76"/>
          <stop offset="34%" stop-color="#282a30" stop-opacity=".44"/>
          <stop offset="68%" stop-color="#5a5e68" stop-opacity=".15"/>
          <stop offset="94%" stop-color="#FBF9F5" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="sumi-forest-wash" x1="0.1" y1="0" x2="0.3" y2="1">
          <stop offset="0%" stop-color="#1c1e22" stop-opacity=".52"/>
          <stop offset="58%" stop-color="#484b52" stop-opacity=".18"/>
          <stop offset="95%" stop-color="#FBF9F5" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <g id="cameraRig">
        <!-- Distant soft sumi-e ink-wash mountain (upper left / center-left) -->
        <path class="sumi-wash" d="M 20 420 Q 115 340 195 310 Q 230 295 268 272 Q 315 245 365 282 Q 445 335 555 370 L 580 540 L 10 540 Z" fill="url(#sumi-distant)" filter="url(#sumi-soft)"/>
        <!-- Mid-ground misty sumi-e ridges -->
        <path class="sumi-wash" d="M 310 470 Q 395 405 462 355 Q 505 325 552 345 Q 620 278 688 228 Q 742 268 805 310 Q 915 215 978 242 Q 1055 280 1150 430 L 1170 620 L 290 620 Z" fill="url(#sumi-mid-wash)"/>
        <!-- Warm mist cloud dissolving mid-slopes -->
        <ellipse cx="520" cy="435" rx="390" ry="52" fill="#FBF9F5" opacity=".88" filter="url(#sumi-mist-blur)"/>
        <!-- Main sumi-e ascent mountain & contrasted rocky summit at (830, 130) -->
        <path id="layerMain" class="sumi-wash" d="M 35 695 Q 115 642 190 610 Q 292 544 390 465 Q 504 384 620 295 Q 702 228 768 182 Q 802 152 830 130 Q 858 154 892 212 Q 942 292 985 274 Q 1038 320 1135 485 L 1175 725 L 20 725 Z" fill="url(#sumi-peak-wash)"/>
        <!-- Summit snow/light crevices in sumi-e dry-brush style -->
        <path d="M 830 130 L 795 176 L 816 172 L 774 224 L 822 192 L 832 232 L 846 186 L 878 222 L 854 166 Z" fill="#FBF9F5" opacity=".78"/>
        <path d="M 620 295 L 588 334 L 614 326 L 574 372 L 626 340 L 648 358 Z" fill="#FBF9F5" opacity=".54"/>
        <path d="M 390 465 L 364 494 L 388 488 L 412 506 Z" fill="#FBF9F5" opacity=".46"/>
        <!-- Soft organic sumi-e ink brushwork along the main ridge -->
        <path class="sumi-ridge-soft" d="M 85 662 Q 140 632 190 610 Q 288 548 390 465 Q 505 385 620 295 Q 726 220 830 130 Q 868 168 912 246 M 955 286 Q 985 272 1048 345" fill="none" stroke-width="2.2" opacity=".64"/>
        <!-- Lower-left forested sumi-e slope dissolving into mist -->
        <path class="sumi-wash" d="M 30 585 Q 110 595 190 618 Q 275 645 375 675 L 385 745 L 20 745 Z" fill="url(#sumi-forest-wash)" filter="url(#sumi-soft)"/>
        ${sumiPines}
        <!-- Low warm mist ribbon blending the base into #FBF9F5 -->
        <ellipse cx="600" cy="695" rx="620" ry="58" fill="#FBF9F5" opacity=".9" filter="url(#sumi-mist-blur)"/>
        <!-- Ascent route & climber -->
        <path class="route-guide" d="${TRAIL_PATH}" stroke-width="1.4"/>
        <path id="activeTrail" class="route-ink" d="${TRAIL_PATH}" stroke-width="2.6" stroke-dasharray="${TRAIL_LENGTH}" stroke-dashoffset="${activeOffset}"/>
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

  const pillarShortCode = (pillarName, idx, lang) => {
    const p = String(pillarName || '').toLowerCase();
    if (p.includes('cash') || p.includes('ahorro') || p.includes('flujo')) return lang === 'EN' ? 'CF' : 'CF';
    if (p.includes('debt') || p.includes('deuda')) return 'DB';
    if (p.includes('inv')) return 'IN';
    if (p.includes('liq')) return 'LQ';
    if (p.includes('insur') || p.includes('segur') || p.includes('prot')) return 'PR';
    return ['CF', 'DB', 'IN', 'LQ', 'PR'][idx] || `P${idx + 1}`;
  };

  function renderHeader(state, data) {
    const lang = langOf(state);
    const score = (data && data.score) || {};
    const view = viewKey(state.view);
    const basecampActive = view === 'expedition' || view === 'overview';
    const dayActive = view === 'current';
    const briefActive = view === 'brief';
    const radioActive = view === 'radio';
    const options = ids.map(id => `<option value="${id}" ${id === state.caseId ? 'selected' : ''}>${esc(((dataFor(id) || {}).meta || {}).household || id)}</option>`).join('');

    const microPillars = (score.pillars || []).slice(0, 5).map((p, idx) => {
      const val = Math.max(0, Math.min(100, Number(p.score) || 0));
      const tone = val >= 70 ? 'is-ok' : val >= 40 ? 'is-warn' : 'is-danger';
      const code = pillarShortCode(p.pillar, idx, lang);
      const tip = `${p.pillar}: ${p.points_shown_in_app} (${val}%) · Score ${score.published_score ?? 0}/100`;
      return `<div class="micro-pillar" tabindex="0" role="group" aria-label="${esc(tip)}" title="${esc(tip)}">
        <span class="micro-pillar-code">${esc(code)}</span>
        <span class="micro-bar"><span class="micro-bar-fill ${tone}" style="width:${val}%"></span></span>
        <div class="micro-pillar-popover">
          <strong>${esc(p.pillar)}</strong><br>
          <span>${esc(p.points_shown_in_app)} · ${val}%</span><br>
          <span>${lang === 'EN' ? 'Plan score' : 'Score global'}: ${esc(score.published_score ?? 0)}/100</span>
        </div>
      </div>`;
    }).join('');

    const currentLabel = dayLabel(lang, state.irlDay);
    const briefTitle = words[lang].brief;
    const radioTitle = words[lang].radio;

    return `<header class="site-header header-floating">
      <a class="brand" href="#" data-action="nav" data-view="Basecamp">sherpas</a>
      <select class="case-select" aria-label="${t(state, 'select')}" data-case>${options}</select>
      <div class="micro-pillars" aria-label="${t(state, 'plan')} · ${esc(score.published_score ?? 0)}/100">${microPillars}</div>
      <nav class="site-nav" aria-label="${t(state, 'nav')}">
        <button class="nav-tab ${basecampActive ? 'active' : ''}" data-action="nav" data-view="Basecamp">Basecamp</button>
        <button class="nav-tab ${dayActive ? 'active' : ''}" data-action="nav" data-view="${esc(currentLabel)}">${esc(currentLabel)}</button>
        <button class="nav-icon-btn ${briefActive ? 'active' : ''}" data-action="nav" data-view="${esc(briefTitle)}" title="${esc(briefTitle)}" aria-label="${esc(briefTitle)}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12h6M9 16h4"/></svg>
        </button>
        <button class="nav-icon-btn ${radioActive ? 'active' : ''}" data-action="nav" data-view="${esc(radioTitle)}" title="${esc(radioTitle)}" aria-label="${esc(radioTitle)}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5M19.1 4.9C23 8.8 23 15.2 19.1 19.1"/><circle cx="12" cy="12" r="2"/></svg>
        </button>
      </nav>
      <div class="language-toggle" aria-label="${lang === 'ES' ? 'Idioma' : 'Language'}">
        <button data-action="lang" data-lang="ES" class="${lang === 'ES' ? 'active' : ''}">ES</button>
        <button data-action="lang" data-lang="EN" class="${lang === 'EN' ? 'active' : ''}">EN</button>
      </div>
    </header>`;
  }

  function renderRiskInspectionCard(state, data, persona, s, riskIdx) {
    const lang = langOf(state);
    const entries = buildHistoryEntries(state.history, state.blocked, state.stage);
    const entry = entries[Math.max(0, Math.min(entries.length - 1, Number(riskIdx) || 0))] || { stage: state.stage };
    const originStage = Math.max(0, Math.min(3, Number(entry.stage) || 0));
    const campInfo = biome(originStage, lang);
    const goodMove = stepGoodOption(state, data, s, originStage);
    const badChoiceText = (entry.decisionChosen && entry.decisionChosen[lang]) || t(state, 'ignore');
    const causedText = blockedCopy(state.caseId, state.mode, persona, state);
    const gapText = goodMove.scoreBefore != null && goodMove.scoreAfter != null
      ? ` (${lang === 'ES' ? 'brecha de score' : 'score gap'}: ${goodMove.scoreBefore} → ${goodMove.scoreAfter})`
      : '';
    const tensionsHtml = (persona.tensions || []).map(x => `<p>${detail(x.id, x.detail, lang)}</p>`).join('') || `<p>${esc(persona.D3 || '')}</p>`;

    return `<aside class="floating-dialog" data-dialog="blocked">
      <div class="floating-dialog-head">
        <div>
          <p class="eyebrow">${t(state, 'inspectRiskTitle')}</p>
          <h2>${t(state, 'stopped')}</h2>
        </div>
        <button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button>
      </div>
      <div class="crack">
        <div class="crack-grid">
          <div><strong>${t(state, 'whereTaken')}:</strong> ${esc(campInfo.label)}</div>
          <div><strong>${t(state, 'whatDecision')}:</strong> ${esc(badChoiceText)} · <em>${t(state, 'recommendedWas')}: ${esc(goodMove.label)}</em></div>
          <div><strong>${t(state, 'whatCaused')}:</strong> <span class="blocked-impact">${esc(causedText)}${esc(gapText)}</span></div>
          <div><strong>${t(state, 'whyHappened')}:</strong> ${tensionsHtml}</div>
        </div>
      </div>
      ${mathSummary(data, state)}
      <div class="button-row">
        ${state.blocked ? `<button class="primary" data-action="rewind">${t(state, 'rewind')}</button>` : `<button class="primary" data-action="focus-active">${t(state, 'focusActive')}</button>`}
        <button data-action="zoom-out">${t(state, 'panoramic')}</button>
      </div>
    </aside>`;
  }

  function render(state) {
    state = state || createInitialState();
    const lang = langOf(state);
    const raw = dataFor(state.caseId) || {};
    const data = localizeData(raw, lang);
    const persona = data.persona || {};
    const s = specs[state.caseId][lang];
    const couple = !!(data.meta && data.meta.isCouple);
    const stageIdx = Math.max(0, Math.min(3, Number(state.stage) || 0));
    const focusedIdx = state.focusedNode != null ? Math.max(0, Math.min(3, Number(state.focusedNode) || 0)) : stageIdx;
    const stage = biome(stageIdx, lang);
    const view = viewKey(state.view);
    const dialogVisible = state.dialogVisible !== false;
    const fail = failTags[state.caseId][lang];
    const shortLabels = campShorts[lang];
    const entries = buildHistoryEntries(state.history, state.blocked, stageIdx);
    const activeRiskIdx = state.inspectedRisk != null ? Number(state.inspectedRisk) : (state.blocked ? Math.max(0, entries.length - 1) : null);

    let initBox = fullCamera;
    if (view === 'expedition' && (state.phase === 'expedition' || state.phase === 'blocked')) {
      if (state.initialViewBox) initBox = state.initialViewBox;
      else if (state.cameraMode === 'panoramic') initBox = fullCamera;
      else if (state.blocked || activeRiskIdx != null) {
        const rEntry = entries[activeRiskIdx] || { stage: stageIdx };
        initBox = dialogVisible ? riskCameraBox(fail, biomes[rEntry.stage || 0].point, rEntry.stage || 0) : fullCamera;
      } else {
        initBox = dialogVisible ? campCamera(focusedIdx) : fullCamera;
      }
    }

    const wallpaper = `<div class="mountain-stage mountain-fullscreen ${state.blocked ? 'storm-shake' : ''}" data-biome="${stage.id}" data-dialog-ready="${dialogVisible ? 'true' : 'false'}">
      ${svgMarkup(state.summit ? 0 : stage.offset, state.summit ? biomes[3].point : stage.point, state.history || [], state.blocked, couple, state.votes, fail, lang, { stage: state.summit ? 3 : stageIdx, initialViewBox: initBox, inspectedRisk: activeRiskIdx })}
    </div>`;

    let panel = '';
    if (view === 'brief') {
      panel = `<aside class="floating-panel panel-wide"><p class="eyebrow">${t(state, 'brief')}</p><h1>${t(state, 'brief')}</h1><div class="advisor-brief"><h2>${t(state, 'concerns')}</h2><p>${esc(state.subjectiveConcern || persona.subjectiveConcerns || t(state, 'noAnswer'))}</p><p>${(state.fearOrder || []).map(esc).join(' · ')}</p></div><div class="advisor-brief"><h2>${t(state, 'couple')}</h2><p>${esc(s.pact)}</p></div><div class="advisor-brief"><h2>${t(state, 'questions')}</h2>${(state.advisorDoubts || []).map(x => `<p>${esc(x)}</p>`).join('') || `<p>${t(state, 'noQuestions')}</p>`}</div><div class="advisor-brief"><h2>${t(state, 'discarded')}</h2>${entries.map(x => `<p><strong>${esc(biome(x.stage || 0, lang).label)}:</strong> ${esc((x.decisionChosen && x.decisionChosen[lang]) || t(state, 'ignore'))} → ${esc(fail.label)}</p>`).join('') || `<p>${t(state, 'noDiscarded')}</p>`}</div>${mathSummary(data, state)}</aside>`;
    } else if (view === 'current') {
      panel = `<aside class="floating-panel"><p class="eyebrow">${esc(dayLabel(lang, state.irlDay))}</p><h2>${esc(s.pact)}</h2><p class="body-copy">${t(state, 'next')}</p>${mathSummary(data, state)}<div class="button-row"><button class="primary" data-action="nav" data-view="Basecamp">${t(state, 'continueExpedition')}</button><button data-action="repeat">${t(state, 'repeat')}</button></div></aside>`;
    } else if (state.phase === 'fears' && !state.summit) {
      panel = `<aside class="floating-panel"><p class="eyebrow">${t(state, 'fears')}</p><h1>${t(state, 'fearTitle')}</h1><p class="body-copy">${t(state, 'fearHelp')}</p><div class="choice-list">${(persona.objectiveConcerns || []).map(c => `<label class="choice"><input type="checkbox" data-fear="${esc(c.id)}" ${(state.fearOrder || []).includes(c.id) ? 'checked' : ''}><span>${detail(c.id, c.detail, lang)}</span></label>`).join('')}</div><label for="subjective">${t(state, 'fearAsk')}</label><textarea id="subjective" data-subjective>${esc(state.subjectiveConcern || '')}</textarea>${mathSummary(data, state)}<div class="button-row"><button class="primary" data-action="next-fears">${couple ? t(state, 'continue') : t(state, 'enter')}</button></div></aside>`;
    } else if (state.phase === 'cordada' && !state.summit) {
      panel = `<aside class="floating-panel"><p class="eyebrow">${t(state, 'team')}</p><h1>${t(state, 'private')} ${esc((state.voters || s.people)[state.voteTurn === 'A' ? 0 : 1])}</h1><p>${t(state, 'clock')}</p><div class="choice-list">${(persona.objectiveConcerns || []).map(c => `<label class="choice"><input type="checkbox" data-vote-fear="${esc(c.id)}"><span>${detail(c.id, c.detail, lang)}</span></label>`).join('')}<label class="choice"><input type="radio" name="priority" value="crecimiento" data-priority><span>${t(state, 'growth')}</span></label><label class="choice"><input type="radio" name="priority" value="deuda-proteccion" data-priority><span>${t(state, 'debt')}</span></label></div><p class="eyebrow">${t(state, 'time')}: ${Math.max(0, 60 - Math.floor((Date.now() - (state.timerStartedAt || Date.now())) / 1000))} s</p>${mathSummary(data, state)}<div class="button-row"><button class="primary" data-action="submit-vote">${state.voteTurn === 'A' ? t(state, 'save') : t(state, 'matches')}</button></div></aside>`;
    } else if (state.phase === 'cross' && !state.summit) {
      const a = state.votes.A || {}, b = state.votes.B || {};
      const common = (a.fears || []).filter(id => (b.fears || []).includes(id));
      const shared = common.length ? common.map(id => { const x = (persona.objectiveConcerns || []).find(c => c.id === id); return `<li>${x ? detail(id, x.detail, lang) : esc(id)}</li>`; }).join('') : `<li>${lang === 'ES' ? 'D6: proteger a los hijos.' : 'D6: protect the children.'}</li>`;
      const fr = [...(a.priority && b.priority && a.priority !== b.priority ? [`<p><strong>${t(state, 'different')}:</strong> ${t(state, a.priority === 'crecimiento' ? 'growth' : 'debt')} ${lang === 'ES' ? 'frente a' : 'versus'} ${t(state, b.priority === 'crecimiento' ? 'growth' : 'debt')}.</p>`] : []), ...(persona.tensions || []).slice(0, 2).map(x => `<p>${detail(x.id, x.detail, lang)}</p>`)].join('') || `<p>${t(state, 'common')}</p>`;
      panel = `<aside class="floating-panel"><p class="eyebrow">${t(state, 'cross')}</p><h1>${t(state, 'agree')}</h1><ul>${shared}</ul><h2>${t(state, 'friction')}</h2>${fr}<p class="reframe">${t(state, 'pact')}: ${esc(s.pact)}</p>${mathSummary(data, state)}<div class="button-row"><button class="primary" data-action="start-expedition">${t(state, 'enter')}</button></div></aside>`;
    } else if (state.blocked || activeRiskIdx != null) {
      const cardHtml = renderRiskInspectionCard(state, data, persona, s, activeRiskIdx != null ? activeRiskIdx : Math.max(0, entries.length - 1));
      panel = (dialogVisible ? cardHtml : cardHtml.replace('class="floating-dialog"', 'class="floating-dialog is-dialog-hidden" hidden'))
        + `<div class="floating-overview-cta ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'is-hidden'}" ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'hidden'}><span>${t(state, 'panoramicHint')}</span><button class="primary" data-action="focus-active">${t(state, 'focusActive')}</button></div>`;
    } else {
      const inspectingOther = (focusedIdx !== stageIdx) || state.summit || view === 'overview';
      const focusedBiome = biome(focusedIdx, lang);
      const focusedMove = stepGoodOption(state, data, s, focusedIdx);
      const activeMove = stepGoodOption(state, data, s, stageIdx);
      const campRiskIdx = entries.findIndex(e => Number(e.stage) === focusedIdx);
      const dialogContent = inspectingOther
        ? `<div class="floating-dialog-head"><div><p class="eyebrow">${t(state, 'inspectCamp')} · ${esc(focusedBiome.label)}</p><h2>${esc(shortLabels[focusedIdx])}</h2></div><button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
           <p class="reframe">${esc(focusedMove.label)}</p>
           <p class="preview">${esc(focusedMove.trend)}</p>
           ${campRiskIdx >= 0 ? `<div class="crack"><strong>${t(state, 'whatCaused')}:</strong> ${esc(fail.label)} <button data-action="inspect-risk" data-risk-index="${campRiskIdx}">${t(state, 'inspectRiskTitle')}</button></div>` : ''}
           ${mathSummary(data, state)}
           <div class="button-row">
             ${!state.summit && focusedIdx !== stageIdx ? `<button class="primary" data-action="focus-active">${t(state, 'focusActive')}</button>` : ''}
             <button data-action="zoom-out">${t(state, 'panoramic')}</button>
             ${state.summit ? `<button data-action="repeat">${t(state, 'repeat')}</button>` : ''}
           </div>`
        : `<div class="floating-dialog-head"><div><p class="eyebrow">${t(state, 'phase')} · ${esc(stage.label)}</p><h2>${t(state, 'choose')}</h2></div><button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
           <p class="reframe">${esc(s.reframe)}</p>
           <div class="choice-list">
             <label class="choice"><input type="radio" name="route" value="good" checked><span>${esc(activeMove.label)}</span></label>
             <label class="choice"><input type="radio" name="route" value="bad"><span>${stageIdx === 1 && s.events.length ? esc(s.events[0]) : t(state, 'ignore')}</span></label>
           </div>
           <p class="preview" data-preview>${esc(preview(state, data, 'good'))}</p>
           ${mathSummary(data, state)}
           <div class="button-row"><button class="primary" data-action="advance">${t(state, 'confirm')}</button></div>`;
      panel = `<aside class="floating-dialog ${dialogVisible ? '' : 'is-dialog-hidden'}" data-dialog="decision" ${dialogVisible ? '' : 'hidden'}>${dialogContent}</aside>
        <div class="floating-overview-cta ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'is-hidden'}" ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'hidden'}><span>${t(state, 'panoramicHint')}</span><button class="primary" data-action="focus-active">${t(state, 'focusActive')}</button></div>`;
    }

    return `${renderHeader(state, data)}<main class="page-shell page-mountain-full">${wallpaper}${panel}</main>`;
  }

  function createSherpasAI() {
    if (root.SherpasAI) return root.SherpasAI;
    const mark = mode => { if (root.document) root.document.documentElement.dataset.sherpasAi = mode; };
    const client = {
      mode: 'deterministic',
      last: null,
      request(kind, payload, fallback) {
        const local = fallback == null ? { mode: 'deterministic', kind, strict_zero_inference: true } : fallback;
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
    return trailPointAtFraction(fraction);
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
    const target = intent && intent.targetBox ? intent.targetBox : campCamera(stage);
    const from = parseViewBox(svg);

    if (type === 'overview') {
      animateViewBox(svg, from, fullCamera.slice(), 480, done, tk);
      return;
    }
    if (type === 'risk') {
      const risks = svg.querySelectorAll('.risk-path');
      const risk = svg.querySelector('.risk-path[data-active-risk="true"]') || risks[risks.length - 1];
      if (!risk) { if (done) done(); return; }
      const pts = String(risk.dataset.riskBreak || '620,295').split(',').map(Number);
      const w = 185, h = 115.625;
      const crash = [Math.max(0, Math.min(fullCamera[2] - w, pts[0] - w * 0.56)), Math.max(0, Math.min(fullCamera[3] - h, pts[1] - h * 0.44)), w, h];
      const len = risk.getTotalLength ? risk.getTotalLength() : 220;
      risk.style.strokeDasharray = String(len);
      risk.style.strokeDashoffset = String(len);
      animateViewBox(svg, from, fullCamera.slice(), 340, () => {
        animateSteps(920, tk, p => {
          const e = easeInOut(p);
          risk.style.strokeDashoffset = String(len * (1 - e));
          if (typeof risk.getPointAtLength === 'function') {
            const pt = risk.getPointAtLength(len * e);
            const curW = fullCamera[2] + (w - fullCamera[2]) * e;
            const curH = fullCamera[3] + (h - fullCamera[3]) * e;
            const curX = Math.max(0, Math.min(fullCamera[2] - curW, pt.x - curW * 0.56));
            const curY = Math.max(0, Math.min(fullCamera[3] - curH, pt.y - curH * 0.44));
            setViewBox(svg, [curX, curY, curW, curH]);
          } else {
            setViewBox(svg, fullCamera.map((n, i) => n + (crash[i] - n) * e));
          }
        }, done);
      }, tk);
      return;
    }
    if (type === 'enter') {
      setViewBox(svg, fullCamera);
      animateViewBox(svg, fullCamera.slice(), target, 700, done, tk);
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
      animateViewBox(svg, from, fullCamera.slice(), 400, () => {
        animateSteps(560, tk, p => {
          const e = easeInOut(p);
          if (trailEl) trailEl.setAttribute('stroke-dashoffset', String(fromOff + (toOff - fromOff) * e));
          if (markerEl) {
            const [mx, my] = trailPointAt(svg, fromFrac + (toFrac - fromFrac) * e);
            markerEl.setAttribute('transform', `translate(${mx.toFixed(2)} ${my.toFixed(2)})`);
          }
        }, () => {
          animateViewBox(svg, fullCamera.slice(), campCamera(toStage), 620, done, tk);
        });
      }, tk);
      return;
    }
    if (type === 'rewind') {
      animateViewBox(svg, from, fullCamera.slice(), 360, () => {
        animateViewBox(svg, fullCamera.slice(), target, 540, done, tk);
      }, tk);
      return;
    }
    const zoomedElsewhere = from[2] < 600 && (Math.abs(from[0] - target[0]) > 40 || Math.abs(from[1] - target[1]) > 40);
    if (zoomedElsewhere) {
      animateViewBox(svg, from, fullCamera.slice(), 300, () => animateViewBox(svg, fullCamera.slice(), target, 520, done, tk), tk);
    } else {
      animateViewBox(svg, from, target, 600, done, tk);
    }
  }

  function handleMountainAction(action, trigger, el, state, rerender, onSummit) {
    const syncViewportClass = () => {
      if (root.document && root.document.body) {
        root.document.body.classList.add('is-mountain-viewport');
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
        state.inspectedRisk = null;
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
      state.view = viewName('expedition', langOf(state), state.irlDay);
      state.cameraMode = 'camp';
      state.focusedNode = state.stage || 0;
      state.inspectedRisk = null;
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
        const raw = dataFor(state.caseId) || {};
        const dataES = localizeData(raw, 'ES');
        const goodES = stepGoodOption({ caseId: state.caseId, lang: 'ES' }, dataES, specs[state.caseId].ES, state.stage);
        const goodEN = stepGoodOption({ caseId: state.caseId, lang: 'EN' }, raw, specs[state.caseId].EN, state.stage);
        const existingIdx = state.history.findIndex(h => Number(h.stage) === Number(state.stage));
        const entry = {
          stage: state.stage,
          campLabel: { ES: biomes[state.stage].ES, EN: biomes[state.stage].EN },
          decisionChosen: { ES: words.ES.ignore, EN: words.EN.ignore },
          recommendedMove: { ES: goodES.label, EN: goodEN.label, scoreBefore: goodEN.scoreBefore, scoreAfter: goodEN.scoreAfter },
          detailKey: 'D3',
          detail: (raw.persona || {}).D3 || ''
        };
        if (existingIdx >= 0) {
          state.history[existingIdx] = entry;
          state.inspectedRisk = existingIdx;
        } else {
          state.history.push(entry);
          state.inspectedRisk = state.history.length - 1;
        }
        state.blocked = true;
        state.phase = 'blocked';
        state.cameraMode = 'camp';
        state.dialogVisible = !hasRaf();
        state.initialViewBox = hasRaf() ? prevBox : riskCameraBox(riskRecord(state.caseId, langOf(state)), biomes[state.stage].point, state.stage);
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
      state.inspectedRisk = null;
      hideDialogs(el, state);
      if (hasRaf() && svg) {
        runCamera(svg, { type: 'advance', fromStage, toStage }, () => {
          if (isSummitStep) {
            setTimeout(() => {
              state.initialViewBox = null;
              onSummit();
              syncViewportClass();
            }, 340);
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
      hideDialogs(el, state);
      state.inspectedRisk = null;
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

    if (action === 'inspect-risk') {
      const riskIdx = Number(trigger.dataset.riskIndex || 0);
      const entries = buildHistoryEntries(state.history, state.blocked, state.stage);
      const entry = entries[Math.max(0, Math.min(entries.length - 1, riskIdx))] || { stage: state.stage };
      const rStage = Math.max(0, Math.min(3, Number(entry.stage) || 0));
      const targetBox = riskCameraBox(riskRecord(state.caseId, langOf(state)), biomes[rStage].point, rStage);
      const svg = el.querySelector('.mountain-svg[data-camera]');
      const prevBox = svg ? parseViewBox(svg) : fullCamera.slice();
      state.view = viewName('expedition', langOf(state), state.irlDay);
      state.inspectedRisk = riskIdx;
      state.cameraMode = 'camp';
      state.dialogVisible = !hasRaf();
      state.initialViewBox = hasRaf() ? prevBox : targetBox;
      rerender();
      syncViewportClass();
      if (hasRaf()) {
        const nextSvg = el.querySelector('.mountain-svg[data-camera]');
        runCamera(nextSvg, { type: 'focus', stage: rStage, targetBox }, () => { state.initialViewBox = null; revealDialog(el, state); });
      }
      return true;
    }

    if (action === 'focus-node' || action === 'focus-active') {
      const targetStage = action === 'focus-active' ? (Number(state.stage) || 0) : Number(trigger.dataset.node || 0);
      const svg = el.querySelector('.mountain-svg[data-camera]');
      const prevBox = svg ? parseViewBox(svg) : fullCamera.slice();
      state.view = viewName('expedition', langOf(state), state.irlDay);
      state.blocked = false;
      if (state.phase === 'blocked') state.phase = 'expedition';
      state.inspectedRisk = null;
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
      const svg = el.querySelector('.mountain-svg[data-camera]');
      state.inspectedRisk = null;
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
        root.document.body.classList.add('is-mountain-viewport');
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
      state.view = viewName('current', langOf(state), state.irlDay);
      update();
    };
    function bind() {
      el.querySelectorAll('[data-case]').forEach(n => n.onchange = () => {
        const next = createInitialState(n.value);
        next.lang = state.lang;
        state = next;
        update();
      });
      el.querySelectorAll('[data-action]').forEach(n => n.onclick = (ev) => {
        if (n.tagName === 'A' && ev && ev.preventDefault) ev.preventDefault();
        const a = n.dataset.action;
        if (handleMountainAction(a, n, el, state, () => { el.innerHTML = render(state); syncViewportClass(); bind(); }, onSummit)) return;
        if (a === 'nav') {
          state.view = n.dataset.view;
          const vk = viewKey(state.view);
          if (vk === 'expedition' || vk === 'overview') {
            if (state.summit || vk === 'overview') {
              state.cameraMode = 'panoramic';
              state.dialogVisible = false;
              state.initialViewBox = fullCamera.slice();
            } else if (state.phase === 'expedition' || state.phase === 'blocked') {
              state.dialogVisible = true;
              state.initialViewBox = campCamera(state.focusedNode != null ? state.focusedNode : state.stage);
            }
          }
        } else if (a === 'lang') {
          state.lang = n.dataset.lang === 'EN' ? 'EN' : 'ES';
          persistLanguage(state.lang);
          state.view = viewName(viewKey(state.view), state.lang, state.irlDay);
        } else if (a === 'submit-vote') {
          state.votes[state.voteTurn] = { fears: [...el.querySelectorAll('[data-vote-fear]:checked')].map(x => x.dataset.voteFear), priority: (el.querySelector('[data-priority]:checked') || {}).value || '' };
          if (state.voteTurn === 'A') state.voteTurn = 'B';
          else state.phase = 'cross';
        } else if (a === 'doubt') state.advisorDoubts.push(n.dataset.doubt || '');
        else if (a === 'repeat') { const next = createInitialState(state.caseId); next.lang = state.lang; state = next; }
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
        else if (a === 'lang') { state.lang = v === 'EN' ? 'EN' : 'ES'; persistLanguage(state.lang); state.view = viewName(viewKey(state.view), state.lang, state.irlDay); }
        else if (a === 'summit') { state.summit = true; state.phase = 'summit'; state.view = viewName('current', langOf(state), state.irlDay); }
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
    renderHeader,
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
