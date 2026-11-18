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
      fears: 'Fase 1A · Evaluación inicial',
      fearTitle: '¿Qué tres temas te quitan más tranquilidad hoy?',
      fearHelp: 'Toca hasta 3 tarjetas por orden de prioridad (1º, 2º y 3º) y ajusta tu termómetro emocional. Tu #1 enfocará el primer nodo del Basecamp.',
      fearAsk: 'Duda libre o nota para tu asesor (opcional)',
      fearPlaceholder: 'Ej.: ¿Cómo afecta esto a nuestra liquidez de este año?',
      continue: 'Ver diagnóstico y contraste',
      enter: 'Entrar al Basecamp',
      backEval: 'Editar Top-3',
      team: 'Fase 1A · Turno privado en pareja',
      private: 'Turno privado de',
      blindHint: 'Elige tu Top-3 y tu nivel de inquietud sin que la otra persona vea la pantalla.',
      growth: 'Priorizar crecimiento patrimonial',
      debt: 'Priorizar liquidez, deuda y protección',
      time: 'Turno a ciegas',
      save: 'Guardar mi turno y pasar a',
      matches: 'Ver diagnóstico de pareja y contraste',
      cross: 'Diagnóstico inicial y contraste del plan',
      agree: 'Coincidencias en vuestro Top-3',
      friction: 'Diferencias de foco y tensiones del plan',
      pact: 'Pacto de ruta hacia el Basecamp',
      contrastTitle: 'Contraste: Lo que más te preocupa vs. Lo que más impacta tu plan',
      whatWorries: 'Tu prioridad #1 declarada',
      whatImpacts: 'Lo que más mueve la aguja en tus números',
      blindSpot: 'Lectura de contraste',
      thermometerTitle: 'Termómetro emocional ante el plan',
      thermoGapTitle: 'Termómetro emocional de la pareja',
      profileSplitTitle: 'Perfil de riesgo declarado vs. cartera real',
      rankBadge: ['1º', '2º', '3º'],
      pickRank: 'Elegir',
      top3Counter: 'Top-3 seleccionado',
      focusBanner: 'Foco #1 priorizado en este nodo',
      blocked: 'Desvío detectado en la ruta', stopped: 'Análisis del camino erróneo', impact: 'Consecuencia proyectada',
      context: 'Contexto adicional', tensions: 'Por qué ocurre (tensiones y hechos)', rewind: 'Rebobinar al campamento',
      phase: 'Basecamp · Ruta de ascenso', route: 'Una ruta, cuatro campamentos', choose: 'Elige el paso en este campamento',
      ignore: 'Posponer esta medida y mantener la exposición actual', confirm: 'Confirmar paso', doubt: 'Enviar duda al asesor',
      trend: 'Impacto directo', exact: 'Ver cálculo exacto', levers: 'Palancas individuales', none: 'Sin palancas registradas',
      yearly: 'Proyección anual', facts: 'Datos factuales', sources: 'Fuentes', concerns: 'Top-3 preocupaciones y termómetro',
      noAnswer: 'Sin duda adicional registrada.', couple: 'Diagnóstico y pacto de pareja', questions: 'Dudas para el asesor',
      noQuestions: 'No hay dudas registradas.', discarded: 'Decisiones erróneas exploradas', noDiscarded: 'Aún no hay caminos erróneos explorados.',
      complete: 'Cima alcanzada', continueExpedition: 'Volver a Basecamp', repeat: 'Reiniciar evaluación',
      next: 'Revisa los pasos del Día 0 o toca cualquier campamento y nodo rojo en Basecamp.',
      mapAria: 'Montaña sumi-e de la expedición Sherpas', risk: 'Desvío en riesgo',
      chart: 'Proyección anual: activos invertibles y patrimonio neto',
      chartAria: 'Comparación anual entre activos invertibles y patrimonio neto',
      blue: 'Azul: activos invertibles', green: 'Verde: patrimonio neto',
      different: 'Prioridad distinta en la pareja', common: 'Ambos compartís el mismo enfoque general; revisad juntos cómo repartir el flujo anual.',
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
      fears: 'Phase 1A · Initial Assessment',
      fearTitle: 'Which three topics weigh most on your peace of mind today?',
      fearHelp: 'Click up to 3 cards in priority order (1st, 2nd, 3rd) and set your emotional thermometer. Your #1 choice will focus the first critical Basecamp node.',
      fearAsk: 'Open question or note for your advisor (optional)',
      fearPlaceholder: 'E.g., How does this affect our cash cushion this year?',
      continue: 'View diagnosis and plan contrast',
      enter: 'Enter Basecamp',
      backEval: 'Edit Top-3',
      team: 'Phase 1A · Private couple turn',
      private: 'Private turn for',
      blindHint: 'Pick your Top-3 and stress thermometer privately before handing the screen to your partner.',
      growth: 'Prioritize long-term growth',
      debt: 'Prioritize liquidity, debt, and protection',
      time: 'Blind turn',
      save: 'Save my turn and pass to',
      matches: 'See couple diagnosis and plan contrast',
      cross: 'Initial diagnosis and plan contrast',
      agree: 'Where your Top-3 overlaps',
      friction: 'Focus differences and plan tensions',
      pact: 'Route pact entering Basecamp',
      contrastTitle: 'Contrast: What worries you most vs. What impacts your plan most',
      whatWorries: 'Your #1 stated priority',
      whatImpacts: 'What moves the needle most in your numbers',
      blindSpot: 'Contrast reading',
      thermometerTitle: 'Emotional thermometer toward the plan',
      thermoGapTitle: 'Couple emotional thermometer',
      profileSplitTitle: 'Stated risk profile vs. actual portfolio',
      rankBadge: ['1st', '2nd', '3rd'],
      pickRank: 'Pick',
      top3Counter: 'Top-3 selected',
      focusBanner: 'Priority #1 focused at this node',
      blocked: 'Route deviation detected', stopped: 'Failed path analysis', impact: 'Projected consequence',
      context: 'Additional context', tensions: 'Why it happens (tensions and facts)', rewind: 'Rewind to camp',
      phase: 'Basecamp · Ascent route', route: 'One route, four camps', choose: 'Choose the step at this camp',
      ignore: 'Postpone this move and keep current exposure', confirm: 'Confirm step', doubt: 'Send question to Advisor Brief',
      trend: 'Direct impact', exact: 'See exact math', levers: 'Individual levers', none: 'No recorded levers',
      yearly: 'Yearly projection', facts: 'Facts', sources: 'Sources', concerns: 'Top-3 concerns and thermometer',
      noAnswer: 'No additional question recorded.', couple: 'Couple diagnosis and pact', questions: 'Questions for the advisor',
      noQuestions: 'No questions recorded.', discarded: 'Explored wrong decisions', noDiscarded: 'No wrong paths explored yet.',
      complete: 'Summit reached', continueExpedition: 'Back to Basecamp', repeat: 'Restart assessment',
      next: 'Review Day 0 steps or click any camp and red node on Basecamp.',
      mapAria: 'Sherpas sumi-e expedition mountain', risk: 'Route at risk',
      chart: 'Yearly projection: investable assets and net worth',
      chartAria: 'Yearly comparison of investable assets and net worth',
      blue: 'Blue: investable assets', green: 'Green: net worth',
      different: 'Different partner priority', common: 'You both share the same broad focus; review together how to sequence annual cash flow.',
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

  const thermoLabels = {
    ES: {
      1: '1 · Calma total',
      2: '2 · Tranquilo con dudas',
      3: '3 · Inquietud moderada',
      4: '4 · Alta presión',
      5: '5 · Agobio urgente'
    },
    EN: {
      1: '1 · Full calm',
      2: '2 · Mostly calm',
      3: '3 · Moderate concern',
      4: '4 · High pressure',
      5: '5 · Urgent stress'
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
      ES: { people: ['Michael'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Prioriza liquidez, cobertura paraguas y tasa de retiro sostenible.', pact: 'Ejecutar medidas prioritarias de deuda, retiro y cobertura.', events: [] },
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

  function getSpec(caseId, lang, rawData) {
    const l = lang === 'EN' ? 'EN' : 'ES';
    if (specs[caseId] && specs[caseId][l]) return specs[caseId][l];
    const owners = (((rawData || dataFor(caseId) || {}).meta || {}).owners || []).map(o => o.name).filter(Boolean);
    const people = owners.length ? owners : ['Cliente'];
    return l === 'EN'
      ? { people, blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Execute the highest-impact moves on liquidity, debt, protection, and retirement.', pact: 'Execute priority plan moves step by step.', events: [] }
      : { people, blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Ejecuta las medidas de mayor impacto en liquidez, deuda, protección y retiro.', pact: 'Ejecutar paso a paso las medidas prioritarias del plan.', events: [] };
  }

  const moveTitles = {
    'Add umbrella cover': 'Añadir cobertura paraguas de responsabilidad civil',
    'Lower the withdrawal rate': 'Reducir la tasa de retiro anual a nivel sostenible',
    'Raise growth allocation toward glide': 'Ajustar el peso en crecimiento hacia la senda objetivo',
    'Close a coverage gap': 'Cerrar la brecha de seguro patrimonial en vivienda',
    'Reduce single-name concentration': 'Reducir la concentración en una sola posición (VTI)',
    'Reduce growth allocation toward glide': 'Moderar el peso en crecimiento hacia la senda objetivo',
    'Pay down revolving card': 'Amortizar la tarjeta de crédito rotativa',
    'Add life cover': 'Ampliar la cobertura de seguro de vida',
    'Raise mortality coverage': 'Ampliar la cobertura de seguro de vida familiar',
    'Raise annual savings': 'Incrementar el ahorro anual dirigido a retiro'
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

  // Detect valid backend /api/ai/reframe topic from any concern, tension, or move text
  function detectTopic(text) {
    const s = String(text || '').toLowerCase();
    if (/home purchase|down payment|closing costs|buy a \$[\d,]+ home|compra de vivienda|entrada de/.test(s)) return 'home_purchase';
    if (/credit card|high-interest card|high-rate|apr|debt load|dti|revolving|amex|chase|tarjeta|deuda/.test(s)) return 'debt';
    if (/life insurance|mortality|umbrella|home or auto insurance|homeowners|uninsured|liability|coverage gap|seguro|paraguas|cobertura/.test(s)) return 'protection';
    if (/cash reserve|accessible cash|thin reserve|thin cash|idle cash|emergency|efectivo|colchón|reserva/.test(s)) return 'liquidity';
    if (/retir|run out of savings|savings run out|deplet|social security|withdrawal|jubilaci|retiro|agotan/.test(s)) return 'retirement';
    if (/cash flow|thin margin|free cash flow|shortfall|income dependence|paycheck|flujo de caja|margen/.test(s)) return 'cash_flow';
    if (/concentrat|equity|technology|vti|upro|tax|401\(k\)|roth|hsa|529|college|education|inversi|cartera|universidad/.test(s)) return 'investments';
    return 'overview';
  }

  // Strip all technical codes (O1..O9, T1..T5, CRITICAL/SIGNIFICANT/MODERATE/MINOR/HIGH/MEDIUM/LOW, Connected: D3, etc.)
  function stripTechnicalMarkers(raw) {
    return String(raw == null ? '' : raw)
      .replace(/^\s*-\s*/, '')
      .replace(/\*\*/g, '')
      .replace(/^(?:O\d+|T\d+)\s*(?:\((?:CRITICAL|SIGNIFICANT|MODERATE|MINOR|HIGH|MEDIUM|LOW|CRÍTICO|SIGNIFICATIVO|MODERADO|MENOR|ALTA|MEDIA|BAJA)\))?\s*(?:CRITICAL|SIGNIFICANT|MODERATE|MINOR|HIGH|MEDIUM|LOW|CRÍTICO|SIGNIFICATIVO|MODERADO|MENOR|ALTA|MEDIA|BAJA)?\s*:\s*/i, '')
      .replace(/\s*\((?:CRITICAL|SIGNIFICANT|MODERATE|MINOR|HIGH|MEDIUM|LOW|CRÍTICO|SIGNIFICATIVO|MODERADO|MENOR|ALTA|MEDIA|BAJA)\)/gi, '')
      .replace(/\b(?:CRITICAL|SIGNIFICANT|MODERATE|MINOR|CRÍTICO|SIGNIFICATIVO|MODERADO|MENOR)\s*:\s*/gi, '')
      .replace(/\s*Connected:\s*[^.]+\.?/gi, '')
      .replace(/\b(?:O\d+|D\d+[a-c]?)\s+against\s+(?:O\d+|D\d+[a-c]?)(?:\s+and\s+(?:O\d+|D\d+[a-c]?|the stated Protection anchor))?\.?\s*/gi, '')
      .replace(/\band the stated Protection anchor\.?\s*/gi, '')
      .replace(/\bD4 misalignment,?\s*/gi, '')
      .replace(/\bO\d+\s+(?:and|or|against|,)\s+O\d+(?:,?\s*together with O\d+ and O\d+,?)?(?:\s*and\s*(?:O\d+|D\d+[a-c]?))?\.?\s*/gi, '')
      .replace(/\bO\d+,\s*O\d+\s+and\s+D\d+[a-c]?\.?\s*/gi, '')
      .replace(/\bO\d+\s+against\s+current savings priorities\.?\s*/gi, '')
      .replace(/\bO\d+\s+against\s+the current saving pattern\.?\s*/gi, '')
      .replace(/\s*\((?:O\d+(?:,\s*O\d+)*|see T\d+)\)/gi, '')
      .replace(/\s*See T\d+\.?/gi, '')
      .replace(/\s{2,}/g, ' ')
      .trim();
  }

  // Split cleaned text into { title, body }
  function splitTitleAndBody(cleaned) {
    const m = cleaned.match(/^([^.!?]+)[.!?]\s*(.*)$/s);
    if (!m) return { title: cleaned, body: '' };
    return { title: m[1].trim(), body: m[2].trim() };
  }

  // Comprehensive, zero-inference English-to-Spanish humanizer preserving 100% of figures
  const esTitleMap = [
    [/^Retirement plan runs out of savings at age (\d+)$/i, 'El ahorro para el retiro se agota a los $1 años'],
    [/^Retirement shortfall$/i, 'Brecha en el ahorro para la jubilación'],
    [/^Retirement$/i, 'Ahorro y brecha para la jubilación'],
    [/^Cash for the home purchase and a thin reserve$/i, 'Efectivo ajustado ante la compra de vivienda'],
    [/^Life insurance shortfall of (\$[\d,.]+)$/i, 'Déficit de seguro de vida de $1'],
    [/^Life insurance shortfall$/i, 'Cobertura de seguro de vida insuficiente'],
    [/^Life insurance$/i, 'Brecha en seguro de vida familiar'],
    [/^No umbrella cover(?:age)?$/i, 'Sin póliza paraguas de responsabilidad civil'],
    [/^Negative cash flow$/i, 'Flujo de caja anual en negativo'],
    [/^Yearly cash flow is negative$/i, 'El flujo de caja anual es negativo'],
    [/^High-interest card$/i, 'Tarjeta de crédito de alto interés'],
    [/^High-rate credit card$/i, 'Saldo en tarjeta de crédito de alto coste'],
    [/^Debt load and the ([\d.]+%) card$/i, 'Carga de deuda y tarjeta al $1 APR'],
    [/^Unused savings room$/i, 'Margen fiscal desaprovechado en cuentas de retiro'],
    [/^Unused contribution limits$/i, 'Espacio fiscal sin utilizar en cuentas de ahorro'],
    [/^Tax-advantaged limits unused$/i, 'Cuentas con ventaja fiscal sin aprovechar'],
    [/^Tax cost on taxable holdings$/i, 'Coste fiscal anual en inversiones sujetas a impuestos'],
    [/^One employer and concentrated holdings$/i, 'Dependencia de un solo sueldo y concentración tecnológica'],
    [/^Concentration and home bias$/i, 'Concentración de cartera y sesgo hacia EE. UU.'],
    [/^Portfolio equity above target and technology concentration$/i, 'Peso en acciones sobre objetivo y concentración tecnológica'],
    [/^College funding gap$/i, 'Brecha en el fondo universitario de los hijos'],
    [/^College funding$/i, 'Ahorro universitario pendiente de cubrir'],
    [/^Education funding unfunded$/i, 'Fondo educativo universitario aún sin ahorro en 529'],
    [/^No home or auto insurance recorded$/i, 'Vivienda y vehículo sin póliza registrada en el plan'],
    [/^Thin cash after near-term goals$/i, 'Colchón líquido mínimo tras cubrir metas cercanas'],
    [/^Home purchase planned for (\d{4})$/i, 'Compra de vivienda prevista para $1'],
    [/^Idle cash$/i, 'Exceso de efectivo sin rentabilidad'],
    [/^Cash reserve$/i, 'Reserva de liquidez por debajo del objetivo'],
    [/^Income dependence$/i, 'Alta dependencia de los ingresos salariales'],
    [/^Thin margin$/i, 'Margen de flujo de caja anual estrecho'],
    [/^Retirement shortfall, college funding and negative cash flow$/i, 'Retiro, universidad y flujo negativo compiten por el mismo dinero'],
    [/^Growth portfolio against early depletion and negative cash flow$/i, 'Cartera agresiva frente a agotamiento temprano y flujo negativo'],
    [/^Cash reserve against near-term goals$/i, 'Reserva de liquidez frente a pagos cercanos']
  ];

  const esPhraseReplacements = [
    // Exact full-sentence & multi-clause patterns (preserving all numbers via capture groups)
    [/Savings run out at (\d+) against a plan to (\d+), with (\$[\d,.]+) of planned spending unpaid and a (\$[\d,.]+) gap at retirement\./gi,
      'Los ahorros se agotan a los $1 años frente a un horizonte hasta los $2, dejando $3 de gasto previsto sin cubrir y una brecha de $4 al jubilarse.'],
    [/The average draw is ([\d.]+%)\./gi, 'La tasa media de retiro es del $1.'],
    [/Cash of (\$[\d,.]+) covers about ([\d.]+) months, (\$[\d,.]+) short of the (\d+) to (\d+) month reserve\./gi,
      'El efectivo disponible de $1 cubre unos $2 meses, quedando a $3 de la reserva recomendada de $4 a $5 meses.'],
    [/Counting the January (\d{4}) goals, the target is (\$[\d,.]+) to (\$[\d,.]+), and the plan's cash covers (\d+) months after them\./gi,
      'Al sumar las metas de enero de $1, el objetivo sube a $2–$3 y el efectivo actual cubre $4 meses tras afrontarlas.'],
    [/He has (\$[\d,.]+) of whole life cover against (\$[\d,.]+) to (\$[\d,.]+) recommended\. His salary is the only income\./gi,
      'Cuenta con $1 en seguro de vida frente a los $2–$3 recomendados, siendo su sueldo la única fuente de ingresos.'],
    [/The recommended minimum is (\$[\d,.]+)\. A claim could reach (\$[\d,.]+) of liquid assets and a (\$[\d,.]+) net worth\./gi,
      'El mínimo recomendado es $1; una reclamación podría comprometer $2 en activos líquidos y $3 de patrimonio neto.'],
    [/Net cash flow is (-\$[\d,.]+) a year \((-[\d.]+%) of gross income\), even with (\$[\d,.]+) a year going to savings\./gi,
      'El flujo de caja neto es de $1 al año ($2 del ingreso bruto), incluso destinando $3 anuales al ahorro.'],
    [/The Amex Platinum balance is (\$[\d,.]+) at ([\d.]+%), with (\$[\d,.]+) paid each month\. It is small but his most expensive debt\./gi,
      'El saldo de Amex Platinum es de $1 al $2 APR con pagos de $3 al mes: un importe pequeño, pero su deuda más cara.'],
    [/He defers (\$[\d,.]+) to the 401\(k\) against a (\$[\d,.]+) limit, so (\$[\d,.]+) more is possible \(worth about (\$[\d,.]+) in tax at ([\d.]+%)\)\./gi,
      'Aporta $1 al 401(k) frente al límite de $2, dejando $3 de margen adicional (unos $4 de ahorro fiscal al tipo del $5).'],
    [/He could contribute up to (\$[\d,.]+) to a Roth IRA \(estimate\) and has put in (\$[\d,.]+)\. His HSA has (\$[\d,.]+) of a (\$[\d,.]+) limit, leaving (\$[\d,.]+)\./gi,
      'Podría aportar hasta $1 a una Roth IRA (hoy en $2) y su HSA tiene $3 sobre un límite de $4, dejando $5 libres.'],
    [/His (\$[\d,.]+) salary equals ([\d.]+%) of his net worth, and the (\$[\d,.]+) of RSUs adds to that\. Technology is his largest sector\./gi,
      'Su salario de $1 equivale al $2 de su patrimonio neto, a lo que se suman $3 en RSU con alta concentración en tecnología.'],
    [/Retirement accounts hold (\$[\d,.]+), Social Security covers only ([\d.]+%) of the (\$[\d,.]+) yearly need, and (\$[\d,.]+) of planned spending goes unpaid by the end of the plan\./gi,
      'Las cuentas de jubilación tienen $1, el Seguro Social solo cubre el $2 de los $3 necesarios al año y quedan $4 de gasto previsto sin cubrir al final del plan.'],
    [/Net worth, which includes the home, lasts until about age (\d+)\./gi,
      'El patrimonio neto, incluyendo la vivienda, resiste aproximadamente hasta los $1 años.'],
    [/She is (\$[\d,.]+) a year short after expenses and savings\./gi,
      'Presenta un déficit anual de $1 tras cubrir gastos y ahorro.'],
    [/(\$[\d,.]+) is still needed and the 529 balance is (\$[\d,.]+)\./gi,
      'Faltan $1 por cubrir para la universidad y el saldo en planes 529 es de $2.'],
    [/The plan flags the (\$[\d,.]+) home and the (\$[\d,.]+) Porsche Cayenne as uninsured, and adding homeowners cover is its top-ranked move \(score (\d+) to (\d+)\)\./gi,
      'El plan señala la vivienda de $1 y el Porsche Cayenne de $2 sin póliza registrada; asegurar la vivienda es la medida de mayor impacto inmediato (sube el score de $3 a $4).'],
    [/Her budget does include (\$[\d,.]+) a year for home insurance, so the data does not settle whether the home is covered\./gi,
      'Su presupuesto sí contempla $1 al año para seguro de hogar, por lo que conviene confirmar si la póliza ya está activa.'],
    [/Only (\$[\d,.]+) sits above the reserve once (\$[\d,.]+) of goals are set aside\./gi,
      'Solo quedan $1 por encima de la reserva mínima una vez apartados $2 para metas próximas.'],
    [/Technology is ([\d.]+%) of her stocks, US exposure is ([\d.]+%), and VTI is the largest position\. Her salary is ([\d.]+%) of net worth\./gi,
      'Tecnología pesa el $1 de sus acciones, la exposición a EE. UU. es del $2 y VTI es la mayor posición; su salario representa el $3 del patrimonio neto.'],
    [/The plan lists cutting VTI from ([\d.]+%) to ([\d.]+%) and moving from ([\d.]+%) to ([\d.]+%) growth\./gi,
      'El plan propone reducir VTI del $1 al $2 y ajustar el peso en crecimiento del $3 al $4.'],
    [/She could put up to (\$[\d,.]+) a year in an HSA \(about (\$[\d,.]+) of tax saved at her ([\d.]+%) bracket\) if her health plan qualifies, and up to (\$[\d,.]+) in a deductible traditional IRA\./gi,
      'Podría aportar hasta $1 al año a una HSA (ahorrando unos $2 en impuestos en su tramo del $3) y hasta $4 en una IRA tradicional deducible.'],
    [/She has contributed (\$[\d,.]+) to each\. Whether she has a 401\(k\) is unknown, and Roth IRA contributions are not permitted for her\./gi,
      'Hoy aporta $1 a ambas; no consta un plan 401(k) y por nivel de ingresos no puede aportar a Roth IRA.'],
    [/Tax on her investments costs about (\$[\d,.]+) a year, mostly from dividends taxed at ([\d.]+%)\./gi,
      'La factura fiscal de sus inversiones cuesta unos $1 al año, principalmente por dividendos gravados al $2.'],
    [/The bond fund JNK costs (\$[\d,.]+) and the dividend fund SCHD in the brokerage account (\$[\d,.]+)\. Missing cost basis blocks a sale-by-sale review\./gi,
      'El fondo de bonos JNK genera $1 de coste fiscal y SCHD $2 en la cuenta sujeta a impuestos; falta el coste de adquisición para evaluar ventas concretas.'],
    [/The plan assumes a (\$[\d,.]+) purchase \(about (\$[\d,.]+) by then\): a (\$[\d,.]+) down payment, (\$[\d,.]+) of closing costs and a (\$[\d,.]+) mortgage at ([\d.]+%) over (\d+) years, (\$[\d,.]+) a month\./gi,
      'El plan contempla una compra de $1 (unos $2 en esa fecha): entrada de $3, gastos de cierre de $4 y una hipoteca de $5 al $6 a $7 años ($8 al mes).'],
    [/Timothy is short (\$[\d,.]+) and Melanie (\$[\d,.]+), and both have dependents\. This is one of the two caps holding the published score down\./gi,
      'A Timothy le faltan $1 de cobertura de vida y a Melanie $2 teniendo hijos pequeños; este límite frena directamente la puntuación del plan.'],
    [/(\$[\d,.]+) at ([\d.]+%) against (\$[\d,.]+) of accessible cash\. This is the other cap on the score\./gi,
      'Mantienen $1 en tarjeta al $2 APR frente a $3 de efectivo disponible; es el segundo freno directo sobre el score.'],
    [/A (\$[\d,.]+) gap\. Against a net worth of (\$[\d,.]+) and a 90th-percentile income, a liability claim could reach well beyond current cover\./gi,
      'Brecha de $1 en responsabilidad civil: con un patrimonio neto de $2 e ingresos altos, una demanda superaría la cobertura actual.'],
    [/(\$[\d,.]+) in 529s against a (\$[\d,.]+) funding gap\./gi,
      'Tienen $1 en cuentas 529 frente a una brecha educativa proyectada de $2.'],
    [/(\$[\d,.]+) sits above the emergency reserve and near-term goals, and the cash earns about ([\d.]+%), roughly (\$[\d,.]+) a year on (\$[\d,.]+)\./gi,
      'Hay $1 ociosos por encima de la reserva y metas cercanas rindiendo apenas un $2 (unos $3 al año sobre $4).'],
    [/The near-term cash target counts only the (\$[\d,.]+) vacation, not the planned (\d{4}) vehicle and (\d{4}) home purchases\./gi,
      'El objetivo de liquidez a corto plazo solo incluye los $1 de vacaciones, sin descontar aún el vehículo de $2 ni la vivienda de $3.'],
    [/About ([\d.]+%) stocks in the long-term accounts against a ([\d.]+%) Moderate target, technology at about ([\d.]+%) of stock holdings, and a leveraged ETF \(UPRO\) at (\$[\d,.]+)\./gi,
      'Las cuentas a largo plazo tienen un $1 en acciones frente al objetivo moderado del $2, con un $3 concentrado en tecnología y $4 en el ETF apalancado 3x UPRO.'],
    [/Neither spouse has contributed to a Roth IRA \(each is estimated eligible for up to (\$[\d,.]+)\) or to a health savings account \(HSA, an (\$[\d,.]+) household limit, usable only if their health plan qualifies\)\./gi,
      'Ninguno ha aportado a Roth IRA (hasta $1 estimados por persona) ni a la cuenta de salud HSA (límite familiar de $2 si su seguro médico califica).'],
    [/Each spouse already defers part of their pay into a 401\(k\) \((\$[\d,.]+) for Timothy, (\$[\d,.]+) for Melanie\), so more 401\(k\) saving has room of (\$[\d,.]+) for Timothy and (\$[\d,.]+) for Melanie against the (\$[\d,.]+) limit\./gi,
      'Ambos aportan ya al 401(k) ($1 Timothy y $2 Melanie), dejando aún $3 y $4 de margen hasta el tope de $5.'],
    [/The plan puts the tax saving from using that room at about (\$[\d,.]+) a year\./gi,
      'Aprovechar ese margen en el 401(k) generaría unos $1 al año en ahorro fiscal.'],
    [/The gap is (\$[\d,.]+) and about (\$[\d,.]+) a year more is needed, while free cash flow is (\$[\d,.]+) a year\. Nothing goes into either 401\(k\)\./gi,
      'La brecha de jubilación es de $1 y requiere unos $2 adicionales al año, mientras que el flujo libre actual es de $3/año y hoy aportan $0 a los 401(k).'],
    [/No employer match is recorded; the plan estimates about (\$[\d,.]+) for Daniel and (\$[\d,.]+) for Emily, unconfirmed\./gi,
      'No hay aporte empresarial confirmado, aunque el plan estima unos $1 posibles para Daniel y $2 para Emily.'],
    [/Contributing the full (\$[\d,.]+) would cut tax by about (\$[\d,.]+) a year at their ([\d.]+%) marginal rate\./gi,
      'Aportar el máximo conjunto de $1 reduciría sus impuestos en unos $2 al año a su tipo marginal del $3.'],
    [/Shortfalls of (\$[\d,.]+) for Daniel and (\$[\d,.]+) for Emily\. Adding (\$[\d,.]+) of cover is worth (\d+) points of score \((\d+) to (\d+)\)\./gi,
      'Déficit de cobertura de $1 en Daniel y $2 en Emily; sumar $3 de seguro de vida eleva el score en $4 puntos (de $5 a $6).'],
    [/A (\$[\d,.]+) gap\. Adding it is worth (\d+) points \((\d+) to (\d+)\)\. With life cover, the two together lift it to (\d+)\./gi,
      'Falta una cobertura paraguas de $1; añadirla suma $2 puntos (de $3 a $4) y combinada con el seguro de vida eleva el score a $5.'],
    [/Accessible cash of (\$[\d,.]+) against a target of (\$[\d,.]+) to (\$[\d,.]+), a gap of (\$[\d,.]+)\./gi,
      'Efectivo disponible de $1 frente a un objetivo recomendado de $2 a $3 (déficit líquido de $4).'],
    [/Debt-only DTI is ([\d.]+%), monthly debt payments are (\$[\d,.]+), and the (\$[\d,.]+) card is the most expensive debt by a wide margin\./gi,
      'El ratio de deuda sobre ingresos es del $1 ($2/mes en cuotas), siendo la tarjeta de $3 la deuda más costosa con gran diferencia.'],
    [/The mortgage is (\$[\d,.]+) at ([\d.]+%) \((\$[\d,.]+) a month\), the Toyota Highlander loan (\$[\d,.]+) at ([\d.]+%) \((\$[\d,.]+)\) and Daniel's student loan (\$[\d,.]+) at ([\d.]+%) \((\$[\d,.]+)\)\./gi,
      'La hipoteca es de $1 al $2 ($3/mes), el préstamo del Toyota Highlander de $4 al $5 ($6/mes) y el préstamo estudiantil de Daniel de $7 al $8 ($9/mes).'],
    [/Annual salary is ([\d.]+%) of net worth, so the household relies heavily on two paychecks\. Worth keeping in view, with no action needed today\./gi,
      'El salario anual equivale al $1 del patrimonio neto, por lo que el hogar depende estrechamente de ambas nóminas.'],
    [/Free cash flow of (\$[\d,.]+) a year is ([\d.]+%) of income, small next to the needs above\. Raising annual savings alone lifts the score from (\d+) to (\d+)\./gi,
      'El flujo de caja libre de $1 al año ($2 de los ingresos) es ajustado frente a las metas pendientes; redirigirlo al ahorro sube el score de $3 a $4.'],
    [/A (\$[\d,.]+) gap remains after the (\$[\d,.]+) already in the 529, even though (\$[\d,.]+) a year goes in\./gi,
      'Persiste una brecha universitaria de $1 pese a los $2 ya acumulados en el plan 529 y los $3 que aportan cada año.'],
    // Tensions across the 4 cases
    [/The (\$[\d,.]+) down payment competes with retirement saving for the same dollars, and the plan has only (\$[\d,.]+) in cash for it\. The projection implies the purchase is paid mostly from investments, which cuts the base that has to carry retirement\./gi,
      'La entrada de $1 para la vivienda compite con el ahorro de jubilación por los mismos recursos y solo hay $2 en efectivo; financiarla vendiendo inversiones recortaría la base para el retiro.'],
    [/Closing the retirement gap would take about (\$[\d,.]+) more a year, while cash flow is already (-\$[\d,.]+) a year\. Both claim the same dollars\./gi,
      'Cerrar la brecha de jubilación exigiría ahorrar unos $1 más al año, mientras que el flujo de caja ya es negativo en $2 anuales.'],
    [/Closing the insurance gaps adds premiums while cash flow is negative and cash is thin\./gi,
      'Cubrir las brechas de seguro añade primas en un momento en que el flujo de caja es negativo y la liquidez es ajustada.'],
    [/A Growth profile suits a 20-year retirement horizon, but money needed in January (\d{4}) is short-term money\. Rebuilding cash by (\$[\d,.]+) or more, and setting aside the down payment, competes with staying invested\./gi,
      'Un perfil de Crecimiento encaja a 20 años vista, pero el dinero para enero de $1 es de corto plazo: reconstruir la reserva en $2 y separar la entrada compite con mantener el capital invertido.'],
    [/Paying off a ([\d.]+%) card faster is a guaranteed return, but it uses cash that is already thin and competes with retirement saving\. At (\$[\d,.]+) a month it is projected paid off by July (\d{4})\./gi,
      'Liquidar la tarjeta al $1 ofrece un ahorro garantizado, aunque consume liquidez; al ritmo de $2/mes terminaría de pagarse en julio de $3.'],
    [/Her savings go to taxable and cash accounts while retirement accounts hold (\$[\d,.]+)\. The (\$[\d,.]+) college gap, the age (\d+) depletion and the (\$[\d,.]+) yearly shortfall compete for the same dollars, and the (\d{4}) home purchase adds another call on cash\. Urgency is high because college payments are under way\./gi,
      'Su ahorro va a cuentas imponibles y efectivo mientras las cuentas de retiro están en $1. La brecha universitaria de $2, el agotamiento a los $3 años y el déficit anual de $4 compiten con la vivienda prevista en $5 justo cuando ya empiezan los pagos universitarios.'],
    [/Stated and actual risk are both aggressive, yet the plan runs out at (\d+) and cash flow is negative\. A market drop would hit a household with a ([\d.]+%) starting draw and a thin cushion\./gi,
      'Tanto el perfil declarado como la cartera son agresivos, pero el ahorro se agota a los $1 años con flujo negativo: una caída bursátil golpearía un retiro que parte con una extracción del $2 anual.'],
    [/Only (\$[\d,.]+) sits above the reserve after (\$[\d,.]+) of goals, and the (\$[\d,.]+) yearly shortfall would erode it\./gi,
      'Solo quedan $1 sobre la reserva tras apartar $2 de metas cercanas, y el déficit anual de $3 iría erosionando ese margen.'],
    [/Large idle cash coexists with (\$[\d,.]+) of combined life insurance shortfall and no umbrella\. Resources exist to close part of the gap, but the cash is sitting unused\. The published score is held at (\d+), while the plan models (\d+) with a card paydown and more life cover, and (\d+) if an umbrella policy is added too\./gi,
      'Un gran saldo de efectivo ocioso convive con un déficit combinado de $1 en seguro de vida y sin póliza paraguas. Hay liquidez de sobra para resolverlo: el score actual de $2 sube a $3 al pagar la tarjeta y ampliar seguro de vida, y alcanza $4 añadiendo la póliza paraguas.'],
    [/D4 misalignment,?\s*The spouses' stated profiles \(Growth and Moderate\) differ, while the invested book is about ([\d.]+%) stocks\. Revealed risk is higher than the Moderate household reading\./gi,
      'Sus perfiles declarados difieren (Crecimiento frente a Moderado), mientras la cartera invertida alcanza un $1 en acciones, por encima del nivel moderado del hogar.'],
    [/An ([\d.]+%) card balance is carried while accessible cash far exceeds the reserve\. The card costs about (\$[\d,.]+) a year in interest \(([\d.]+%) of (\$[\d,.]+)\), against roughly (\$[\d,.]+) a year earned on the cash\./gi,
      'Se arrastra una tarjeta al $1 APR mientras el efectivo supera ampliamente la reserva: la tarjeta cuesta unos $2 al año en intereses ($3 de $4) frente a solo $5 anuales que rinde el efectivo.'],
    [/O4 against current savings priorities\.\s*/gi, ''],
    [/The (\$[\d,.]+) yearly education need competes with 401\(k\), Roth and HSA contributions for the same cash flow, which is itself reported as uncertain\./gi,
      'Los $1 anuales requeridos para educación compiten con las aportaciones al 401(k), Roth y HSA por el mismo flujo de caja.'],
    [/compete for the same (\$[\d,.]+) of yearly free cash flow\. Retirement needs about (\$[\d,.]+) a year and the cash gap is (\$[\d,.]+)\. They must weigh the trade-off together\./gi,
      'Jubilación, reserva líquida y seguros compiten por los mismos $1 de flujo de caja libre anual: el retiro necesita unos $2/año y a la reserva le faltan $3, por lo que deben priorizar en pareja.'],
    [/O2, O3 and D4c\.\s*/gi, ''],
    [/The protection gaps stay open while the household carries high exposure and a thin cushion, and closing them costs cash flow that O1 and O4 also need\./gi,
      'Las brechas de protección siguen abiertas mientras el hogar mantiene un colchón líquido estrecho, y cubrirlas requiere parte del flujo que también necesitan la reserva y el retiro.'],
    [/They state a Moderate orientation and hold a moderate portfolio, but their overall exposure is closer to aggressive, which suggests drift\. Any plan also has to work for both a Growth and a Moderate partner\./gi,
      'Declaran una orientación moderada en cartera, pero su baja liquidez y falta de seguros los expone a un riesgo real elevado; además, el plan debe equilibrar el perfil de Crecimiento de él con el Moderado de ella.'],
    [/O5 against the current saving pattern\.\s*/gi, ''],
    [/The household saves (\$[\d,.]+) a year \((\$[\d,.]+) to brokerage, (\$[\d,.]+) to the 529 and (\$[\d,.]+) to cash\) while carrying an (\$[\d,.]+) balance at ([\d.]+%) and sending (\$[\d,.]+) to the 401\(k\)s\./gi,
      'El hogar ahorra $1 al año ($2 a corretaje, $3 al plan 529 y $4 a efectivo) mientras arrastra $5 en tarjeta al $6 APR y aporta $7 a los planes 401(k).'],
    [/The 529 receives (\$[\d,.]+) a year while retirement receives nothing, though retirement is the larger gap\./gi,
      'El plan universitario 529 recibe $1 al año mientras que la jubilación no recibe aportaciones, pese a ser la brecha financiera mayor.'],
    // Top moves actions & notes
    [/Add (\$[\d,.]+[MK]?) of umbrella to raise the liability shield/gi,
      'Añadir $1 de póliza paraguas para blindar el patrimonio ante responsabilidad civil'],
    [/Cutting withdrawals to (\$[\d,.]+)\/year \(([\d.]+%)\) reaches the sustainable band/gi,
      'Reducir los retiros anuales a $1/año ($2) para situar el flujo en zona sostenible'],
    [/Move the invested mix from ([\d.]+%) to ([\d.]+%) growth \(glide ([\d.]+%)\) for the next horizon-fit band — about (\$[\d,.]+) of the invested book/gi,
      'Ajustar la cartera del $1 al $2 en crecimiento (senda objetivo $3) — movilizando unos $4 de la cartera'],
    [/Add homeowners insurance on Primary home so coverage integrity clears that gap/gi,
      'Activar la póliza de seguro de hogar sobre la vivienda principal para cerrar la brecha patrimonial'],
    [/Bring VTI from ([\d.]+%) to ([\d.]+%) of investable for the next concentration band — about (\$[\d,.]+) of that line/gi,
      'Reducir el peso de VTI del $1 al $2 de los activos invertibles — reasignando unos $3'],
    [/Pay (\$[\d,.]+) on the ([\d.]+%) card from cash to remove high revolving exposure and clear the gate/gi,
      'Amortizar $1 de la tarjeta al $2 APR usando efectivo disponible para levantar el freno del score'],
    [/Add (\$[\d,.]+) of life cover to raise the mortality ratio and clear the gate/gi,
      'Añadir $1 de seguro de vida para cubrir el umbral familiar y desbloquear la puntuación'],
    [/Add (\$[\d,.]+) of life cover to reach the next mortality-coverage anchor/gi,
      'Añadir $1 de seguro de vida para alcanzar el siguiente nivel de protección familiar'],
    [/Redirect (\$[\d,.]+)\/year of free cash flow into savings to raise retirement-directed savings toward the next band/gi,
      'Redirigir los $1/año de flujo de caja libre hacia ahorro de jubilación para subir al siguiente tramo'],
    [/After the card paydown, life cover must reach (\$[\d,.]+) to keep the mortality ratio at the gate line\./gi,
      'Tras rebajar la tarjeta, la cobertura de vida debe situarse en $1 para superar ambos límites del score.'],
    [/Together they raise the published score more than either move alone\./gi,
      'Ejecutadas en conjunto elevan la puntuación del plan más que cada medida por separado.'],
    // Transition alerts & subjective concerns & D6/D4
    [/Home purchase in January (\d{4}) \(within 12 months\)\.\s*Michael plans to buy a (\$[\d,.]+) home \((\$[\d,.]+) at purchase\) with a (\$[\d,.]+) down payment and a (\d+)-year loan of (\$[\d,.]+) at ([\d.]+%)\.\s*The monthly payment is (\$[\d,.]+),?[^.]*\./gi,
      'Compra de vivienda en enero de $1 (en menos de 12 meses): planea adquirir una casa de $2 ($3 al cierre) con $4 de entrada y una hipoteca a $5 años de $6 al $7 ($8/mes).'],
    [/None detected(?: within 12 to 24 months)?\./gi, 'Sin cambios bruscos de etapa en los próximos 12–24 meses.'],
    [/None recorded\./gi, 'Sin preocupaciones previas registradas en entrevista.'],
    [/The nearest events are the (\$[\d,.]+) vacation in January (\d{4}), college in August (\d{4}) and August (\d{4}), and retirement in (\d{4})\./gi,
      'Los hitos más cercanos son las vacaciones de $1 en enero de $2, el inicio universitario en agosto de $3 y agosto de $4, y la jubilación en $5.'],
    [/The nearest shifts are the planned vehicle purchase in (\d{4}), the planned home purchase in (\d{4}), college starts in (\d{4}) and (\d{4}), and retirement (\d+) years out\./gi,
      'Los próximos hitos son la compra de vehículo en $1, la compra de vivienda en $2, la universidad en $3 y $4, y la jubilación a $5 años vista.'],
    [/Ethan's August (\d{4}) payment, Ava's August (\d{4}) start and a January (\d{4}) vacation will press on her cash, but change no label within 12 to 24 months\. The home purchase is in (\d{4})\./gi,
      'El pago universitario de Ethan en agosto de $1, el inicio de Ava en agosto de $2 y las vacaciones de enero de $3 exigirán liquidez, con la compra de vivienda prevista para $4.']
  ];

  // Generic clause-level fallback translator for any future unseen JSON sentence
  const genericWordReplacements = [
    [/\bRetirement shortfall\b/gi, 'Déficit para la jubilación'],
    [/\bretirement accounts\b/gi, 'cuentas de jubilación'],
    [/\bretirement gap\b/gi, 'brecha de jubilación'],
    [/\bretirement saving(?:s)?\b/gi, 'ahorro para el retiro'],
    [/\binvestable assets\b/gi, 'activos invertibles'],
    [/\bnet worth\b/gi, 'patrimonio neto'],
    [/\bfree cash flow\b/gi, 'flujo de caja libre'],
    [/\bnet cash flow\b/gi, 'flujo de caja neto'],
    [/\bcash flow\b/gi, 'flujo de caja'],
    [/\baccessible cash\b/gi, 'efectivo disponible'],
    [/\bemergency reserve\b/gi, 'reserva de emergencia'],
    [/\blife insurance\b/gi, 'seguro de vida'],
    [/\blife cover\b/gi, 'cobertura de vida'],
    [/\bumbrella cover(?:age)?\b/gi, 'cobertura paraguas'],
    [/\bumbrella policy\b/gi, 'póliza paraguas'],
    [/\bdown payment\b/gi, 'entrada inicial'],
    [/\bhome purchase\b/gi, 'compra de vivienda'],
    [/\bmortgage\b/gi, 'hipoteca'],
    [/\bcredit card\b/gi, 'tarjeta de crédito'],
    [/\bhigh-interest\b/gi, 'alto interés'],
    [/\bshortfall\b/gi, 'déficit'],
    [/\bgap\b/gi, 'brecha'],
    [/\bmonths\b/gi, 'meses'],
    [/\ba year\b/gi, 'al año'],
    [/\ba month\b/gi, 'al mes'],
    [/\bage (\d+)\b/gi, 'los $1 años'],
    [/\bscore\b/gi, 'puntuación'],
    [/\bhousehold\b/gi, 'hogar'],
    [/\bspouses\b/gi, 'cónyuges']
  ];

  function translateTitleToES(title) {
    let out = stripTechnicalMarkers(title).replace(/\.$/, '');
    for (const [rx, rep] of esTitleMap) {
      if (rx.test(out)) return out.replace(rx, rep);
    }
    for (const [rx, rep] of esPhraseReplacements) {
      out = out.replace(rx, rep);
    }
    for (const [rx, rep] of genericWordReplacements) {
      out = out.replace(rx, rep);
    }
    return out;
  }

  function translateBodyToES(body) {
    let out = stripTechnicalMarkers(body);
    if (!out) return '';
    for (const [rx, rep] of esPhraseReplacements) {
      out = out.replace(rx, rep);
    }
    // Clean any remaining raw English phrases in generic future JSONs
    if (/\b(?:The|His|Her|They|There is|There are|Against|Counting)\b/.test(out)) {
      for (const [rx, rep] of genericWordReplacements) {
        out = out.replace(rx, rep);
      }
    }
    return out.replace(/\s{2,}/g, ' ').trim();
  }

  function humanizeConcernObject(item, lang) {
    const rawDetail = String((item && item.detail) || '');
    const cleaned = stripTechnicalMarkers(rawDetail);
    const { title: rawTitle, body: rawBody } = splitTitleAndBody(cleaned);
    const topic = detectTopic(cleaned);
    if (lang === 'EN') {
      const title = rawTitle || 'Plan priority';
      const body = rawBody || cleaned;
      return Object.assign({}, item, {
        topic,
        title,
        body,
        detail: body ? `**${title}.** ${body}` : `**${title}.**`
      });
    }
    const titleES = translateTitleToES(rawTitle || cleaned);
    const bodyES = translateBodyToES(rawBody);
    return Object.assign({}, item, {
      topic,
      title: titleES,
      body: bodyES,
      detail: bodyES ? `**${titleES}.** ${bodyES}` : `**${titleES}.**`
    });
  }

  function humanizeTensionObject(item, lang) {
    const rawDetail = String((item && item.detail) || '');
    const cleaned = stripTechnicalMarkers(rawDetail);
    const { title: rawTitle, body: rawBody } = splitTitleAndBody(cleaned);
    const hasTitle = rawBody && rawTitle.length < 75 && !/\$/.test(rawTitle);
    const topic = detectTopic(cleaned);
    if (lang === 'EN') {
      const title = hasTitle ? rawTitle : '';
      const body = hasTitle ? rawBody : cleaned;
      return Object.assign({}, item, {
        topic,
        title,
        body,
        detail: title ? `**${title}.** ${body}` : body
      });
    }
    const titleES = hasTitle ? translateTitleToES(rawTitle) : '';
    const bodyES = translateBodyToES(hasTitle ? rawBody : cleaned);
    return Object.assign({}, item, {
      topic,
      title: titleES,
      body: bodyES,
      detail: titleES ? `**${titleES}.** ${bodyES}` : bodyES
    });
  }

  function humanizePersonaD4(rawD4, lang, rawData) {
    const owners = (((rawData || {}).meta || {}).owners || []);
    const text = String(rawD4 || '');
    const stocksMatch = text.match(/([\d.]+%)\s*(?:is in\s+)?stocks/i);
    const stocksPct = stocksMatch ? stocksMatch[1] : null;
    const targetMatch = text.match(/target(?:\s+mix)?\s+is\s+(?:about\s+)?([\d.]+%)/i) || text.match(/against\s+an?\s+([\d.]+%)\s*(?:Growth|Moderate)?\s*target/i);
    const targetPct = targetMatch ? targetMatch[1] : null;
    const uproMatch = text.match(/UPRO[^.]*(\$[\d,.]+)/i);
    if (owners.length >= 2) {
      const a = owners[0], b = owners[1];
      const profES = { Growth: 'Crecimiento', Moderate: 'Moderado', Aggressive: 'Agresivo', Conservative: 'Conservador' };
      if (lang === 'ES') {
        const splitText = `${a.name} declara perfil ${profES[a.risk_profile] || a.risk_profile || 'Crecimiento'} y ${b.name} perfil ${profES[b.risk_profile] || b.risk_profile || 'Moderado'}.`;
        const mixText = stocksPct ? ` En la práctica, la cartera mantiene un ${stocksPct} en acciones${targetPct ? ` (frente al ${targetPct} objetivo)` : ''}${uproMatch ? `, incluyendo ${uproMatch[1]} en el ETF apalancado 3x UPRO` : ''}.` : '';
        return splitText + mixText;
      }
      const splitEN = `${a.name} states a ${a.risk_profile || 'Growth'} profile while ${b.name} states ${b.risk_profile || 'Moderate'}.`;
      const mixEN = stocksPct ? ` In practice, the invested portfolio holds ${stocksPct} in stocks${targetPct ? ` (against a ${targetPct} target)` : ''}${uproMatch ? `, including ${uproMatch[1]} in 3x leveraged UPRO` : ''}.` : '';
      return splitEN + mixEN;
    }
    const single = owners[0] || { name: 'Cliente', risk_profile: 'Growth' };
    if (lang === 'ES') {
      return `${single.name} declara un perfil de riesgo de ${single.risk_profile === 'Growth' ? 'Crecimiento' : single.risk_profile}${stocksPct ? `, con un ${stocksPct} de la cartera a largo plazo invertido en acciones` : ''}${targetPct ? ` frente al ${targetPct} objetivo` : ''}.`;
    }
    return `${single.name} states a ${single.risk_profile || 'Growth'} risk profile${stocksPct ? `, holding ${stocksPct} in stocks across long-term accounts` : ''}${targetPct ? ` against an ${targetPct} target` : ''}.`;
  }

  function humanizePersonaD6(rawD6, lang, rawData) {
    const s = String(rawD6 || '');
    const isCouple = !!(((rawData || {}).meta || {}).isCouple);
    if (lang === 'EN') {
      if (/FREEDOM/i.test(s)) return 'Financial independence and early retirement flexibility, supported by a high savings rate and planned annual travel.';
      if (/DUTY/i.test(s)) return 'Family stewardship: funding college goals and keeping strong protection in place for the children.';
      if (/PROTECTION/i.test(s)) return isCouple ? 'Family protection: safeguarding two incomes and the children while closing open insurance and liquidity gaps.' : 'Household security and downside protection.';
      return stripTechnicalMarkers(s);
    }
    if (/FREEDOM/i.test(s)) return 'Libertad financiera y retiro temprano, respaldados por una alta tasa de ahorro y metas de viaje anual.';
    if (/DUTY/i.test(s)) return 'Responsabilidad familiar: financiar la universidad de los hijos y mantener su protección asegurada.';
    if (/PROTECTION/i.test(s)) return isCouple ? 'Protección familiar: resguardar ambos ingresos y el futuro de los hijos cerrando las brechas de seguro y liquidez.' : 'Seguridad patrimonial y protección ante imprevistos.';
    return translateBodyToES(s);
  }

  function humanizeShockDescription(desc, idx, lang) {
    if (lang === 'EN') return String(desc || '');
    const esShocks = [
      'La Fed subió los tipos 25 pb hasta el 5.25–5.50%, la undécima y última subida del ciclo (su nivel más alto en 22 años), manteniéndolos 14 meses antes de recortar en septiembre de 2024.',
      'La Fed mantuvo tipos pero su gráfico de puntos anticipó 75 pb de recortes para 2024. El S&P 500 marcó nuevos máximos y el Russell 2000 subió un 4% con caída de rentabilidades a largo plazo.',
      'El desarme del carry trade del yen y el temor a recesión en EE. UU. provocaron una caída global: el TOPIX japonés cayó un 12.3%, el VIX superó 65 intradía y el S&P 500 abrió con -3% antes de recuperar casi todo en la semana.',
      'Primer recorte de tipos de la Fed en cuatro años (-50 pb), abriendo formalmente el ciclo de bajadas al confirmar que la inflación convergía hacia el 2%.',
      'Victoria electoral de Trump: el S&P 500 subió un 2.5%, el Dow un 3.6% y el Russell 2000 un 5.8%, impulsando banca y pequeña capitalización mientras el dólar se fortalecía.',
      'La startup china DeepSeek lanzó un modelo de IA abierto competitivo a una fracción de coste: Nvidia perdió $589B de capitalización en un día, el Nasdaq cayó un 3.1% y el S&P 500 un 1.5%.',
      'Anuncio de aranceles recíprocos generales (10% base, 34% China, 20% UE, 46% Vietnam): el S&P 500 cayó un 10% en dos días ($6.6T evaporados) y repuntaron los rendimientos de los bonos.',
      'Tras caer el S&P 500 un 10% en dos días, se anunció una pausa arancelaria de 90 días (excepto China al 125%): el S&P 500 rebotó un 9.52% en una sola sesión y el Nasdaq un 12.16%, con récord de 30B de acciones negociadas.',
      'Tregua arancelaria EE. UU.-China en Ginebra reduciendo aranceles del 125% al 10% durante 90 días: el S&P 500 subió un 3.3% y el Nasdaq un 4.4% liderados por tecnología y consumo.',
      'El Tribunal Supremo anuló el uso de poderes de emergencia para imponer los aranceles recíprocos de abril de 2025, desmontando su base legal.',
      'Operación Furia Épica (ataques conjuntos de EE. UU. e Israel contra instalaciones en Irán, casi 900 ataques en 12 horas): el crudo Brent saltó un 10–13% y las bolsas globales corrigieron por riesgo energético.'
    ];
    return esShocks[idx] || translateBodyToES(desc);
  }

  function localizeData(data, lang) {
    if (!data) return data;
    const l = lang === 'EN' ? 'EN' : 'ES';
    const score = data.score || {}, persona = data.persona || {};
    const concerns = (persona.objectiveConcerns || []).map(x => humanizeConcernObject(x, l));
    const tensions = (persona.tensions || []).map(x => humanizeTensionObject(x, l));

    if (l === 'EN') {
      return Object.assign({}, data, {
        score: Object.assign({}, score, {
          top_moves: (score.top_moves || []).map(m => Object.assign({}, m, {
            topic: detectTopic((m.title || '') + ' ' + (m.action || ''))
          }))
        }),
        persona: Object.assign({}, persona, {
          D4Human: humanizePersonaD4(persona.D4, 'EN', data),
          D6: humanizePersonaD6(persona.D6, 'EN', data),
          subjectiveConcerns: /None (?:detected|recorded)/i.test(String(persona.subjectiveConcerns || ''))
            ? 'No prior interview notes recorded yet.'
            : stripTechnicalMarkers(persona.subjectiveConcerns),
          transitionAlerts: stripTechnicalMarkers(persona.transitionAlerts),
          objectiveConcerns: concerns,
          tensions
        })
      });
    }

    return Object.assign({}, data, {
      score: Object.assign({}, score, {
        pillars: (score.pillars || []).map(p => Object.assign({}, p, {
          pillar: { 'Savings and cash flow': 'Ahorro y flujo de caja', Debt: 'Deuda', Investments: 'Inversiones', 'Liquidity and emergency fund': 'Liquidez y fondo de emergencia', 'Insurance and protection': 'Seguros y protección' }[p.pillar] || p.pillar
        })),
        top_moves: (score.top_moves || []).map((m, i) => Object.assign({}, m, {
          topic: detectTopic((m.title || '') + ' ' + (m.action || '')),
          title: moveTitles[m.title] || translateTitleToES(m.title || `Medida prioritaria ${i + 1}`),
          action: translateBodyToES(m.action || m.title || ''),
          note: translateBodyToES(m.note || '')
        })),
        combined_moves: (score.combined_moves || []).map((m, i) => {
          const translatedMoves = (m.moves || []).map((x, j) => moveTitles[x] || translateTitleToES(x || `Medida ${j + 1}`));
          return Object.assign({}, m, {
            title: translatedMoves.join(' + ') || `Medidas combinadas ${i + 1}`,
            action: translateBodyToES(m.action || translatedMoves.join(' + ')),
            moves: translatedMoves,
            note: translateBodyToES(m.note || '')
          });
        }),
        message: translateBodyToES(score.message || ''),
        explainer: translateBodyToES(score.explainer || '')
      }),
      persona: Object.assign({}, persona, {
        D4Human: humanizePersonaD4(persona.D4, 'ES', data),
        D6: humanizePersonaD6(persona.D6, 'ES', data),
        D3: translateBodyToES(persona.D3 || ''),
        subjectiveConcerns: /None (?:detected|recorded)/i.test(String(persona.subjectiveConcerns || ''))
          ? 'Sin notas de entrevista previas registradas en el expediente.'
          : translateBodyToES(persona.subjectiveConcerns),
        transitionAlerts: translateBodyToES(persona.transitionAlerts || ''),
        objectiveConcerns: concerns,
        tensions
      }),
      savingsWaterfall: (data.savingsWaterfall || []).map(x => Object.assign({}, x, {
        bucket: buckets[x.bucket] || x.bucket,
        status: { Filled: 'Cubierto', 'Partially filled': 'Parcialmente cubierto', Empty: 'Pendiente' }[x.status] || x.status
      })),
      shocks: (data.shocks || []).map((x, i) => Object.assign({}, x, {
        name: shockNames[i] || translateTitleToES(x.name || 'Evento histórico'),
        portfolioImpact: { Mixed: 'Mixto', Negative: 'Negativo', Positive: 'Positivo', 'Rates-driven': 'Tipos de interés' }[x.portfolioImpact] || x.portfolioImpact,
        description: humanizeShockDescription(x.description, i, 'ES')
      }))
    });
  }

  // Render clean human HTML for any concern or tension without O1/T1 or SIGNIFICATIVO prefixes
  const detail = (id, value, lang) => {
    if (value && typeof value === 'object') {
      const title = esc(value.title || '');
      const body = esc(value.body || '');
      return title && body ? `<strong>${title}.</strong> ${body}` : (title ? `<strong>${title}</strong>` : body);
    }
    const item = humanizeConcernObject({ id, detail: value }, lang === 'EN' ? 'EN' : 'ES');
    return item.body ? `<strong>${esc(item.title)}.</strong> ${esc(item.body)}` : `<strong>${esc(item.title)}</strong>`;
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

  // Active Top-3 concern IDs for current user or current partner turn
  function activeTop3(state) {
    const raw = dataFor(state && state.caseId) || {};
    const isCouple = !!(raw.meta && raw.meta.isCouple);
    if (isCouple && state.phase === 'fears') {
      const turn = state.voteTurn === 'B' ? 'B' : 'A';
      const turnVotes = (state.votes && state.votes[turn]) || {};
      return Array.isArray(turnVotes.fears) ? turnVotes.fears.slice(0, 3) : [];
    }
    return Array.isArray(state && state.fearOrder) ? state.fearOrder.slice(0, 3) : [];
  }

  // Active emotional thermometer (1..5)
  function activeThermometer(state) {
    const raw = dataFor(state && state.caseId) || {};
    const isCouple = !!(raw.meta && raw.meta.isCouple);
    if (isCouple && state.phase === 'fears') {
      const turn = state.voteTurn === 'B' ? 'B' : 'A';
      const turnVotes = (state.votes && state.votes[turn]) || {};
      const val = Number(turnVotes.thermometer);
      return Number.isFinite(val) && val >= 1 && val <= 5 ? val : 3;
    }
    const val = Number(state && state.thermometer);
    return Number.isFinite(val) && val >= 1 && val <= 5 ? val : 3;
  }

  // Find the user's #1 prioritized concern object (or default to first objectiveConcern)
  function primaryConcern(state, localizedData) {
    const concerns = ((localizedData && localizedData.persona && localizedData.persona.objectiveConcerns) || []);
    if (!concerns.length) return null;
    const topId = (state && state.fearOrder && state.fearOrder[0])
      || (state && state.votes && state.votes.A && state.votes.A.fears && state.votes.A.fears[0])
      || concerns[0].id;
    return concerns.find(c => c.id === topId) || concerns[0];
  }

  // Order top_moves so the move matching the user's #1 concern topic is prioritized at Campamento Base (stage 0)
  function orderedTopMoves(state, data) {
    const moves = ((data && data.score && data.score.top_moves) || []).slice();
    if (moves.length <= 1) return moves;
    const firstConcern = primaryConcern(state, data);
    if (!firstConcern) return moves;
    const targetTopic = firstConcern.topic || detectTopic(firstConcern.detail);
    const topicCompat = {
      protection: ['protection'],
      debt: ['debt', 'cash_flow'],
      liquidity: ['liquidity', 'cash_flow', 'debt'],
      home_purchase: ['liquidity', 'cash_flow', 'investments'],
      retirement: ['cash_flow', 'retirement', 'investments'],
      cash_flow: ['cash_flow', 'debt', 'liquidity'],
      investments: ['investments', 'retirement']
    }[targetTopic] || [targetTopic];

    let bestIdx = -1;
    for (const tp of topicCompat) {
      bestIdx = moves.findIndex(m => (m.topic || detectTopic((m.title || '') + ' ' + (m.action || ''))) === tp);
      if (bestIdx >= 0) break;
    }
    if (bestIdx > 0) {
      const chosen = moves.splice(bestIdx, 1)[0];
      moves.unshift(chosen);
    }
    return moves;
  }

  // Build Contrast ("Lo que más te preocupa vs. Lo que más impacta tu plan") with 100% literal JSON figures
  function buildContrastSummary(state, data) {
    const lang = langOf(state);
    const es = lang === 'ES';
    const concerns = (data.persona && data.persona.objectiveConcerns) || [];
    const top1 = primaryConcern(state, data) || concerns[0] || { id: 'O1', title: es ? 'Prioridad del plan' : 'Plan priority', body: '', topic: 'overview' };
    const rawMoves = ((data.score && data.score.top_moves) || []).slice();
    const scoreNow = (data.score && data.score.published_score) ?? 0;
    const bestSingle = rawMoves.reduce((best, m) => {
      const gain = (Number(m.score_after) || scoreNow) - (Number(m.score_before) || scoreNow);
      const bestGain = (Number(best && best.score_after) || scoreNow) - (Number(best && best.score_before) || scoreNow);
      return !best || gain > bestGain ? m : best;
    }, rawMoves[0] || null);
    const combined = ((data.score && data.score.combined_moves) || []);
    const bestCombined = combined.reduce((best, m) => (!best || (Number(m.score_after) || 0) > (Number(best.score_after) || 0) ? m : best), combined[0] || null);
    const rec = riskRecord(state.caseId, lang);

    const bestMoveTitle = bestSingle ? (bestSingle.title || bestSingle.action) : (es ? 'Medida principal del plan' : 'Primary plan move');
    const bestMoveAction = bestSingle ? (bestSingle.action || bestSingle.title) : '';
    const singleDelta = bestSingle ? `${bestSingle.score_before ?? scoreNow} → ${bestSingle.score_after ?? scoreNow}` : `${scoreNow}`;
    const comboLabel = bestCombined ? (bestCombined.title || (bestCombined.moves || []).join(' + ') || (es ? 'medidas combinadas' : 'combined moves')) : '';
    const comboNote = bestCombined && bestCombined.score_after
      ? (es ? ` (y hasta ${bestCombined.score_after}/100 combinando ${comboLabel})` : ` (and up to ${bestCombined.score_after}/100 combining ${comboLabel})`)
      : '';
    const exhaustionNote = rec.hasExhaustion
      ? (es ? ` Además, la proyección anual marca agotamiento de activos invertibles en ${rec.year}${rec.age != null ? ` (edad ${rec.age})` : ''} con ${exactMoney(rec.investable_assets)}.`
            : ` In addition, the yearly projection flags investable-asset depletion in ${rec.year}${rec.age != null ? ` (age ${rec.age})` : ''} at ${exactMoney(rec.investable_assets)}.`)
      : '';

    const top1Topic = top1.topic || detectTopic(top1.detail);
    const bestTopic = bestSingle ? (bestSingle.topic || detectTopic((bestSingle.title || '') + ' ' + (bestSingle.action || ''))) : 'overview';
    const aligned = top1Topic === bestTopic || (top1Topic === 'retirement' && bestTopic === 'cash_flow');

    const worryText = `${top1.title}${top1.body ? ` — ${top1.body}` : ''}`;
    const impactText = `${bestMoveTitle}: ${bestMoveAction} (Score ${singleDelta})${comboNote}.${exhaustionNote}`;
    const blindSpotText = aligned
      ? (es
          ? `Tu intuición da en el blanco: tu preocupación #1 coincide con la palanca cuantitativa clave del plan. Empezaremos el Basecamp atacando directamente este frente.`
          : `Your intuition is spot-on: your #1 concern aligns with the plan's primary quantitative lever. We will start Basecamp by tackling this front directly.`)
      : (es
          ? `Contraste clave: lo que más te inquieta hoy es «${top1.title}», mientras que en los números del plan el mayor salto de puntuación (${singleDelta}${comboNote}) exige actuar también sobre «${bestMoveTitle}». En el Basecamp conectaremos tu prioridad #1 en el primer nodo sin descuidar este punto ciego.`
          : `Key contrast: what worries you most today is "${top1.title}", whereas the largest score jump in the numbers (${singleDelta}${comboNote}) also requires acting on "${bestMoveTitle}". In Basecamp we will address your #1 priority at the first node while closing this blind spot.`);

    return { top1, bestSingle, bestCombined, aligned, worryText, impactText, blindSpotText, topic: top1Topic };
  }

  // Adapt narrative reframe to the emotional thermometer (1..5) and #1 priority
  function buildThermometerReframe(state, data) {
    const lang = langOf(state);
    const es = lang === 'ES';
    const level = activeThermometer(state);
    const contrast = buildContrastSummary(state, data);
    const top1 = contrast.top1;
    const score = (data.score && data.score.published_score) ?? 0;

    if (state.aiReframe && state.aiReframe.lang === lang && state.aiReframe.text) {
      return state.aiReframe.text;
    }

    if (es) {
      if (level >= 4) {
        return `Termómetro ${level}/5 (alta presión): Respira; no tienes que resolver todo el plan hoy. Con un score actual de ${score}/100, vamos a empezar paso a paso por lo que más te pesa («${top1.title}») con una sola acción concreta y medible en el Campamento Base.`;
      }
      if (level <= 2) {
        return `Termómetro ${level}/5 (calma estratégica): Aprovechemos tu tranquilidad para optimizar el plan (score actual ${score}/100). Tu prioridad #1 («${top1.title}») abre el recorrido en el Campamento Base antes de capturar los puntos de mayor retorno cuantitativo.`;
      }
      return `Termómetro ${level}/5 (enfoque equilibrado): Partimos de un score de ${score}/100. Hemos colocado tu prioridad #1 («${top1.title}») como foco de arranque en el Campamento Base para ordenar liquidez, riesgo y retiro sin fricción.`;
    }
    if (level >= 4) {
      return `Thermometer ${level}/5 (high pressure): Take a breath—you don't need to fix the entire plan at once. Starting from a ${score}/100 score, we will begin at Basecamp with one clear, concrete step addressing "${top1.title}".`;
    }
    if (level <= 2) {
      return `Thermometer ${level}/5 (strategic calm): Let's use your calm perspective to fine-tune the plan (current score ${score}/100). Your #1 priority ("${top1.title}") leads the first Basecamp node before locking in the highest-return score levers.`;
    }
    return `Thermometer ${level}/5 (balanced focus): Starting from a ${score}/100 score, we placed your #1 priority ("${top1.title}") at the opening Basecamp node so liquidity, protection, and long-term growth move in sync.`;
  }

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
    const lang = langOf(state);
    const es = lang === 'ES';
    const moves = orderedTopMoves(state, data);
    const tensions = ((data && data.persona && data.persona.tensions) || []);
    const top1 = primaryConcern(state, data);
    if (stageIdx < moves.length && moves[stageIdx]) {
      const m = moves[stageIdx];
      const relatedTension = tensions.find(tn => tn.topic === m.topic) || tensions[stageIdx] || tensions[0];
      const badOption = relatedTension
        ? (es
            ? `Dejar sin resolver: ${relatedTension.title || relatedTension.body.slice(0, 110)}`
            : `Leave unresolved: ${relatedTension.title || relatedTension.body.slice(0, 110)}`)
        : (es
            ? `Posponer «${m.title}» y mantener el score estancado en ${m.score_before ?? (data.score && data.score.published_score)}`
            : `Postpone "${m.title}" and leave the score at ${m.score_before ?? (data.score && data.score.published_score)}`);
      return {
        label: m.action || m.title || s.pact,
        title: m.title || m.action || s.pact,
        badLabel: badOption,
        focusNote: stageIdx === 0 && top1 ? `${top1.title}` : '',
        scoreBefore: m.score_before,
        scoreAfter: m.score_after,
        trend: `${t(state, 'trend')}: ${m.action || m.title} (${es ? 'puntaje' : 'score'} ${m.score_before} → ${m.score_after}).`
      };
    }
    const combined = (data.score && data.score.combined_moves) || [];
    if (combined.length) {
      const best = combined.reduce((a, b) => ((b.moves || []).length >= (a.moves || []).length ? b : a), combined[0]);
      const baseScore = data.score && data.score.published_score;
      const comboLabel = (best.moves || []).join(' + ') || best.title || s.pact;
      const before = best.score_before != null ? best.score_before : baseScore;
      const badOption = es
        ? `Aplicar medidas aisladas sin coordinar el paquete completo (${before} vs. ${best.score_after})`
        : `Apply isolated moves without coordinating the full package (${before} vs. ${best.score_after})`;
      return {
        label: `${comboLabel}${best.score_after != null ? ` (${before} → ${best.score_after})` : ''}`,
        title: comboLabel,
        badLabel: badOption,
        focusNote: '',
        scoreBefore: before,
        scoreAfter: best.score_after,
        trend: `${t(state, 'trend')}: ${comboLabel} (${es ? 'puntaje' : 'score'} ${before} → ${best.score_after}).`
      };
    }
    const pub = (data.score && data.score.published_score) || 0;
    const fallbackBad = tensions[0]
      ? (es ? `Mantener abierta la tensión principal: ${tensions[0].title || tensions[0].body.slice(0, 105)}` : `Keep the main tension open: ${tensions[0].title || tensions[0].body.slice(0, 105)}`)
      : t(state, 'ignore');
    return { label: s.pact, title: s.pact, badLabel: fallbackBad, focusNote: '', scoreBefore: pub, scoreAfter: pub, trend: `${t(state, 'trend')}: ${s.pact}` };
  }

  function preview(state, data, route) {
    const lang = langOf(state);
    const s = getSpec(state.caseId, lang, data);
    if (route !== 'bad') return stepGoodOption(state, data, s, Number(state.stage) || 0).trend;
    const rec = riskRecord(state.caseId, lang);
    return rec.hasExhaustion
      ? `${t(state, 'trend')}: ${rec.label}`
      : (lang === 'ES' ? 'Sin agotamiento anual de activos invertibles; persiste la brecha de puntuación del campamento.' : 'No yearly investable-asset exhaustion; the camp score gap persists.');
  }

  function strictCasePayload(caseId, lang, node, state) {
    const source = dataFor(caseId) || {};
    const stage = Math.max(0, Math.min(Number(node) || 0, 3));
    const topRank = (state && state.fearOrder && state.fearOrder.slice(0, 3)) || [];
    const firstConcern = ((source.persona || {}).objectiveConcerns || []).find(c => c.id === topRank[0]) || ((source.persona || {}).objectiveConcerns || [])[0];
    const topic = firstConcern ? detectTopic(firstConcern.detail) : 'overview';
    return {
      strict_zero_inference: true,
      case_id: caseId,
      topic,
      lens: 'both',
      language: lang,
      stage,
      context: {
        lang: lang || 'ES',
        concerns: topRank,
        top_rank: topRank[0] || (firstConcern && firstConcern.id) || 'O1',
        thermometer: activeThermometer(state),
        subjective: (state && state.subjectiveConcern) || ''
      },
      case_data: source,
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
      thermometer: 3,
      subjectiveConcern: '',
      votes: {},
      voteTurn: 'A',
      timerStartedAt: null,
      aiReframe: null,
      aiPact: null,
      aiBrief: null,
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
    const diverged = !!(entries.length || (votes && votes.A && votes.B && ((votes.A.priority && votes.B.priority && votes.A.priority !== votes.B.priority) || (votes.A.fears && votes.B.fears && votes.A.fears[0] !== votes.B.fears[0]))));
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
        <path class="sumi-wash" d="M 20 420 Q 115 340 195 310 Q 230 295 268 272 Q 315 245 365 282 Q 445 335 555 370 L 580 540 L 10 540 Z" fill="url(#sumi-distant)" filter="url(#sumi-soft)"/>
        <path class="sumi-wash" d="M 310 470 Q 395 405 462 355 Q 505 325 552 345 Q 620 278 688 228 Q 742 268 805 310 Q 915 215 978 242 Q 1055 280 1150 430 L 1170 620 L 290 620 Z" fill="url(#sumi-mid-wash)"/>
        <ellipse cx="520" cy="435" rx="390" ry="52" fill="#FBF9F5" opacity=".88" filter="url(#sumi-mist-blur)"/>
        <path id="layerMain" class="sumi-wash" d="M 35 695 Q 115 642 190 610 Q 292 544 390 465 Q 504 384 620 295 Q 702 228 768 182 Q 802 152 830 130 Q 858 154 892 212 Q 942 292 985 274 Q 1038 320 1135 485 L 1175 725 L 20 725 Z" fill="url(#sumi-peak-wash)"/>
        <path d="M 830 130 L 795 176 L 816 172 L 774 224 L 822 192 L 832 232 L 846 186 L 878 222 L 854 166 Z" fill="#FBF9F5" opacity=".78"/>
        <path d="M 620 295 L 588 334 L 614 326 L 574 372 L 626 340 L 648 358 Z" fill="#FBF9F5" opacity=".54"/>
        <path d="M 390 465 L 364 494 L 388 488 L 412 506 Z" fill="#FBF9F5" opacity=".46"/>
        <path class="sumi-ridge-soft" d="M 85 662 Q 140 632 190 610 Q 288 548 390 465 Q 505 385 620 295 Q 726 220 830 130 Q 868 168 912 246 M 955 286 Q 985 272 1048 345" fill="none" stroke-width="2.2" opacity=".64"/>
        <path class="sumi-wash" d="M 30 585 Q 110 595 190 618 Q 275 645 375 675 L 385 745 L 20 745 Z" fill="url(#sumi-forest-wash)" filter="url(#sumi-soft)"/>
        ${sumiPines}
        <ellipse cx="600" cy="695" rx="620" ry="58" fill="#FBF9F5" opacity=".9" filter="url(#sumi-mist-blur)"/>
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
    const badChoiceText = (entry.decisionChosen && entry.decisionChosen[lang]) || goodMove.badLabel || t(state, 'ignore');
    const causedText = blockedCopy(state.caseId, state.mode, persona, state);
    const gapText = goodMove.scoreBefore != null && goodMove.scoreAfter != null
      ? ` (${lang === 'ES' ? 'brecha de score' : 'score gap'}: ${goodMove.scoreBefore} → ${goodMove.scoreAfter})`
      : '';
    const tensionsHtml = (persona.tensions || []).map(x => `<p>${detail(x.id, x, lang)}</p>`).join('') || `<p>${esc(persona.D3 || '')}</p>`;

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

  // Render Phase 1A: Wide 2-column centered overlay with Top-3 ranking, emotional thermometer, optional question, and unified couple Turn A -> Turn B
  function renderEvaluationOverlay(state, data, persona, s, couple) {
    const lang = langOf(state);
    const es = lang === 'ES';
    const turn = state.voteTurn === 'B' ? 'B' : 'A';
    const people = (state.voters && state.voters.length ? state.voters : s.people) || ['A', 'B'];
    const currentPerson = people[turn === 'B' ? 1 : 0] || people[0];
    const nextPerson = people[1] || 'B';
    const top3 = activeTop3(state);
    const thermo = activeThermometer(state);
    const rankLabels = words[lang].rankBadge;
    const turnVotes = (couple && state.votes && state.votes[turn]) || {};
    const currentPriority = turnVotes.priority || state.priorityFocus || 'deuda-proteccion';
    const currentSubjective = couple ? (turnVotes.subjective != null ? turnVotes.subjective : '') : (state.subjectiveConcern || '');

    const cardsHtml = (persona.objectiveConcerns || []).map(c => {
      const rankIdx = top3.indexOf(c.id);
      const isSelected = rankIdx >= 0;
      const badgeText = isSelected ? rankLabels[rankIdx] : words[lang].pickRank;
      const rankClass = isSelected ? `is-selected is-rank-${rankIdx + 1}` : '';
      return `<div class="concern-card ${rankClass}" data-action="toggle-concern" data-concern-id="${esc(c.id)}" role="button" tabindex="0" aria-pressed="${isSelected ? 'true' : 'false'}">
        <input type="checkbox" class="sr-only" data-fear="${esc(c.id)}" ${isSelected ? 'checked' : ''} tabindex="-1" aria-hidden="true">
        <div class="concern-card-head">
          <span class="concern-title">${esc(c.title)}</span>
          <span class="rank-badge ${rankClass}" data-rank="${isSelected ? rankIdx + 1 : ''}">${esc(badgeText)}</span>
        </div>
        <p class="concern-body">${esc(c.body)}</p>
      </div>`;
    }).join('');

    const thermoButtons = [1, 2, 3, 4, 5].map(lvl => {
      const active = thermo === lvl;
      return `<button type="button" class="thermo-pill ${active ? 'active' : ''}" data-action="set-thermometer" data-level="${lvl}" aria-pressed="${active ? 'true' : 'false'}">${esc(thermoLabels[lang][lvl])}</button>`;
    }).join('');

    const coupleHeader = couple
      ? `<div class="couple-turn-banner" data-turn="${turn}">
          <span class="turn-pill">${es ? `Turno ${turn === 'A' ? '1/2' : '2/2'}` : `Turn ${turn === 'A' ? '1/2' : '2/2'}`} · <strong>${esc(currentPerson)}</strong></span>
          <span class="turn-hint">${t(state, 'blindHint')}</span>
          <div class="couple-priority-switches">
            <label class="priority-chip ${currentPriority === 'crecimiento' ? 'active' : ''}">
              <input type="radio" name="priority" value="crecimiento" data-priority ${currentPriority === 'crecimiento' ? 'checked' : ''}>
              <span>${t(state, 'growth')}</span>
            </label>
            <label class="priority-chip ${currentPriority === 'deuda-proteccion' ? 'active' : ''}">
              <input type="radio" name="priority" value="deuda-proteccion" data-priority ${currentPriority === 'deuda-proteccion' ? 'checked' : ''}>
              <span>${t(state, 'debt')}</span>
            </label>
          </div>
        </div>`
      : '';

    const selectedSummary = top3.length
      ? top3.map((id, i) => {
          const found = (persona.objectiveConcerns || []).find(x => x.id === id);
          return `<span class="top3-chip"><strong>${esc(rankLabels[i])}:</strong> ${esc(found ? found.title : id)}</span>`;
        }).join(' ')
      : `<span class="top3-empty">${es ? 'Toca hasta 3 tarjetas para ordenarlas (1º, 2º, 3º).' : 'Click up to 3 cards to rank them (1st, 2nd, 3rd).'}</span>`;

    const primaryCtaLabel = couple
      ? (turn === 'A' ? `${t(state, 'save')} ${esc(nextPerson)}` : t(state, 'matches'))
      : t(state, 'continue');

    return `<aside class="floating-panel eval-overlay" data-phase="fears">
      <div class="eval-head">
        <div>
          <p class="eyebrow">${couple ? t(state, 'team') : t(state, 'fears')}</p>
          <h1>${couple ? `${t(state, 'private')} ${esc(currentPerson)}: ${t(state, 'fearTitle')}` : t(state, 'fearTitle')}</h1>
          <p class="body-copy">${t(state, 'fearHelp')}</p>
        </div>
        <div class="top3-status" aria-live="polite">
          <span class="eyebrow">${t(state, 'top3Counter')} (${top3.length}/3)</span>
          <div class="top3-chips">${selectedSummary}</div>
        </div>
      </div>
      ${coupleHeader}
      <div class="concerns-grid" role="group" aria-label="${t(state, 'fearTitle')}">
        ${cardsHtml}
      </div>
      <div class="eval-footer-grid">
        <div class="thermometer-box">
          <label class="eyebrow" for="thermoRange">${t(state, 'thermometerTitle')}: <strong>${esc(thermoLabels[lang][thermo])}</strong></label>
          <div class="thermometer-pills" role="group" aria-label="${t(state, 'thermometerTitle')}">${thermoButtons}</div>
          <input id="thermoRange" type="range" min="1" max="5" step="1" value="${thermo}" data-thermometer class="sr-only">
        </div>
        <div class="subjective-box">
          <label class="eyebrow" for="subjective">${t(state, 'fearAsk')}</label>
          <input id="subjective" type="text" data-subjective value="${esc(currentSubjective)}" placeholder="${esc(t(state, 'fearPlaceholder'))}">
        </div>
      </div>
      <div class="eval-actions">
        ${mathSummary(data, state)}
        <div class="button-row">
          <button class="primary" data-action="next-fears">${esc(primaryCtaLabel)}</button>
        </div>
      </div>
    </aside>`;
  }

  // Render Pre-Basecamp Contrast & Couple Diagnosis screen (phase === 'contrast' or 'cross')
  function renderContrastOverlay(state, data, persona, s, couple) {
    const lang = langOf(state);
    const es = lang === 'ES';
    const contrast = buildContrastSummary(state, data);
    const reframeText = buildThermometerReframe(state, data);
    const rankLabels = words[lang].rankBadge;
    const top3Ids = (state.fearOrder || []).slice(0, 3);
    const top3Html = top3Ids.map((id, i) => {
      const c = (persona.objectiveConcerns || []).find(x => x.id === id);
      return `<span class="top3-chip"><strong>${esc(rankLabels[i] || `#${i + 1}`)}:</strong> ${esc(c ? c.title : id)}</span>`;
    }).join(' ');

    let coupleSection = '';
    if (couple) {
      const a = (state.votes && state.votes.A) || { fears: top3Ids, thermometer: state.thermometer || 3, priority: 'crecimiento' };
      const b = (state.votes && state.votes.B) || { fears: top3Ids, thermometer: state.thermometer || 3, priority: 'deuda-proteccion' };
      const people = (state.voters && state.voters.length ? state.voters : s.people) || ['A', 'B'];
      const common = (a.fears || []).filter(id => (b.fears || []).includes(id));
      const sharedHtml = common.length
        ? common.map(id => {
            const c = (persona.objectiveConcerns || []).find(x => x.id === id);
            return `<li>${c ? detail(id, c, lang) : esc(id)}</li>`;
          }).join('')
        : `<li>${esc(persona.D6 || (es ? 'Proteger la estabilidad familiar y los hijos.' : 'Protect family stability and the children.'))}</li>`;

      const thermoA = Number(a.thermometer) || 3;
      const thermoB = Number(b.thermometer) || 3;
      const gap = Math.abs(thermoA - thermoB);
      const gapDesc = gap === 0
        ? (es ? 'Sintonía emocional plena (mismo nivel en el termómetro).' : 'Full emotional alignment (same thermometer level).')
        : gap >= 2
          ? (es ? `Brecha emocional relevante (${gap} niveles de diferencia): conviene pactar pasos automáticos para reducir la presión de quien siente mayor urgencia.`
                : `Significant emotional gap (${gap} levels apart): agree on automated steps to relieve pressure for the more stressed partner.`)
          : (es ? `Diferencia suave (${gap} nivel): fácil de armonizar con un calendario común.`
                : `Mild difference (${gap} level): easy to align with a shared schedule.`);

      const aTop = ((persona.objectiveConcerns || []).find(x => x.id === (a.fears && a.fears[0])) || {}).title || '—';
      const bTop = ((persona.objectiveConcerns || []).find(x => x.id === (b.fears && b.fears[0])) || {}).title || '—';
      const priorityDiff = a.priority && b.priority && a.priority !== b.priority
        ? `<p><strong>${t(state, 'different')}:</strong> ${esc(people[0])} (${t(state, a.priority === 'crecimiento' ? 'growth' : 'debt')}) ${es ? 'frente a' : 'vs.'} ${esc(people[1])} (${t(state, b.priority === 'crecimiento' ? 'growth' : 'debt')}).</p>`
        : `<p>${t(state, 'common')}</p>`;

      const pactText = (state.aiPact && state.aiPact.lang === lang && state.aiPact.text) || s.pact;

      coupleSection = `<div class="couple-diagnosis-grid">
        <div class="contrast-card">
          <h2>${t(state, 'agree')}</h2>
          <p class="preview"><strong>${esc(people[0])} #1:</strong> ${esc(aTop)} · <strong>${esc(people[1])} #1:</strong> ${esc(bTop)}</p>
          <ul>${sharedHtml}</ul>
        </div>
        <div class="contrast-card">
          <h2>${t(state, 'thermoGapTitle')} &amp; ${t(state, 'profileSplitTitle')}</h2>
          <p><strong>${esc(people[0])}:</strong> ${esc(thermoLabels[lang][thermoA])} · <strong>${esc(people[1])}:</strong> ${esc(thermoLabels[lang][thermoB])}</p>
          <p>${esc(gapDesc)}</p>
          <p><strong>${t(state, 'profileSplitTitle')}:</strong> ${esc(persona.D4Human || '')}</p>
          ${priorityDiff}
        </div>
      </div>
      <div class="contrast-card">
        <h2>${t(state, 'friction')}</h2>
        ${(persona.tensions || []).slice(0, 2).map(x => `<p>${detail(x.id, x, lang)}</p>`).join('')}
        <p class="reframe"><strong>${t(state, 'pact')}:</strong> ${esc(pactText)}</p>
      </div>`;
    }

    return `<aside class="floating-panel eval-overlay" data-phase="contrast">
      <div class="eval-head">
        <div>
          <p class="eyebrow">${t(state, 'cross')}</p>
          <h1>${t(state, 'contrastTitle')}</h1>
        </div>
        <div class="top3-chips">${top3Html}</div>
      </div>
      <div class="contrast-grid">
        <div class="contrast-card is-worry">
          <p class="eyebrow">${t(state, 'whatWorries')}</p>
          <h2>${esc(contrast.top1.title)}</h2>
          <p>${esc(contrast.top1.body)}</p>
        </div>
        <div class="contrast-card is-impact">
          <p class="eyebrow">${t(state, 'whatImpacts')}</p>
          <h2>${esc(contrast.bestSingle ? contrast.bestSingle.title : s.pact)}</h2>
          <p>${esc(contrast.impactText)}</p>
        </div>
      </div>
      <div class="contrast-callout">
        <strong>${t(state, 'blindSpot')}:</strong> ${esc(contrast.blindSpotText)}
      </div>
      <p class="reframe" data-ai-reframe>${esc(reframeText)}</p>
      ${coupleSection}
      ${mathSummary(data, state)}
      <div class="button-row">
        <button class="primary" data-action="start-expedition">${t(state, 'enter')}</button>
        <button data-action="edit-fears">${t(state, 'backEval')}</button>
      </div>
    </aside>`;
  }

  function render(state) {
    state = state || createInitialState();
    const lang = langOf(state);
    const raw = dataFor(state.caseId) || {};
    const data = localizeData(raw, lang);
    const persona = data.persona || {};
    const s = getSpec(state.caseId, lang, raw);
    const couple = !!(data.meta && data.meta.isCouple);
    const stageIdx = Math.max(0, Math.min(3, Number(state.stage) || 0));
    const focusedIdx = state.focusedNode != null ? Math.max(0, Math.min(3, Number(state.focusedNode) || 0)) : stageIdx;
    const stage = biome(stageIdx, lang);
    const view = viewKey(state.view);
    const dialogVisible = state.dialogVisible !== false;
    const fail = failTags[state.caseId][lang];
    const shortLabels = campShorts[lang];
    const entries = buildHistoryEntries(state.history, state.blocked, stageIdx);
    const activeRiskIdx = state.inspectedRisk != null ? Number(state.inspectedRisk) : (state.blocked && focusedIdx === stageIdx ? Math.max(0, entries.length - 1) : null);

    let initBox = fullCamera;
    if (view === 'expedition' && (state.phase === 'expedition' || state.phase === 'blocked')) {
      if (state.initialViewBox) initBox = state.initialViewBox;
      else if (state.cameraMode === 'panoramic') initBox = fullCamera;
      else if ((state.blocked && focusedIdx === stageIdx) || activeRiskIdx != null) {
        const rEntry = entries[activeRiskIdx] || { stage: stageIdx };
        initBox = dialogVisible ? riskCameraBox(fail, biomes[rEntry.stage || 0].point, rEntry.stage || 0) : fullCamera;
      } else {
        initBox = dialogVisible ? campCamera(focusedIdx) : fullCamera;
      }
    }

    const wallpaper = `<div class="mountain-stage mountain-fullscreen ${state.blocked ? 'storm-shake' : ''}" data-biome="${stage.id}" data-dialog-ready="${dialogVisible ? 'true' : 'false'}">
      ${svgMarkup(state.summit ? 0 : stage.offset, state.summit ? biomes[3].point : stage.point, state.history || [], state.blocked, couple, state.votes, fail, lang, { stage: state.summit ? 3 : stageIdx, initialViewBox: initBox, inspectedRisk: activeRiskIdx })}
    </div>`;

    const contrast = buildContrastSummary(state, data);
    const rankLabels = words[lang].rankBadge;
    const top3Summary = (state.fearOrder || []).slice(0, 3).map((id, i) => {
      const c = (persona.objectiveConcerns || []).find(x => x.id === id);
      return `${rankLabels[i] || `#${i + 1}`} ${c ? c.title : id}`;
    }).join(' · ') || contrast.top1.title;
    const thermoText = thermoLabels[lang][activeThermometer(state)];

    let panel = '';
    if (view === 'brief') {
      panel = `<aside class="floating-panel panel-wide">
        <p class="eyebrow">${t(state, 'brief')}</p>
        <h1>${t(state, 'brief')}</h1>
        <div class="advisor-brief">
          <h2>${t(state, 'concerns')}</h2>
          <p><strong>Top-3:</strong> ${esc(top3Summary)}</p>
          <p><strong>${t(state, 'thermometerTitle')}:</strong> ${esc(thermoText)}</p>
          <p><strong>${t(state, 'contrastTitle')}:</strong> ${esc(contrast.blindSpotText)}</p>
          <p>${esc(state.subjectiveConcern || persona.subjectiveConcerns || t(state, 'noAnswer'))}</p>
        </div>
        <div class="advisor-brief">
          <h2>${t(state, 'couple')}</h2>
          <p>${esc(s.pact)}</p>
          ${couple ? `<p><strong>${t(state, 'profileSplitTitle')}:</strong> ${esc(persona.D4Human || '')}</p>` : ''}
        </div>
        <div class="advisor-brief">
          <h2>${t(state, 'questions')}</h2>
          ${(state.advisorDoubts || []).map(x => `<p>${esc(x)}</p>`).join('') || `<p>${t(state, 'noQuestions')}</p>`}
        </div>
        <div class="advisor-brief">
          <h2>${t(state, 'discarded')}</h2>
          ${entries.map(x => `<p><strong>${esc(biome(x.stage || 0, lang).label)}:</strong> ${esc((x.decisionChosen && x.decisionChosen[lang]) || t(state, 'ignore'))} → ${esc(fail.label)}</p>`).join('') || `<p>${t(state, 'noDiscarded')}</p>`}
        </div>
        ${mathSummary(data, state)}
      </aside>`;
    } else if (view === 'current') {
      panel = `<aside class="floating-panel">
        <p class="eyebrow">${esc(dayLabel(lang, state.irlDay))}</p>
        <h2>${esc(s.pact)}</h2>
        <p class="body-copy"><strong>Top-3:</strong> ${esc(top3Summary)} · <strong>${esc(thermoText)}</strong></p>
        <p class="body-copy">${esc(contrast.blindSpotText)}</p>
        <p class="body-copy">${t(state, 'next')}</p>
        ${mathSummary(data, state)}
        <div class="button-row">
          <button class="primary" data-action="nav" data-view="Basecamp">${t(state, 'continueExpedition')}</button>
          <button data-action="repeat">${t(state, 'repeat')}</button>
        </div>
      </aside>`;
    } else if ((state.phase === 'fears' || state.phase === 'cordada') && !state.summit) {
      panel = renderEvaluationOverlay(state, data, persona, s, couple);
    } else if ((state.phase === 'cross' || state.phase === 'contrast') && !state.summit) {
      panel = renderContrastOverlay(state, data, persona, s, couple);
    } else if ((state.blocked && focusedIdx === stageIdx) || activeRiskIdx != null) {
      const cardHtml = renderRiskInspectionCard(state, data, persona, s, activeRiskIdx != null ? activeRiskIdx : Math.max(0, entries.length - 1));
      panel = (dialogVisible ? cardHtml : cardHtml.replace('class="floating-dialog"', 'class="floating-dialog is-dialog-hidden" hidden'))
        + `<div class="floating-overview-cta ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'is-hidden'}" ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'hidden'}><span>${t(state, 'panoramicHint')}</span><button class="primary" data-action="focus-active">${t(state, 'focusActive')}</button></div>`;
    } else {
      const inspectingOther = (focusedIdx !== stageIdx) || state.summit || view === 'overview';
      const focusedBiome = biome(focusedIdx, lang);
      const focusedMove = stepGoodOption(state, data, s, focusedIdx);
      const activeMove = stepGoodOption(state, data, s, stageIdx);
      const campRiskIdx = entries.findIndex(e => Number(e.stage) === focusedIdx);
      const focusBannerHtml = stageIdx === 0 && contrast.top1
        ? `<div class="focus-priority-pill"><strong>${t(state, 'focusBanner')}:</strong> ${esc(contrast.top1.title)} · <span>${esc(thermoText)}</span></div>`
        : '';
      const campReframe = stageIdx === 0 ? buildThermometerReframe(state, data) : s.reframe;
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
           ${focusBannerHtml}
           <p class="reframe">${esc(campReframe)}</p>
           <div class="choice-list">
             <label class="choice"><input type="radio" name="route" value="good" checked><span>${esc(activeMove.label)}</span></label>
             <label class="choice"><input type="radio" name="route" value="bad"><span>${esc(activeMove.badLabel || t(state, 'ignore'))}</span></label>
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
        const endpoint = String(kind || 'reframe').trim();
        const rawBody = Object.assign({}, payload || {});
        let body = { case_id: rawBody.case_id || 'michael-carter' };
        if (endpoint === 'reframe') {
          const validTopics = ['overview', 'liquidity', 'cash_flow', 'debt', 'retirement', 'protection', 'investments', 'home_purchase', 'housing'];
          const tp = validTopics.includes(rawBody.topic) ? rawBody.topic : 'overview';
          body = {
            case_id: body.case_id,
            topic: tp,
            lens: rawBody.lens === 'plain' || rawBody.lens === 'math' ? rawBody.lens : 'both',
            context: rawBody.context && typeof rawBody.context === 'object' ? rawBody.context : {}
          };
        } else if (endpoint === 'pact') {
          body = {
            case_id: body.case_id,
            member_a_votes: rawBody.member_a_votes || {},
            member_b_votes: rawBody.member_b_votes || {}
          };
        } else if (endpoint === 'brief') {
          body = {
            case_id: body.case_id,
            fear_ranking: Array.isArray(rawBody.fear_ranking) ? rawBody.fear_ranking : []
          };
          if (typeof rawBody.subjective_concerns === 'string' && rawBody.subjective_concerns.trim()) {
            body.subjective_concerns = rawBody.subjective_concerns.trim();
          }
        }
        const local = fallback == null ? { mode: 'deterministic', kind: endpoint, strict_zero_inference: true } : fallback;
        client.mode = 'deterministic';
        client.last = local;
        mark('deterministic');
        if (typeof root.fetch === 'function' && root.location && /^https?:$/i.test(root.location.protocol || '')) {
          try {
            const ctrl = typeof root.AbortController === 'function' ? new root.AbortController() : null;
            const timer = ctrl ? setTimeout(() => { try { ctrl.abort(); } catch (_) {} }, 1200) : null;
            return root.fetch(`/api/ai/${encodeURIComponent(endpoint)}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(body),
              signal: ctrl ? ctrl.signal : undefined
            }).then(r => {
              if (timer) clearTimeout(timer);
              return r && r.ok ? r.json() : local;
            }).then(res => {
              const out = res && typeof res === 'object' ? Object.assign({}, local, res) : local;
              client.last = out;
              return out;
            }).catch(() => {
              if (timer) clearTimeout(timer);
              return local;
            });
          } catch (_) {}
        }
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

  function toggleConcernInList(list, id) {
    const arr = Array.isArray(list) ? list.slice(0, 3) : [];
    const idx = arr.indexOf(id);
    if (idx >= 0) {
      arr.splice(idx, 1);
    } else if (arr.length < 3) {
      arr.push(id);
    } else {
      arr[2] = id;
    }
    return arr;
  }

  function handleMountainAction(action, trigger, el, state, rerender, onSummit) {
    const syncViewportClass = () => {
      if (root.document && root.document.body) {
        root.document.body.classList.add('is-mountain-viewport');
      }
    };

    if (action === 'toggle-concern') {
      const id = trigger.dataset.concernId;
      if (!id) return true;
      const raw = dataFor(state.caseId) || {};
      const isCouple = !!(raw.meta && raw.meta.isCouple);
      if (isCouple && state.phase === 'fears') {
        const turn = state.voteTurn === 'B' ? 'B' : 'A';
        state.votes = state.votes || {};
        const cur = state.votes[turn] || { fears: [], thermometer: 3, priority: turn === 'A' ? 'crecimiento' : 'deuda-proteccion' };
        cur.fears = toggleConcernInList(cur.fears, id);
        state.votes[turn] = cur;
      } else {
        state.fearOrder = toggleConcernInList(state.fearOrder, id);
      }
      rerender();
      return true;
    }

    if (action === 'set-thermometer') {
      const lvl = Math.max(1, Math.min(5, Number(trigger.dataset.level) || 3));
      const raw = dataFor(state.caseId) || {};
      const isCouple = !!(raw.meta && raw.meta.isCouple);
      if (isCouple && state.phase === 'fears') {
        const turn = state.voteTurn === 'B' ? 'B' : 'A';
        state.votes = state.votes || {};
        const cur = state.votes[turn] || { fears: [], thermometer: 3, priority: turn === 'A' ? 'crecimiento' : 'deuda-proteccion' };
        cur.thermometer = lvl;
        state.votes[turn] = cur;
      }
      state.thermometer = lvl;
      rerender();
      return true;
    }

    if (action === 'edit-fears') {
      state.phase = 'fears';
      state.voteTurn = 'A';
      rerender();
      return true;
    }

    if (action === 'next-fears' || action === 'submit-vote') {
      const raw = dataFor(state.caseId) || {};
      const isCouple = !!(raw.meta && raw.meta.isCouple);
      const allConcernIds = ((raw.persona && raw.persona.objectiveConcerns) || []).map(c => c.id);
      const checkedInDom = [...el.querySelectorAll('[data-fear]:checked,[data-vote-fear]:checked')].map(x => x.dataset.fear || x.dataset.voteFear).filter(Boolean);
      const subVal = ((el.querySelector('[data-subjective]') || {}).value || '').trim();
      const prioVal = (el.querySelector('[data-priority]:checked') || {}).value || 'deuda-proteccion';
      state.voters = getSpec(state.caseId, langOf(state), raw).people;

      if (isCouple) {
        const turn = state.voteTurn === 'B' ? 'B' : 'A';
        state.votes = state.votes || {};
        const existing = state.votes[turn] || {};
        const picked = (existing.fears && existing.fears.length)
          ? existing.fears.slice(0, 3)
          : (checkedInDom.length ? checkedInDom.slice(0, 3) : allConcernIds.slice(0, 3));
        const thermo = Number(existing.thermometer) || Number(state.thermometer) || 3;
        state.votes[turn] = {
          fears: picked,
          thermometer: thermo,
          priority: prioVal || existing.priority || (turn === 'A' ? 'crecimiento' : 'deuda-proteccion'),
          subjective: subVal || existing.subjective || ''
        };
        if (subVal && !state.advisorDoubts.includes(subVal)) {
          state.advisorDoubts.push(`${state.voters[turn === 'B' ? 1 : 0]}: ${subVal}`);
        }
        if (turn === 'A') {
          state.voteTurn = 'B';
          state.phase = 'fears';
          rerender();
          return true;
        }
        const aFears = (state.votes.A && state.votes.A.fears) || [];
        const bFears = (state.votes.B && state.votes.B.fears) || [];
        const merged = [...new Set([aFears[0], bFears[0], ...aFears, ...bFears].filter(Boolean))].slice(0, 3);
        state.fearOrder = merged.length ? merged : allConcernIds.slice(0, 3);
        state.thermometer = Math.round(((Number((state.votes.A || {}).thermometer) || 3) + (Number((state.votes.B || {}).thermometer) || 3)) / 2);
        state.subjectiveConcern = [state.votes.A && state.votes.A.subjective, state.votes.B && state.votes.B.subjective].filter(Boolean).join(' · ');
        state.phase = 'cross';
        SherpasAI.request('pact', {
          case_id: state.caseId,
          member_a_votes: state.votes.A,
          member_b_votes: state.votes.B
        }, { mode: 'deterministic' });
      } else {
        const picked = (state.fearOrder && state.fearOrder.length)
          ? state.fearOrder.slice(0, 3)
          : (checkedInDom.length ? checkedInDom.slice(0, 3) : allConcernIds.slice(0, 3));
        state.fearOrder = picked;
        if (subVal) {
          state.subjectiveConcern = subVal;
          if (!state.advisorDoubts.includes(subVal)) state.advisorDoubts.push(subVal);
        }
        state.phase = 'cross';
      }

      const payload = strictCasePayload(state.caseId, langOf(state), 0, state);
      SherpasAI.request('reframe', payload, { mode: 'deterministic' });
      rerender();
      syncViewportClass();
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
      SherpasAI.request('reframe', strictCasePayload(state.caseId, langOf(state), state.stage, state), { mode: 'deterministic' });
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
      SherpasAI.request('reframe', strictCasePayload(state.caseId, langOf(state), state.stage, state), { mode: 'deterministic' });

      if (route === 'bad') {
        const raw = dataFor(state.caseId) || {};
        const dataES = localizeData(raw, 'ES');
        const dataEN = localizeData(raw, 'EN');
        const goodES = stepGoodOption({ caseId: state.caseId, lang: 'ES', fearOrder: state.fearOrder }, dataES, getSpec(state.caseId, 'ES', raw), state.stage);
        const goodEN = stepGoodOption({ caseId: state.caseId, lang: 'EN', fearOrder: state.fearOrder }, dataEN, getSpec(state.caseId, 'EN', raw), state.stage);
        const existingIdx = state.history.findIndex(h => Number(h.stage) === Number(state.stage));
        const entry = {
          stage: state.stage,
          campLabel: { ES: biomes[state.stage].ES, EN: biomes[state.stage].EN },
          decisionChosen: { ES: goodES.badLabel || words.ES.ignore, EN: goodEN.badLabel || words.EN.ignore },
          recommendedMove: { ES: goodES.label, EN: goodEN.label, scoreBefore: goodEN.scoreBefore, scoreAfter: goodEN.scoreAfter },
          detailKey: 'D3',
          detail: (dataES.persona || {}).D3 || ''
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
      SherpasAI.request('brief', {
        case_id: state.caseId,
        fear_ranking: state.fearOrder || [],
        subjective_concerns: state.subjectiveConcern || ''
      }, { mode: 'deterministic' });
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
          if (vk === 'brief') {
            SherpasAI.request('brief', {
              case_id: state.caseId,
              fear_ranking: state.fearOrder || [],
              subjective_concerns: state.subjectiveConcern || ''
            }, { mode: 'deterministic' });
          }
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
        } else if (a === 'doubt') state.advisorDoubts.push(n.dataset.doubt || '');
        else if (a === 'repeat') { const next = createInitialState(state.caseId); next.lang = state.lang; state = next; }
        update();
        state.initialViewBox = null;
      });
      el.querySelectorAll('[data-fear]').forEach(n => n.onchange = () => {
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
        update();
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
        update();
      };
      el.querySelectorAll('[name="route"]').forEach(n => n.onchange = () => {
        const p = el.querySelector('[data-preview]');
        if (p) p.textContent = preview(state, localizeData(dataFor(state.caseId), langOf(state)), n.value);
      });
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
    thermoLabels,
    buildContrastSummary,
    buildThermometerReframe,
    orderedTopMoves,
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
