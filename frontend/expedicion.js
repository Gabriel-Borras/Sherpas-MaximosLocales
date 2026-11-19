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
      fears: 'Fase 1A · Evaluación',
      fearTitle: '¿Qué 3 temas priorizas hoy?',
      fearHelp: 'Elige hasta 3 en orden (1º, 2º, 3º). Tu #1 abre el Basecamp.',
      fearAsk: 'Duda opcional',
      fearPlaceholder: 'Duda rápida para tu asesor (opcional)...',
      continue: 'Ver contraste',
      enter: 'Entrar al Basecamp',
      backEval: 'Cambiar Top-3',
      team: 'Fase 1A · Turno privado',
      private: 'Turno de',
      blindHint: 'Elige tu Top-3 en privado sin que la otra persona mire.',
      growth: 'Crecimiento',
      debt: 'Liquidez y protección',
      time: 'Turno a ciegas',
      save: 'Pasar turno a',
      matches: 'Ver contraste en pareja',
      cross: 'Contraste del plan',
      agree: 'Coincidencias',
      friction: 'Pareja y pacto',
      pact: 'Pacto',
      contrastTitle: 'Tu #1 vs. Mayor impacto',
      whatWorries: 'Tu #1',
      whatImpacts: 'Mayor impacto',
      blindSpot: 'Clave',
      thermometerTitle: 'Nivel de inquietud',
      thermoGapTitle: 'Pareja',
      profileSplitTitle: 'Perfil de riesgo',
      rankBadge: ['1º', '2º', '3º'],
      pickRank: '+',
      top3Counter: 'Top-3',
      showMore: 'más',
      showLess: 'Ver menos',
      focusBanner: 'Foco #1',
      youAre: 'Eres',
      copyLinkFor: 'Copiar enlace para',
      copied: '¡Copiado!',
      openPartnerTab: 'Abrir',
      inNewTab: 'en nueva pestaña',
      sameDevice: 'Mismo dispositivo',
      twoDevices: '2 dispositivos',
      submitEval: 'Enviar mi evaluación',
      waitingFor: 'Esperando a',
      waitingEvalSub: 'Al enviar su respuesta, la comparativa se abrirá en ambos dispositivos.',
      waitingDecSub: 'En cuanto elija camino, veréis la comparativa aquí.',
      yourChoice: 'Tu elección',
      alignedAdvancing: 'Coincidís → Avanzando',
      pathCompareTitle: 'Comparativa de caminos',
      safeRoute: 'Camino seguro',
      riskRoute: 'Desvío de riesgo',
      agreeAdvance: 'Reunir cordada y avanzar',
      seeRedBranch: 'Ver desvío rojo',
      redoEval: 'Rehacer evaluación',
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
      fears: 'Phase 1A · Assessment',
      fearTitle: 'Which 3 topics matter most today?',
      fearHelp: 'Pick up to 3 in order (1st, 2nd, 3rd). Your #1 opens Basecamp.',
      fearAsk: 'Optional note',
      fearPlaceholder: 'Quick question for your advisor (optional)...',
      continue: 'View contrast',
      enter: 'Enter Basecamp',
      backEval: 'Edit Top-3',
      team: 'Phase 1A · Private turn',
      private: 'Turn:',
      blindHint: 'Pick your Top-3 privately before handing the screen over.',
      growth: 'Growth',
      debt: 'Liquidity & protection',
      time: 'Blind turn',
      save: 'Pass turn to',
      matches: 'See couple contrast',
      cross: 'Plan contrast',
      agree: 'Shared priorities',
      friction: 'Couple & pact',
      pact: 'Pact',
      contrastTitle: 'Your #1 vs. Biggest impact',
      whatWorries: 'Your #1',
      whatImpacts: 'Biggest impact',
      blindSpot: 'Takeaway',
      thermometerTitle: 'Stress level',
      thermoGapTitle: 'Couple',
      profileSplitTitle: 'Risk profile',
      rankBadge: ['1st', '2nd', '3rd'],
      pickRank: '+',
      top3Counter: 'Top-3',
      showMore: 'more',
      showLess: 'Show less',
      focusBanner: 'Focus #1',
      youAre: 'You are',
      copyLinkFor: 'Copy link for',
      copied: 'Copied!',
      openPartnerTab: 'Open',
      inNewTab: 'in new tab',
      sameDevice: 'Same device',
      twoDevices: '2 devices',
      submitEval: 'Submit my assessment',
      waitingFor: 'Waiting for',
      waitingEvalSub: 'Once they submit, the comparison unlocks on both devices.',
      waitingDecSub: 'Once they pick a path, you will see the comparison here.',
      yourChoice: 'Your choice',
      alignedAdvancing: 'Aligned → Advancing',
      pathCompareTitle: 'Path comparison',
      safeRoute: 'Safe path',
      riskRoute: 'Risk deviation',
      agreeAdvance: 'Reunite rope team & advance',
      seeRedBranch: 'Inspect red deviation',
      redoEval: 'Redo evaluation',
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
      1: '1 Calma',
      2: '2',
      3: '3',
      4: '4',
      5: '5 Urgente'
    },
    EN: {
      1: '1 Calm',
      2: '2',
      3: '3',
      4: '4',
      5: '5 Urgent'
    }
  };

  const campShorts = { ES: ['Base', 'C1', 'C2', 'Cima'], EN: ['Base', 'C1', 'C2', 'Summit'] };
  const campAlts = ['2,800m', '4,600m', '6,900m', '8,848m'];
  const shortWords = (txt, maxWords) => {
    const w = String(txt || '').replace(/\s+/g, ' ').trim().split(' ');
    return w.length <= maxWords ? w.join(' ') : `${w.slice(0, maxWords).join(' ').replace(/[,:;.]$/, '')}…`;
  };
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

  const TRAIL_PATH = 'M 255 552 Q 285 516 312 491 Q 368 498 432 479 Q 504 442 564 382 Q 624 378 684 319 Q 744 295 804 209 Q 836 168 858 145';
  const TRAIL_SEGS = [
    [[255, 552], [285, 516], [312, 491]],
    [[312, 491], [368, 498], [432, 479]],
    [[432, 479], [504, 442], [564, 382]],
    [[564, 382], [624, 378], [684, 319]],
    [[684, 319], [744, 295], [804, 209]],
    [[804, 209], [836, 168], [858, 145]]
  ];
  const TRAIL_LENGTH = 757;
  const TRAIL_FRACS = [0.1104, 0.4883, 0.6713, 1];
  const fullCamera = [0, 0, 1200, 750];

  const biomes = [
    { id: 'forest', point: [312, 491], offset: 757, ES: 'Campamento Base · Bosque · 2.800 m', EN: 'Basecamp · Forest · 2,800 m' },
    { id: 'rock', point: [564, 382], offset: 387, ES: 'Campo 1 · Roca y niebla · 4.600 m', EN: 'Camp 1 · Rock and fog · 4,600 m' },
    { id: 'snow', point: [684, 319], offset: 249, ES: 'Campo 2 · Glaciar · 6.900 m', EN: 'Camp 2 · Glacier · 6,900 m' },
    { id: 'summit', point: [858, 145], offset: 0, ES: 'La Cima · Meta alcanzada · 8.848 m', EN: 'Summit · Goal reached · 8,848 m' }
  ];
  const biome = (i, lang) => Object.assign({}, biomes[i], { label: biomes[i][lang] });

  const BIOME_ASSETS = {
    forest: 'assets/mountain-biome-forest.jpg',
    rock: 'assets/mountain-biome-rock.jpg',
    snow: 'assets/mountain-biome-snow.jpg',
    summit: 'assets/mountain-biome-summit.jpg'
  };
  const BIOME_ORDER = ['forest', 'rock', 'snow', 'summit'];
  let biomePreloaded = false;
  function preloadBiomeAssets() {
    if (biomePreloaded || !root || typeof root.Image !== 'function') return;
    biomePreloaded = true;
    BIOME_ORDER.forEach(id => {
      try {
        const img = new root.Image();
        img.decoding = 'async';
        img.src = BIOME_ASSETS[id];
      } catch (_) {}
    });
  }
  preloadBiomeAssets();

  function resolveActiveBiome(state) {
    if (!state) return null;
    if (state.summit || state.phase === 'summit') return 'summit';
    if (state.phase === 'fears' || state.phase === 'cross') return null;
    if (!state.hasEnteredCamp && !(Number(state.stage) > 0)) return null;
    const idx = Math.max(0, Math.min(3, Number(state.stage) || 0));
    return biomes[idx] ? biomes[idx].id : null;
  }

  function applyBiomeToDom(el, biomeId) {
    if (!el || !el.querySelector) return;
    const normalized = biomeId && BIOME_ASSETS[biomeId] ? biomeId : null;
    const stageEl = el.querySelector('.mountain-stage');
    if (stageEl) stageEl.dataset.biome = normalized || 'none';
    const baseImg = el.querySelector('#sumiMountainArt');
    if (baseImg) baseImg.classList.toggle('is-covered', !!normalized);
    el.querySelectorAll('.mountain-biome-layer').forEach(img => {
      img.classList.toggle('is-active', !!normalized && img.dataset.biomeLayer === normalized);
    });
  }

  let biomeCrossfadeToken = 0;
  let biomeCrossfadeRaf1 = null;
  let biomeCrossfadeRaf2 = null;
  function cancelBiomeCrossfade() {
    biomeCrossfadeToken++;
    if (typeof root.cancelAnimationFrame === 'function') {
      if (biomeCrossfadeRaf1) root.cancelAnimationFrame(biomeCrossfadeRaf1);
      if (biomeCrossfadeRaf2) root.cancelAnimationFrame(biomeCrossfadeRaf2);
    }
    biomeCrossfadeRaf1 = null;
    biomeCrossfadeRaf2 = null;
  }

  function scheduleBiomeCrossfade(el, nextBiome) {
    cancelBiomeCrossfade();
    if (!hasRaf() || !el) return;
    const raf = root.requestAnimationFrame;
    const token = biomeCrossfadeToken;
    biomeCrossfadeRaf1 = raf(() => {
      biomeCrossfadeRaf1 = null;
      if (token !== biomeCrossfadeToken) return;
      biomeCrossfadeRaf2 = raf(() => {
        biomeCrossfadeRaf2 = null;
        if (token !== biomeCrossfadeToken) return;
        applyBiomeToDom(el, nextBiome);
      });
    });
  }

  const specs = {
    'michael-carter': {
      ES: { people: ['Michael'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Prioriza tu colchón líquido, un seguro extra ante imprevistos y sacar menos dinero de tus ahorros al año.', pact: 'Ordenar tarjeta, seguro extra y cuánto sacas de tus ahorros al año.', events: [] },
      EN: { people: ['Michael'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Prioritize your cash cushion, extra liability protection, and taking less from savings each year.', pact: 'Tackle credit card, extra protection, and yearly savings withdrawals.', events: [] }
    },
    'samantha-lewis': {
      ES: { people: ['Samantha'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Asegura vivienda y vehículo y reparte mejor tu inversión en VTI.', pact: 'Confirmar seguros de hogar/auto y diversificar tu inversión.', events: [] },
      EN: { people: ['Samantha'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Insure your home and vehicle and spread out your VTI concentration.', pact: 'Confirm home/auto policies and diversify investments.', events: [] }
    },
    'timothy-melanie-weah': {
      ES: { people: ['Timothy', 'Melanie'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Liquida la tarjeta al 18% con el efectivo disponible y amplía el seguro de vida.', pact: 'Liquidar la tarjeta de crédito y proteger a la familia.', events: [] },
      EN: { people: ['Timothy', 'Melanie'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Pay off the 18% credit card with available cash and increase life insurance.', pact: 'Pay off the credit card and protect the family.', events: [] }
    },
    'daniel-emily-johnson': {
      ES: { people: ['Daniel', 'Emily'], blocked: 'Consulta el registro anual del plan para ver el punto documentado.', reframe: 'Amplía el seguro de vida familiar y redirige ahorro a la tarjeta y al 401(k).', pact: 'Proteger a la familia y ahorrar más cada año.', events: [] },
      EN: { people: ['Daniel', 'Emily'], blocked: 'Consult the yearly plan record for the documented point.', reframe: 'Increase family life insurance and redirect savings to the card and 401(k).', pact: 'Protect the family and save more each year.', events: [] }
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
    'Add umbrella cover': 'Seguro extra ante imprevistos graves',
    'Lower the withdrawal rate': 'Sacar menos dinero de tus ahorros al año',
    'Raise growth allocation toward glide': 'Invertir más para el largo plazo',
    'Close a coverage gap': 'Asegurar tu vivienda principal',
    'Reduce single-name concentration': 'Repartir mejor tu inversión en VTI',
    'Reduce growth allocation toward glide': 'Moderar el riesgo de tu cartera',
    'Pay down revolving card': 'Liquidar la tarjeta de crédito',
    'Pay off revolving card': 'Liquidar la tarjeta de crédito',
    'Build emergency fund': 'Completar tu colchón de emergencia',
    'Add life cover': 'Ampliar tu seguro de vida',
    'Add life insurance': 'Ampliar tu seguro de vida',
    'Raise mortality coverage': 'Ampliar tu seguro de vida',
    'Raise annual savings': 'Ahorrar más cada año para tu futuro'
  };

  const moveTitlesEN = {
    'Add umbrella cover': 'Extra liability protection',
    'Lower the withdrawal rate': 'Take less from your savings each year',
    'Raise growth allocation toward glide': 'Invest more for long-term growth',
    'Close a coverage gap': 'Insure your primary home',
    'Reduce single-name concentration': 'Spread out your VTI concentration',
    'Reduce growth allocation toward glide': 'Dial back portfolio risk',
    'Pay down revolving card': 'Pay off high-interest credit card',
    'Pay off revolving card': 'Pay off high-interest credit card',
    'Build emergency fund': 'Build your emergency cash cushion',
    'Add life cover': 'Increase life insurance cover',
    'Add life insurance': 'Increase life insurance cover',
    'Raise mortality coverage': 'Increase life insurance cover',
    'Raise annual savings': 'Save more each year for the future'
  };

  function everydayMoveTitle(rawTitle, lang) {
    const t0 = String(rawTitle || '').trim();
    if (lang === 'EN') {
      if (moveTitlesEN[t0]) return moveTitlesEN[t0];
      return t0
        .replace(/revolving card/gi, 'high-interest credit card')
        .replace(/toward glide/gi, 'for long-term growth')
        .replace(/mortality coverage/gi, 'life insurance cover')
        .replace(/withdrawal rate/gi, 'yearly savings withdrawals')
        .replace(/umbrella cover/gi, 'extra liability protection');
    }
    if (moveTitles[t0]) return moveTitles[t0];
    return translateTitleToES(t0)
      .replace(/tasa de retiro/gi, 'dinero que sacas de tus ahorros')
      .replace(/deuda rotativa|tarjeta revolvente|tarjeta rotativa/gi, 'tarjeta de crédito')
      .replace(/senda objetivo|curva objetivo|glide/gi, 'largo plazo')
      .replace(/cobertura paraguas|póliza paraguas/gi, 'seguro extra ante imprevistos');
  }

  function compactMoveActionLine(move, scoreNow, lang) {
    const es = lang !== 'EN';
    const raw = String((move && (move.action || move.title)) || '');
    const before = (move && move.score_before != null) ? move.score_before : scoreNow;
    const after = (move && move.score_after != null) ? move.score_after : scoreNow;
    const healthSuffix = es ? `Salud financiera ${before} → ${after}` : `Financial health ${before} → ${after}`;
    let detailPart = '';
    const mAmt = raw.match(/\$[\d,.]+[MK]?/i);
    const mPct = raw.match(/\d+(?:\.\d+)?%/g);
    if (/withdraw|sacas|retiros|10,300/i.test(raw) && mAmt) {
      detailPart = es ? `Bajar lo que sacas a ${mAmt[0]}/año` : `Limit yearly withdrawals to ${mAmt[0]}/yr`;
    } else if (/umbrella|paraguas|responsabilidad civil|imprevistos/i.test(raw) && mAmt) {
      detailPart = es ? `Añadir protección civil extra de ${mAmt[0]}` : `Add ${mAmt[0]} in extra liability protection`;
    } else if (/card|tarjeta/i.test(raw) && mAmt) {
      detailPart = es ? `Pagar ${mAmt[0]} de la tarjeta${mPct ? ` al ${mPct[0]}` : ''}` : `Pay ${mAmt[0]} toward the${mPct ? ` ${mPct[0]}` : ''} card`;
    } else if (/life|mortality|seguro de vida/i.test(raw) && mAmt) {
      detailPart = es ? `Añadir ${mAmt[0]} de seguro de vida` : `Add ${mAmt[0]} of life insurance`;
    } else if (/homeowners|hogar|vivienda/i.test(raw)) {
      detailPart = es ? 'Activar póliza de seguro de hogar' : 'Activate homeowners insurance policy';
    } else if (/VTI/i.test(raw) && mPct && mPct.length >= 2) {
      detailPart = es ? `Bajar VTI del ${mPct[0]} al ${mPct[1]}` : `Trim VTI from ${mPct[0]} to ${mPct[1]}`;
    } else if (/free cash flow|flujo de caja|annual savings|ahorro/i.test(raw) && mAmt) {
      detailPart = es ? `Destinar ${mAmt[0]}/año extra al ahorro` : `Redirect ${mAmt[0]}/yr into savings`;
    } else if (/growth|crecimiento/i.test(raw) && mPct && mPct.length >= 2) {
      detailPart = es ? `Ajustar inversión del ${mPct[0]} al ${mPct[1]}` : `Adjust invested mix from ${mPct[0]} to ${mPct[1]}`;
    } else if (mAmt) {
      detailPart = es ? `Importe clave: ${mAmt[0]}` : `Key amount: ${mAmt[0]}`;
    }
    return detailPart ? `${detailPart} · ${healthSuffix}` : healthSuffix;
  }

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
    [/The average draw is ([\d.]+%)\./gi, 'El dinero que saca cada año equivale al $1 de sus ahorros.'],
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
    [/(?:D4 misalignment,?\s*)?The spouses' stated profiles \(Growth and Moderate\) differ, while the invested book is about ([\d.]+%) stocks\.?/gi,
      'Sus perfiles declarados difieren (Crecimiento frente a Moderado), mientras la cartera invertida alcanza un $1 en acciones.'],
    [/Revealed risk is higher than the Moderate household reading\.?/gi,
      'El riesgo real de la cartera supera la lectura moderada del hogar.'],
    [/An ([\d.]+%) card balance is carried while accessible cash far exceeds the reserve\. The card costs about (\$[\d,.]+) a year in interest \(([\d.]+%) of (\$[\d,.]+)\), against roughly (\$[\d,.]+) a year earned on the cash\./gi,
      'Se arrastra una tarjeta al $1 APR mientras el efectivo supera ampliamente la reserva: la tarjeta cuesta unos $2 al año en intereses ($3 de $4) frente a solo $5 anuales que rinde el efectivo.'],
    [/O4 against current savings priorities\.\s*/gi, ''],
    [/The (\$[\d,.]+) yearly education need competes with 401\(k\), Roth and HSA contributions for the same cash flow, which is itself reported as uncertain\./gi,
      'Los $1 anuales requeridos para educación compiten con las aportaciones al 401(k), Roth y HSA por el mismo flujo de caja.'],
    [/compete for the same (\$[\d,.]+) of yearly free cash flow\. Retirement needs about (\$[\d,.]+) a year and the cash gap is (\$[\d,.]+)\. They must weigh the trade-off together\./gi,
      'Jubilación, reserva líquida y seguros compiten por los mismos $1 de flujo de caja libre anual: el retiro necesita unos $2/año y a la reserva le faltan $3, por lo que deben priorizar en pareja.'],
    [/O2, O3 and D4c\.\s*/gi, ''],
    [/The protection gaps stay open while the household carries high exposure and a thin cushion, and closing them costs cash flow that(?: O1 and O4)? also need\./gi,
      'Las brechas de protección siguen abiertas mientras el hogar mantiene un colchón líquido estrecho, y cubrirlas requiere parte del flujo que también necesitan la reserva y el retiro.'],
    [/They state a Moderate orientation and hold a moderate portfolio, but their overall exposure is closer to aggressive, which suggests drift\. Any plan also has to work for both a Growth and a Moderate partner\./gi,
      'Declaran una orientación moderada en cartera, pero su baja liquidez y falta de seguros los expone a un riesgo real elevado; además, el plan debe equilibrar el perfil de Crecimiento de él con el Moderado de ella.'],
    [/O5 against the current saving pattern\.\s*/gi, ''],
    [/The household saves (\$[\d,.]+) a year \((\$[\d,.]+) to brokerage, (\$[\d,.]+) to the 529 and (\$[\d,.]+) to cash\) while carrying an (\$[\d,.]+) balance at ([\d.]+%) and sending (\$[\d,.]+) to the 401\(k\)s\./gi,
      'El hogar ahorra $1 al año ($2 a corretaje, $3 al plan 529 y $4 a efectivo) mientras arrastra $5 en tarjeta al $6 APR y aporta $7 a los planes 401(k).'],
    [/The 529 receives (\$[\d,.]+) a year while retirement receives nothing, though retirement is the larger gap\./gi,
      'El plan universitario 529 recibe $1 al año mientras que la jubilación no recibe aportaciones, pese a ser la brecha financiera mayor.'],
    // Top moves actions & notes (everyday plain language)
    [/Add (\$[\d,.]+[MK]?) of umbrella to raise the liability shield/gi,
      'Contratar un seguro extra de $1 ante imprevistos graves de responsabilidad civil'],
    [/Cutting withdrawals to (\$[\d,.]+)\/year \(([\d.]+%)\) reaches the sustainable band/gi,
      'Bajar lo que sacas de tus ahorros a $1/año ($2) para que el dinero te dure todo el plan'],
    [/Move the invested mix from ([\d.]+%) to ([\d.]+%) growth \(glide ([\d.]+%)\) for the next horizon-fit band — about (\$[\d,.]+) of the invested book/gi,
      'Invertir más para el largo plazo: pasar del $1 al $2 en crecimiento (unos $4 de la cartera)'],
    [/Add homeowners insurance on Primary home so coverage integrity clears that gap/gi,
      'Activar la póliza de seguro de hogar sobre tu vivienda principal'],
    [/Bring VTI from ([\d.]+%) to ([\d.]+%) of investable for the next concentration band — about (\$[\d,.]+) of that line/gi,
      'Repartir mejor tu inversión: bajar VTI del $1 al $2 (unos $3)'],
    [/Pay (\$[\d,.]+) on the ([\d.]+%) card from cash to remove high revolving exposure and clear the gate/gi,
      'Pagar $1 de la tarjeta al $2 usando tu efectivo disponible para quitar intereses caros'],
    [/Add (\$[\d,.]+) of life cover to raise the mortality ratio and clear the gate/gi,
      'Añadir $1 de seguro de vida para proteger a la familia'],
    [/Add (\$[\d,.]+) of life cover to reach the next mortality-coverage anchor/gi,
      'Añadir $1 de seguro de vida para proteger a la familia'],
    [/Redirect (\$[\d,.]+)\/year of free cash flow into savings to raise retirement-directed savings toward the next band/gi,
      'Destinar $1/año que sobran cada año a ahorrar para tu futuro'],
    [/After the card paydown, life cover must reach (\$[\d,.]+) to keep the mortality ratio at the gate line\./gi,
      'Tras rebajar la tarjeta, la cobertura de vida debe situarse en $1 para superar ambos límites del score.'],
    [/Together they raise the published score more than either move alone\./gi,
      'Ejecutadas en conjunto elevan la puntuación del plan más que cada medida por separado.'],
    // Transition alerts & subjective concerns & D6/D4
    [/Home purchase in January (\d{4}) \(within 12 months\)\.\s*Michael plans to buy a (\$[\d,.]+) home \((\$[\d,.]+) at purchase\) with a (\$[\d,.]+) down payment and a (\d+)-year loan of (\$[\d,.]+) at ([\d.]+%)\.\s*The monthly payment is (\$[\d,.]+),?[^.]*\./gi,
      'Compra de vivienda en enero de $1 (en menos de 12 meses): planea adquirir una casa de $2 ($3 al cierre) con $4 de entrada y una hipoteca a $5 años de $6 al $7 ($8/mes).'],
    [/The home would also add property taxes of (\$[\d,.]+) a year, home insurance of (\$[\d,.]+) a year and (\$[\d,.]+) of closing costs\./gi,
      'La vivienda sumaría además $1/año en impuestos de propiedad, $2/año en seguro de hogar y $3 de gastos de cierre.'],
    [/Housing costs, cash, the debt load and retirement saving all change at once\./gi,
      'Los costes de vivienda, la liquidez, la carga de deuda y el ahorro para el retiro cambian todos a la vez.'],
    [/The yearly projection shows investable assets of (\$[\d,.]+) in (\d{4}) and (\$[\d,.]+) in (\d{4})\./gi,
      'La proyección anual muestra activos invertibles de $1 en $2 y $3 en $4.'],
    [/-?\s*The (\$[\d,.]+) vacation also falls in January (\d{4}) and repeats every year until (\d{4})\./gi,
      'Las vacaciones de $1 también coinciden en enero de $2 y se repiten cada año hasta $3.'],
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

  function compactConcern(title, body, rawCleaned, lang) {
    const es = lang !== 'EN';
    const src = `${title} ${body}`;
    const raw = String(rawCleaned || src);

    // 1. Ultra-short 3-5 word title (specific rules BEFORE broad retirement rule to prevent duplicate titles)
    let shortTitle = title;
    const shortMap = es ? [
      [/margen fiscal|espacio fiscal|ventaja fiscal/i, 'Ahorro fiscal sin aprovechar'],
      [/coste fiscal/i, 'Impuestos evitables en cartera'],
      [/se agota a los (\d+)/i, 'Ahorro corto ($1 años)'],
      [/jubilaci|retiro/i, 'Brecha de jubilación'],
      [/compra de vivienda.*2030|prevista para 2030/i, 'Compra vivienda 2030'],
      [/efectivo ajustado.*vivienda|vivienda/i, 'Efectivo para vivienda'],
      [/seguro de vida/i, 'Seguro de vida'],
      [/paraguas|imprevistos/i, 'Seguro extra ante imprevistos'],
      [/vivienda y vehículo sin póliza|sin póliza/i, 'Vivienda y auto sin póliza'],
      [/flujo de caja.*negativo/i, 'Flujo de caja negativo'],
      [/margen.*estrecho/i, 'Margen de ahorro justo'],
      [/tarjeta.*([\d.]+%)|alto interés|alto coste/i, 'Tarjeta cara'],
      [/universid|educat|529/i, 'Fondo universitario'],
      [/efectivo ocioso|sin rentabilidad/i, 'Efectivo sin rentabilidad'],
      [/colchón líquido|reserva de liquidez/i, 'Reserva de liquidez'],
      [/concentraci|acciones sobre objetivo/i, 'Concentración en cartera'],
      [/dependencia.*salari|solo sueldo/i, 'Dependencia salarial']
    ] : [
      [/unused|tax-advantaged/i, 'Unused tax-advantaged savings'],
      [/tax cost/i, 'Portfolio tax drag'],
      [/runs out.*age (\d+)/i, 'Savings end at $1'],
      [/retirement/i, 'Retirement gap'],
      [/home purchase.*2030/i, '2030 home purchase'],
      [/cash for the home|down payment/i, 'Home cash reserve'],
      [/life insurance/i, 'Life insurance gap'],
      [/umbrella|liability/i, 'Extra liability protection'],
      [/no home or auto insurance/i, 'Uninsured home & car'],
      [/cash flow is negative|negative cash flow/i, 'Negative cash flow'],
      [/thin margin/i, 'Thin cash margin'],
      [/credit card|high-interest card|([\d.]+%) card/i, 'High-rate credit card'],
      [/college|education|529/i, 'College funding gap'],
      [/idle cash/i, 'Idle low-yield cash'],
      [/thin cash|cash reserve/i, 'Thin cash reserve'],
      [/concentrat|equity above target/i, 'Portfolio concentration'],
      [/income dependence|one employer/i, 'Salary concentration']
    ];
    let matchedTitle = false;
    for (const [rx, rep] of shortMap) {
      if (rx.test(title)) { shortTitle = title.match(rx)[0].replace(rx, rep); matchedTitle = true; break; }
    }
    if (!matchedTitle) {
      for (const [rx, rep] of shortMap) {
        if (rx.test(src)) { shortTitle = src.match(rx)[0].replace(rx, rep); break; }
      }
    }
    if (shortTitle.split(/\s+/).length > 5) {
      shortTitle = shortTitle.split(/\s+/).slice(0, 5).join(' ').replace(/[,:;.]$/, '');
    }

    // 2. Single-line key metric (literal JSON figures only, max ~55 chars; NEVER raw $digit literals in replace strings!)
    let keyMetric = '';
    const metricRules = es ? [
      [/se agotan a los (\d+) años.*brecha de (\$[\d,.]+)/i, (_, a, g) => `Se agota a los ${a} años · brecha ${g}`],
      [/tienen (\$[\d,.]+).*cubre el ([\d.]+%).*quedan (\$[\d,.]+)/i, (_, z, p, u) => `Cuentas retiro ${z} · ${u} sin cubrir`],
      [/brecha de jubilación es de (\$[\d,.]+).*requiere unos (\$[\d,.]+)/i, (_, g, y) => `Brecha ${g} · +${y}/año necesarios`],
      [/efectivo disponible de (\$[\d,.]+) cubre unos ([\d.]+) meses/i, (_, c, m) => `${c} en caja (${m} meses)`],
      [/faltan (\$[\d,.]+).*vivienda/i, (_, a) => `Faltan ${a} para reserva y compra`],
      [/cuenta con (\$[\d,.]+).*frente a los (\$[\d,.]+)/i, (_, h, r) => `Tiene ${h} vs ${r} recomendados`],
      [/Timothy le faltan (\$[\d,.]+).*Melanie (\$[\d,.]+)/i, (_, a, b) => `Faltan ${a} (Timothy) y ${b} (Melanie)`],
      [/cobertura de (\$[\d,.]+) en Daniel y (\$[\d,.]+) en Emily/i, (_, a, b) => `Déficit ${a} (Daniel) y ${b} (Emily)`],
      [/vivienda de (\$[\d,.]+).*Porsche Cayenne de (\$[\d,.]+)/i, (_, h, c) => `Casa ${h} y Porsche ${c} sin póliza`],
      [/mínimo recomendado es (\$[\d,.]+)/i, (_, m) => `Mínimo ${m} · hoy $0`],
      [/brecha de (\$[\d,.]+) en responsabilidad civil/i, (_, m) => `Falta protección de ${m}`],
      [/falta una cobertura paraguas de (\$[\d,.]+)/i, (_, m) => `Falta protección de ${m} (+4 pts)`],
      [/flujo de caja neto es de (-\$[\d,.]+) al año/i, (_, f) => `${f}/año en negativo`],
      [/déficit anual de (\$[\d,.]+)/i, (_, f) => `-${f}/año tras gastos y ahorro`],
      [/flujo de caja libre de (\$[\d,.]+) al año/i, (_, f) => `Solo ${f}/año libres (5.37%)`],
      [/Amex Platinum es de (\$[\d,.]+) al ([\d.]+%)/i, (_, b, r) => `${b} al ${r} APR`],
      [/mantienen (\$[\d,.]+) en tarjeta al ([\d.]+%).*?(\$[\d,.]+) de efectivo/i, (_, b, r, c) => `${b} al ${r} APR (con ${c} en caja)`],
      [/tarjeta de (\$[\d,.]+)/i, (_, b) => `Tarjeta ${b} al 24.9% APR`],
      [/(\$[\d,.]+) de margen adicional \(unos (\$[\d,.]+)/i, (_, r, s) => `+${r} libres en 401(k) · ahorra ${s}/año`],
      [/aportar hasta (\$[\d,.]+) al año a una HSA.*hasta (\$[\d,.]+)/i, (_, h, i) => `Hasta ${h} en HSA y ${i} en IRA`],
      [/factura fiscal.*cuesta unos (\$[\d,.]+) al año/i, (_, t) => `${t}/año en impuestos evitables`],
      [/ahorro fiscal.*(\$[\d,.]+)/i, (_, s) => `Hasta ${s}/año en ahorro fiscal`],
      [/generaría unos (\$[\d,.]+) al año en ahorro fiscal/i, (_, s) => `Hasta ${s}/año en ahorro fiscal`],
      [/faltan (\$[\d,.]+) por cubrir para la universidad/i, (_, g) => `Faltan ${g} · saldo 529 en $0`],
      [/tienen (\$[\d,.]+) en cuentas 529 frente a.*(\$[\d,.]+)/i, (_, b, g) => `${b} en 529 · brecha de ${g}`],
      [/brecha universitaria de (\$[\d,.]+).*?(\$[\d,.]+) ya acumulados/i, (_, g, b) => `Brecha de ${g} (${b} en 529)`],
      [/hay (\$[\d,.]+) ociosos.*rindiendo apenas un ([\d.]+%)/i, (_, c, r) => `${c} ociosos rindiendo solo ${r}`],
      [/quedan (\$[\d,.]+) por encima de la reserva/i, (_, c) => `Solo ${c} libres tras metas cercanas`],
      [/efectivo disponible de (\$[\d,.]+).*déficit líquido de (\$[\d,.]+)/i, (_, c, g) => `${c} disponibles · faltan ${g}`],
      [/compra de (\$[\d,.]+).*entrada de (\$[\d,.]+)/i, (_, h, d) => `Casa ${h} · entrada ${d}`],
      [/(\$[\d,.]+) en el ETF apalancado 3x UPRO/i, (_, u) => `77% acciones · ${u} en UPRO 3x`],
      [/tecnología pesa el ([\d.]+%).*VTI/i, (_, t) => `39% en VTI · ${t} tecnología`],
      [/salario de (\$[\d,.]+) equivale al ([\d.]+%).*?(\$[\d,.]+) en RSU/i, (_, s, p, r) => `Sueldo = ${p} del patrimonio · ${r} RSU`],
      [/salario anual equivale al ([\d.]+%)/i, (_, p) => `Sueldo = ${p} del patrimonio neto`]
    ] : [
      [/run out at (\d+).*(\$[\d,.]+) gap/i, (_, a, g) => `Runs out at ${a} · ${g} gap`],
      [/hold (\$[\d,.]+).*?(\$[\d,.]+) of planned spending/i, (_, z, u) => `${z} in retirement · ${u} unpaid`],
      [/gap is (\$[\d,.]+).*?(\$[\d,.]+) a year more/i, (_, g, y) => `${g} gap · +${y}/yr needed`],
      [/cash of (\$[\d,.]+) covers about ([\d.]+) months/i, (_, c, m) => `${c} cash (${m} months)`],
      [/(\$[\d,.]+) of whole life.*against (\$[\d,.]+)/i, (_, h, r) => `${h} cover vs ${r} recommended`],
      [/Timothy is short (\$[\d,.]+) and Melanie (\$[\d,.]+)/i, (_, a, b) => `Short ${a} (Timothy) & ${b} (Melanie)`],
      [/shortfalls of (\$[\d,.]+) for Daniel and (\$[\d,.]+)/i, (_, a, b) => `Short ${a} (Daniel) & ${b} (Emily)`],
      [/(\$[\d,.]+) home and the (\$[\d,.]+) Porsche/i, (_, h, c) => `${h} home & ${c} Porsche uninsured`],
      [/recommended minimum is (\$[\d,.]+)/i, (_, m) => `${m} recommended · $0 today`],
      [/(\$[\d,.]+) gap.*liability/i, (_, m) => `${m} liability gap`],
      [/(\$[\d,.]+) gap\. Adding it is worth (\d+) points/i, (_, m, p) => `${m} gap (+${p} pts)`],
      [/net cash flow is (-\$[\d,.]+) a year/i, (_, f) => `${f}/yr negative cash flow`],
      [/(\$[\d,.]+) a year short/i, (_, f) => `-${f}/yr after expenses & savings`],
      [/free cash flow of (\$[\d,.]+) a year/i, (_, f) => `Only ${f}/yr free cash flow`],
      [/Amex Platinum balance is (\$[\d,.]+) at ([\d.]+%)/i, (_, b, r) => `${b} at ${r} APR`],
      [/(\$[\d,.]+) at ([\d.]+%) against (\$[\d,.]+)/i, (_, b, r, c) => `${b} at ${r} APR vs ${c} cash`],
      [/(\$[\d,.]+) card is the most expensive/i, (_, b) => `${b} card at 24.9% APR`],
      [/(\$[\d,.]+) more is possible.*(\$[\d,.]+) in tax/i, (_, r, s) => `+${r} 401(k) room · saves ${s}/yr`],
      [/(\$[\d,.]+) a year in an HSA.*up to (\$[\d,.]+)/i, (_, h, i) => `Up to ${h} HSA & ${i} IRA unused`],
      [/costs about (\$[\d,.]+) a year/i, (_, t) => `${t}/yr in investment tax drag`],
      [/tax saving.*about (\$[\d,.]+) a year/i, (_, s) => `Up to ${s}/yr tax savings`],
      [/(\$[\d,.]+) is still needed.*529/i, (_, g) => `${g} needed · $0 in 529`],
      [/(\$[\d,.]+) in 529s against a (\$[\d,.]+)/i, (_, b, g) => `${b} in 529 · ${g} gap`],
      [/(\$[\d,.]+) gap remains after the (\$[\d,.]+)/i, (_, g, b) => `${g} gap (${b} in 529)`],
      [/(\$[\d,.]+) sits above.*earns about ([\d.]+%)/i, (_, c, r) => `${c} idle earning ${r}`],
      [/only (\$[\d,.]+) sits above the reserve/i, (_, c) => `Only ${c} above reserve`],
      [/accessible cash of (\$[\d,.]+).*gap of (\$[\d,.]+)/i, (_, c, g) => `${c} cash · ${g} reserve gap`],
      [/(\$[\d,.]+) purchase.*(\$[\d,.]+) down payment/i, (_, h, d) => `${h} home · ${d} down payment`],
      [/([\d.]+%) stocks.*UPRO\) at (\$[\d,.]+)/i, (_, p, u) => `${p} stocks · ${u} in 3x UPRO`],
      [/cutting VTI from ([\d.]+%) to ([\d.]+%)/i, (_, a, b) => `VTI at ${a} (target ${b})`],
      [/(\$[\d,.]+) salary equals ([\d.]+%).*?(\$[\d,.]+) of RSUs/i, (_, s, p, r) => `Salary = ${p} of net worth · ${r} RSUs`],
      [/annual salary is ([\d.]+%)/i, (_, p) => `Salary = ${p} of net worth`]
    ];
    for (const [rx, rep] of metricRules) {
      const m = src.match(rx);
      if (m) { keyMetric = m[0].replace(rx, rep); break; }
    }
    if (!keyMetric) {
      // Generic fallback for any future unseen JSON: first 2 figures + short context, max 54 chars
      const nums = (raw.match(/-?\$[\d,.]+(?:[BMKT])?|\b\d+(?:\.\d+)?%/g) || []).slice(0, 2);
      const firstClause = (body || title).split(/[.;]/)[0].trim();
      keyMetric = firstClause.length <= 54
        ? firstClause
        : (nums.length ? `${nums.join(' · ')}` : firstClause.slice(0, 51) + '…');
    }
    return { shortTitle, keyMetric };
  }

  function humanizeConcernObject(item, lang) {
    const rawDetail = String((item && item.detail) || '');
    const cleaned = stripTechnicalMarkers(rawDetail);
    const { title: rawTitle, body: rawBody } = splitTitleAndBody(cleaned);
    const topic = detectTopic(cleaned);
    if (lang === 'EN') {
      const title = rawTitle || 'Plan priority';
      const body = rawBody || cleaned;
      const compact = compactConcern(title, body, cleaned, 'EN');
      return Object.assign({}, item, {
        topic,
        title,
        body,
        shortTitle: compact.shortTitle,
        keyMetric: compact.keyMetric,
        detail: body ? `**${title}.** ${body}` : `**${title}.**`
      });
    }
    const titleES = translateTitleToES(rawTitle || cleaned);
    const bodyES = translateBodyToES(rawBody);
    const compact = compactConcern(titleES, bodyES, cleaned, 'ES');
    return Object.assign({}, item, {
      topic,
      title: titleES,
      body: bodyES,
      shortTitle: compact.shortTitle,
      keyMetric: compact.keyMetric,
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
            title: everydayMoveTitle(m.title, 'EN'),
            topic: detectTopic((m.title || '') + ' ' + (m.action || ''))
          })),
          combined_moves: (score.combined_moves || []).map(m => Object.assign({}, m, {
            moves: (m.moves || []).map(x => everydayMoveTitle(x, 'EN'))
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
          title: everydayMoveTitle(m.title || `Medida prioritaria ${i + 1}`, 'ES'),
          action: translateBodyToES(m.action || m.title || ''),
          note: translateBodyToES(m.note || '')
        })),
        combined_moves: (score.combined_moves || []).map((m, i) => {
          const translatedMoves = (m.moves || []).map((x, j) => everydayMoveTitle(x || `Medida ${j + 1}`, 'ES'));
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
      const turn = state.coupleSyncMode === 'remote' ? (state.memberRole === 'B' ? 'B' : 'A') : (state.voteTurn === 'B' ? 'B' : 'A');
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
      const turn = state.coupleSyncMode === 'remote' ? (state.memberRole === 'B' ? 'B' : 'A') : (state.voteTurn === 'B' ? 'B' : 'A');
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

    const shortMoveTitle = bestSingle
      ? everydayMoveTitle(bestSingle.title || bestSingle.action, lang)
      : (es ? 'Medida principal' : 'Primary move');
    const shortImpactBase = compactMoveActionLine(bestSingle, scoreNow, lang);
    const shortImpactMetric = `${shortImpactBase}${bestCombined && bestCombined.score_after ? ` (${es ? 'hasta' : 'up to'} ${bestCombined.score_after})` : ''}`;
    const shortTakeaway = aligned
      ? (es
          ? `Tu #1 coincide con la acción que más mejora tu salud financiera (${singleDelta}). Empezamos aquí.`
          : `Your #1 matches the action that boosts your financial health most (${singleDelta}). Starting here.`)
      : (es
          ? `Punto ciego: te preocupa «${top1.shortTitle || top1.title}», pero «${shortMoveTitle}» mejora más tu plan (${singleDelta}).`
          : `Blind spot: "${top1.shortTitle || top1.title}" worries you, yet "${shortMoveTitle}" improves your plan most (${singleDelta}).`);

    return { top1, bestSingle, bestCombined, aligned, worryText, impactText, blindSpotText, shortMoveTitle, shortImpactMetric, shortTakeaway, topic: top1Topic };
  }

  // Build concise narrative reframe anchored to #1 priority and literal plan score
  function buildThermometerReframe(state, data) {
    const lang = langOf(state);
    const es = lang === 'ES';
    const contrast = buildContrastSummary(state, data);
    const top1 = contrast.top1;
    const score = (data.score && data.score.published_score) ?? 0;

    if (state.aiReframe && state.aiReframe.lang === lang && state.aiReframe.text) {
      return state.aiReframe.text;
    }

    if (es) {
      return `Score actual ${score}/100 · Empezamos por tu #1 («${top1.shortTitle || top1.title}») en este campamento.`;
    }
    return `Current score ${score}/100 · Starting with your #1 ("${top1.shortTitle || top1.title}") at this camp.`;
  }

  // Evaluate exact point along the painted sumi-e mountain ridge curve for any fraction in [0, 1]
  function trailPointAtFraction(fraction) {
    const f = Math.max(0, Math.min(1, Number(fraction) || 0));
    const n = TRAIL_SEGS.length;
    const seg = Math.min(n - 1, Math.floor(f * n));
    const localT = Math.max(0, Math.min(1, (f * n) - seg));
    const [p0, ctrl, p2] = TRAIL_SEGS[seg];
    const mt = 1 - localT;
    const x = mt * mt * p0[0] + 2 * mt * localT * ctrl[0] + localT * localT * p2[0];
    const y = mt * mt * p0[1] + 2 * mt * localT * ctrl[1] + localT * localT * p2[1];
    return [Math.round(x * 10) / 10, Math.round(y * 10) / 10];
  }

  // Build organic failure path: 24 smooth ridge steps from exact camp fraction to exhaustion age, then gravity cubic C drop
  function riskCoordinates(record, stagePoint, stageIdx) {
    const idx = Math.max(0, Math.min(3, Number(stageIdx) || 0));
    const [sx, sy] = stagePoint || biomes[idx].point;
    if (!record || !record.hasExhaustion) {
      const bx = Math.min(1140, Math.round(sx + 62 + idx * 8));
      const by = Math.min(685, Math.round(sy + 26));
      const c1x = Math.round(sx + (bx - sx) * 0.45);
      const c1y = Math.round(sy + 2);
      const c2x = Math.round(sx + (bx - sx) * 0.85);
      const c2y = Math.round(sy + (by - sy) * 0.45);
      return { sx, sy, rx: sx, ry: sy, x: bx, y: by, wall: true, d: `M ${sx} ${sy} C ${c1x} ${c1y} ${c2x} ${c2y} ${bx} ${by}` };
    }
    const startFrac = TRAIL_FRACS[idx] != null ? TRAIL_FRACS[idx] : idx / 3;
    const exhaustFrac = record.length > 1 ? record.index / (record.length - 1) : startFrac;
    const climbFrac = Math.max(startFrac + 0.08, Math.min(0.95, exhaustFrac));
    const steps = 24;
    const climbPts = [];
    for (let i = 0; i <= steps; i++) {
      const t = i / steps;
      const f = startFrac + (climbFrac - startFrac) * t;
      const [px, py] = trailPointAtFraction(f);
      const driftY = Math.round(4.8 * Math.pow(t, 1.45) * 10) / 10;
      climbPts.push([i === 0 ? sx : px, i === 0 ? sy : Math.round((py + driftY) * 10) / 10]);
    }
    const [rx, ry] = climbPts[climbPts.length - 1];
    const offsetSpread = idx * 18;
    const bx = Math.min(1130, Math.round(rx + 74 + offsetSpread));
    const by = Math.min(685, Math.round(ry + 92 + idx * 10));
    const c1x = Math.round(rx + (bx - rx) * 0.42);
    const c1y = Math.round(ry + 4);
    const c2x = Math.round(rx + (bx - rx) * 0.88);
    const c2y = Math.round(ry + (by - ry) * 0.38);
    const climbD = climbPts.map((pt, i) => `${i === 0 ? 'M' : 'L'} ${pt[0]} ${pt[1]}`).join(' ');
    const d = `${climbD} C ${c1x} ${c1y} ${c2x} ${c2y} ${bx} ${by}`;
    return { sx, sy, rx, ry, x: bx, y: by, wall: false, steps, climbFrac, exhaustFrac, d };
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

  function neutralAlternativeCopy(topic, lang) {
    const es = lang !== 'EN';
    const byTopic = es ? {
      protection: 'Mantener tus pólizas actuales y reservar ese dinero',
      debt: 'Seguir pagando la cuota habitual y conservar el efectivo',
      liquidity: 'Mantener tu ritmo actual y revisar la reserva más adelante',
      home_purchase: 'Priorizar liquidez a mano y aplazar cambios en el plan',
      retirement: 'Conservar tu ritmo actual de gastos y ajustar el próximo año',
      cash_flow: 'Mantener tu presupuesto actual sin recortar este año',
      investments: 'Conservar tu cartera actual sin mover posiciones'
    } : {
      protection: 'Keep your current policies and hold onto the cash',
      debt: 'Keep paying the usual monthly bill and hold your cash',
      liquidity: 'Keep your current pace and revisit cash reserves later',
      home_purchase: 'Prioritize cash on hand and adjust the plan later',
      retirement: 'Keep your current spending pace and adjust next year',
      cash_flow: 'Keep your current budget without trimming this year',
      investments: 'Keep your current portfolio mix without making changes'
    };
    return byTopic[topic] || (es ? 'Seguir con tu plan actual y revisarlo más adelante' : 'Stick with your current plan and review it later');
  }

  function stepGoodOption(state, data, s, stageIdx) {
    const lang = langOf(state);
    const es = lang === 'ES';
    const moves = orderedTopMoves(state, data);
    const top1 = primaryConcern(state, data);
    const scoreNow = (data.score && data.score.published_score) ?? 0;
    if (stageIdx < moves.length && moves[stageIdx]) {
      const m = moves[stageIdx];
      const topic = m.topic || detectTopic((m.title || '') + ' ' + (m.action || ''));
      const badOption = neutralAlternativeCopy(topic, lang);
      const shortFact = compactMoveActionLine(m, scoreNow, lang).split(' · ')[0];
      const before = m.score_before != null ? m.score_before : scoreNow;
      const after = m.score_after != null ? m.score_after : scoreNow;
      return {
        label: m.action || m.title || s.pact,
        title: m.title || m.action || s.pact,
        shortFact,
        badLabel: badOption,
        focusNote: stageIdx === 0 && top1 ? `${top1.shortTitle || top1.title}` : '',
        scoreBefore: before,
        scoreAfter: after,
        trend: `${t(state, 'trend')}: ${m.action || m.title} (${before} → ${after}).`
      };
    }
    const combined = (data.score && data.score.combined_moves) || [];
    if (combined.length) {
      const best = combined.reduce((a, b) => ((b.moves || []).length >= (a.moves || []).length ? b : a), combined[0]);
      const comboLabel = (best.moves || []).join(' + ') || best.title || s.pact;
      const before = best.score_before != null ? best.score_before : scoreNow;
      const after = best.score_after != null ? best.score_after : scoreNow;
      const badOption = es
        ? 'Aplicar solo cambios pequeños y dejar el resto para más adelante'
        : 'Make only small tweaks and leave the rest for later';
      return {
        label: `${comboLabel}${best.score_after != null ? ` (${before} → ${after})` : ''}`,
        title: shortWords(comboLabel, 6),
        shortFact: es ? 'Paquete combinado de medidas' : 'Combined priority package',
        badLabel: badOption,
        focusNote: '',
        scoreBefore: before,
        scoreAfter: after,
        trend: `${t(state, 'trend')}: ${comboLabel} (${before} → ${after}).`
      };
    }
    const pub = scoreNow;
    const fallbackBad = neutralAlternativeCopy('overview', lang);
    return { label: s.pact, title: shortWords(s.pact, 6), shortFact: '', badLabel: fallbackBad, focusNote: '', scoreBefore: pub, scoreAfter: pub, trend: `${t(state, 'trend')}: ${s.pact}` };
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

  // Multi-device couple room helpers & dual sync client (backend /api/rooms/* + localStorage + BroadcastChannel)
  function makeRoomId() {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    let out = 'SH-';
    for (let i = 0; i < 4; i++) out += chars[Math.floor(Math.random() * chars.length)];
    return out;
  }

  function readRoomParams() {
    try {
      const search = root.location && root.location.search ? root.location.search : '';
      const params = new URLSearchParams(search);
      const caseParam = params.get('case');
      const roomParam = params.get('room');
      const memberParam = String(params.get('member') || '').toUpperCase();
      return {
        caseId: caseParam && ids.includes(caseParam) ? caseParam : null,
        roomId: roomParam ? roomParam.trim() : null,
        memberRole: memberParam === 'B' ? 'B' : 'A',
        fromUrl: !!(roomParam || memberParam)
      };
    } catch (_) {
      return { caseId: null, roomId: null, memberRole: 'A', fromUrl: false };
    }
  }

  function buildPartnerUrl(state) {
    const other = state.memberRole === 'B' ? 'A' : 'B';
    const q = `?case=${encodeURIComponent(state.caseId)}&room=${encodeURIComponent(state.roomId || makeRoomId())}&member=${other}`;
    try {
      if (root.location && root.location.origin && root.location.origin !== 'null') {
        return `${root.location.origin}${root.location.pathname || '/'}${q}`;
      }
    } catch (_) {}
    return q;
  }

  function createCoupleRoomSync() {
    const memoryRooms = {};
    const listeners = {};
    let bc = null;
    try {
      if (root.document && typeof root.BroadcastChannel === 'function') {
        bc = new root.BroadcastChannel('sherpas-room');
      }
    } catch (_) {}

    const storageKey = roomId => `sherpas_room_${roomId}`;
    const emptyRoom = (roomId, caseId) => ({
      room_id: roomId,
      case_id: caseId || 'timothy-melanie-weah',
      evaluation: { A: null, B: null },
      evaluation_ready: false,
      decisions: {}
    });

    const normalizeRoom = (roomId, caseId, raw) => {
      const base = emptyRoom(roomId, caseId);
      if (!raw || typeof raw !== 'object') return base;
      const ev = raw.evaluation || {};
      const aEval = ev.A || null;
      const bEval = ev.B || null;
      const decs = {};
      const rawDecs = raw.decisions || {};
      for (const k of Object.keys(rawDecs)) {
        const d = rawDecs[k] || {};
        const hasA = !!d.A;
        const hasB = !!d.B;
        decs[String(k)] = {
          A: d.A || null,
          B: d.B || null,
          ready: !!(hasA && hasB),
          aligned: !!(hasA && hasB && d.A.route === d.B.route)
        };
      }
      return {
        room_id: raw.room_id || roomId,
        case_id: raw.case_id || caseId || base.case_id,
        evaluation: { A: aEval, B: bEval },
        evaluation_ready: !!(aEval && bEval),
        decisions: decs
      };
    };

    const mergeRooms = (roomId, caseId, a, b) => {
      const na = normalizeRoom(roomId, caseId, a);
      const nb = normalizeRoom(roomId, caseId, b);
      const mergedDecs = {};
      const keys = new Set([...Object.keys(na.decisions), ...Object.keys(nb.decisions)]);
      for (const k of keys) {
        const da = na.decisions[k] || {};
        const db = nb.decisions[k] || {};
        const voteA = db.A || da.A || null;
        const voteB = db.B || da.B || null;
        mergedDecs[k] = {
          A: voteA,
          B: voteB,
          ready: !!(voteA && voteB),
          aligned: !!(voteA && voteB && voteA.route === voteB.route)
        };
      }
      const evA = nb.evaluation.A || na.evaluation.A || null;
      const evB = nb.evaluation.B || na.evaluation.B || null;
      return {
        room_id: roomId,
        case_id: nb.case_id || na.case_id,
        evaluation: { A: evA, B: evB },
        evaluation_ready: !!(evA && evB),
        decisions: mergedDecs
      };
    };

    const readLocal = (roomId, caseId) => {
      let fromStorage = null;
      try {
        if (root.localStorage) {
          const txt = root.localStorage.getItem(storageKey(roomId));
          if (txt) fromStorage = JSON.parse(txt);
        }
      } catch (_) {}
      return mergeRooms(roomId, caseId, memoryRooms[roomId], fromStorage);
    };

    const notify = (roomId, data) => {
      const set = listeners[roomId];
      if (set) set.forEach(fn => { try { fn(data); } catch (_) {} });
    };

    const writeLocal = (roomId, caseId, data) => {
      const norm = normalizeRoom(roomId, caseId, data);
      memoryRooms[roomId] = norm;
      try {
        if (root.localStorage) root.localStorage.setItem(storageKey(roomId), JSON.stringify(norm));
      } catch (_) {}
      try {
        if (bc) bc.postMessage({ type: 'room-update', roomId, data: norm });
      } catch (_) {}
      notify(roomId, norm);
      return norm;
    };

    const canHttp = () => typeof root.fetch === 'function' && root.location && /^https?:$/i.test(root.location.protocol || '');

    const postJson = (url, body) => {
      if (!canHttp()) return Promise.resolve(null);
      try {
        const ctrl = typeof root.AbortController === 'function' ? new root.AbortController() : null;
        const timer = ctrl ? setTimeout(() => { try { ctrl.abort(); } catch (_) {} }, 1500) : null;
        return root.fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
          signal: ctrl ? ctrl.signal : undefined
        }).then(r => {
          if (timer) clearTimeout(timer);
          return r && r.ok ? r.json() : null;
        }).catch(() => {
          if (timer) clearTimeout(timer);
          return null;
        });
      } catch (_) {
        return Promise.resolve(null);
      }
    };

    const getJson = url => {
      if (!canHttp()) return Promise.resolve(null);
      try {
        const ctrl = typeof root.AbortController === 'function' ? new root.AbortController() : null;
        const timer = ctrl ? setTimeout(() => { try { ctrl.abort(); } catch (_) {} }, 1500) : null;
        return root.fetch(url, { signal: ctrl ? ctrl.signal : undefined }).then(r => {
          if (timer) clearTimeout(timer);
          return r && r.ok ? r.json() : null;
        }).catch(() => {
          if (timer) clearTimeout(timer);
          return null;
        });
      } catch (_) {
        return Promise.resolve(null);
      }
    };

    if (bc) {
      bc.onmessage = ev => {
        const msg = ev && ev.data;
        if (msg && msg.type === 'room-update' && msg.roomId) {
          const merged = mergeRooms(msg.roomId, msg.data && msg.data.case_id, memoryRooms[msg.roomId], msg.data);
          memoryRooms[msg.roomId] = merged;
          notify(msg.roomId, merged);
        }
      };
    }
    if (typeof root.addEventListener === 'function') {
      root.addEventListener('storage', ev => {
        if (!ev || !ev.key || !ev.key.startsWith('sherpas_room_') || !ev.newValue) return;
        const rid = ev.key.slice('sherpas_room_'.length);
        try {
          const parsed = JSON.parse(ev.newValue);
          const merged = mergeRooms(rid, parsed && parsed.case_id, memoryRooms[rid], parsed);
          memoryRooms[rid] = merged;
          notify(rid, merged);
        } catch (_) {}
      });
    }

    return {
      readLocal,
      createRoom(caseId, roomId) {
        const rid = roomId || makeRoomId();
        const cur = readLocal(rid, caseId);
        writeLocal(rid, caseId, cur);
        postJson('/api/rooms', { case_id: caseId, room_id: rid }).then(res => {
          if (res && res.room_id) writeLocal(rid, caseId, mergeRooms(rid, caseId, readLocal(rid, caseId), res));
        });
        return cur;
      },
      submitEvaluation(roomId, caseId, member, vote) {
        const m = member === 'B' ? 'B' : 'A';
        const cur = readLocal(roomId, caseId);
        const payload = {
          member: m,
          top_fears: Array.isArray(vote.fears) ? vote.fears.slice(0, 3) : (Array.isArray(vote.top_fears) ? vote.top_fears.slice(0, 3) : []),
          fears: Array.isArray(vote.fears) ? vote.fears.slice(0, 3) : (Array.isArray(vote.top_fears) ? vote.top_fears.slice(0, 3) : []),
          thermometer: Number(vote.thermometer) || 3,
          priority: vote.priority || 'deuda-proteccion',
          subjective: vote.subjective || ''
        };
        cur.evaluation[m] = payload;
        cur.evaluation_ready = !!(cur.evaluation.A && cur.evaluation.B);
        const saved = writeLocal(roomId, caseId, cur);
        postJson(`/api/rooms/${encodeURIComponent(roomId)}/evaluation`, payload).then(res => {
          if (res) writeLocal(roomId, caseId, mergeRooms(roomId, caseId, readLocal(roomId, caseId), res));
        });
        return saved;
      },
      submitDecision(roomId, caseId, member, stage, route, label) {
        const m = member === 'B' ? 'B' : 'A';
        const stKey = String(Number(stage) || 0);
        const cur = readLocal(roomId, caseId);
        const entry = cur.decisions[stKey] || { A: null, B: null, ready: false, aligned: false };
        entry[m] = { route: route === 'bad' ? 'bad' : 'good', label: label || '' };
        entry.ready = !!(entry.A && entry.B);
        entry.aligned = !!(entry.ready && entry.A.route === entry.B.route);
        cur.decisions[stKey] = entry;
        const saved = writeLocal(roomId, caseId, cur);
        postJson(`/api/rooms/${encodeURIComponent(roomId)}/decision`, {
          member: m,
          stage: Number(stage) || 0,
          route: entry[m].route,
          label: entry[m].label
        }).then(res => {
          if (res) writeLocal(roomId, caseId, mergeRooms(roomId, caseId, readLocal(roomId, caseId), res));
        });
        return saved;
      },
      fetchRoom(roomId, caseId) {
        const local = readLocal(roomId, caseId);
        return getJson(`/api/rooms/${encodeURIComponent(roomId)}`).then(res => {
          if (res) return writeLocal(roomId, caseId, mergeRooms(roomId, caseId, local, res));
          return local;
        });
      },
      subscribe(roomId, caseId, onUpdate) {
        if (!roomId || typeof onUpdate !== 'function') return () => {};
        if (!listeners[roomId]) listeners[roomId] = new Set();
        listeners[roomId].add(onUpdate);
        let timer = null;
        if (canHttp()) {
          timer = setInterval(() => {
            getJson(`/api/rooms/${encodeURIComponent(roomId)}`).then(res => {
              if (res) {
                const merged = mergeRooms(roomId, caseId, readLocal(roomId, caseId), res);
                memoryRooms[roomId] = merged;
                onUpdate(merged);
              }
            });
          }, 1800);
        }
        return () => {
          if (listeners[roomId]) listeners[roomId].delete(onUpdate);
          if (timer) clearInterval(timer);
        };
      }
    };
  }
  const CoupleRoomSync = createCoupleRoomSync();

  // Per-profile evaluation persistence (localStorage + in-memory fallback)
  const memoryProfileEvals = {};
  const ProfileEvalStore = {
    key: id => `sherpas_profile_eval_${id}`,
    load(caseId) {
      if (!caseId) return null;
      try {
        if (root.localStorage) {
          const raw = root.localStorage.getItem(this.key(caseId));
          if (raw) {
            const parsed = JSON.parse(raw);
            if (parsed && parsed.evaluationDone) {
              memoryProfileEvals[caseId] = parsed;
              return parsed;
            }
          }
        }
      } catch (_) {}
      const mem = memoryProfileEvals[caseId];
      return mem && mem.evaluationDone ? mem : null;
    },
    save(caseId, state) {
      if (!caseId || !state) return null;
      const record = {
        evaluationDone: true,
        fearOrder: Array.isArray(state.fearOrder) ? state.fearOrder.slice(0, 3) : [],
        votes: state.votes && typeof state.votes === 'object' ? JSON.parse(JSON.stringify(state.votes)) : {},
        priority: state.priorityFocus || '',
        updatedAt: Date.now()
      };
      memoryProfileEvals[caseId] = record;
      try {
        if (root.localStorage) root.localStorage.setItem(this.key(caseId), JSON.stringify(record));
      } catch (_) {}
      return record;
    },
    clear(caseId) {
      if (!caseId) return;
      delete memoryProfileEvals[caseId];
      try {
        if (root.localStorage) root.localStorage.removeItem(this.key(caseId));
      } catch (_) {}
    }
  };

  function createInitialState(id) {
    const lang = loadLang();
    const urlParams = readRoomParams();
    const resolvedId = ids.includes(id) ? id : (urlParams.caseId || ids[0]);
    const roomId = urlParams.roomId || makeRoomId();
    const memberRole = urlParams.memberRole || 'A';
    const savedEval = ProfileEvalStore.load(resolvedId);
    const joiningUnfinishedPartnerRoom = !!(
      urlParams.fromUrl &&
      urlParams.roomId &&
      urlParams.memberRole === 'B' &&
      !CoupleRoomSync.readLocal(urlParams.roomId, resolvedId).evaluation_ready
    );
    const skipEval = !!(savedEval && savedEval.evaluationDone && !joiningUnfinishedPartnerRoom);
    return {
      caseId: resolvedId,
      view: viewName('expedition', lang, 0),
      phase: skipEval ? 'expedition' : 'fears',
      evaluationDone: skipEval,
      mode: 'Plain',
      lang,
      irlDay: 0,
      fearOrder: skipEval ? (savedEval.fearOrder || []).slice(0, 3) : [],
      priorityFocus: skipEval ? (savedEval.priority || '') : '',
      showAllConcerns: false,
      thermometer: 3,
      subjectiveConcern: '',
      votes: skipEval && savedEval.votes ? JSON.parse(JSON.stringify(savedEval.votes)) : {},
      voteTurn: memberRole,
      roomId,
      memberRole,
      coupleSyncMode: 'remote',
      roomWaiting: false,
      roomCopied: false,
      roomDecisions: {},
      animatedCoupleKeys: {},
      roomAlignedBanner: false,
      timerStartedAt: null,
      aiReframe: null,
      aiPact: null,
      aiBrief: null,
      stage: 0,
      focusedNode: 0,
      hasEnteredCamp: false,
      activeBiome: null,
      inspectedRisk: null,
      cameraMode: 'panoramic',
      dialogVisible: false,
      blocked: false,
      history: [],
      advisorDoubts: [],
      summit: false
    };
  }

  // The Sumi-e mountain is ALWAYS the 100vw x 100vh full-bleed background across the entire web app
  const isMountainPhase = state => !!state && (viewKey(state.view) === 'expedition' || viewKey(state.view) === 'overview') && (state.phase === 'expedition' || state.phase === 'blocked' || state.summit);

  // Gentle camera framing (~1.82x over 1200x750) keeping mountain context visible
  function campCamera(stage) {
    const idx = Math.max(0, Math.min(3, Number(stage) || 0));
    const pt = biomes[idx].point;
    const w = 660, h = 412;
    const cx = idx === 3 ? pt[0] + 14 : pt[0];
    const cy = idx === 3 ? pt[1] - 14 : pt[1];
    const x = Math.max(0, Math.min(fullCamera[2] - w, cx - w * 0.55));
    const y = Math.max(0, Math.min(fullCamera[3] - h, cy - h * 0.45));
    return [x, y, w, h];
  }

  function riskCameraBox(record, stagePoint, stageIdx) {
    const coord = riskCoordinates(record, stagePoint, stageIdx);
    const w = 696, h = 435;
    const x = Math.max(0, Math.min(fullCamera[2] - w, coord.x - w * 0.55));
    const y = Math.max(0, Math.min(fullCamera[3] - h, coord.y - h * 0.45));
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
        ? `<path d="M ${coord.x} ${coord.y - 9} L ${coord.x} ${coord.y + 9}" stroke="#9E2A2B" stroke-width="1.35" stroke-linecap="round"/>`
        : `<circle cx="${coord.rx}" cy="${coord.ry}" r="2.1" fill="#9E2A2B" opacity=".88"/>`;
      return `<g class="risk-group" data-risk-stage="${originIdx}" data-risk-index="${idx}">
        <path class="risk-path" pathLength="1000" data-active-risk="${isLatest ? 'true' : 'false'}" data-risk-break="${coord.x},${coord.y}" data-exhaustion="${record && record.hasExhaustion ? 'true' : 'false'}" data-year="${record && record.year ? record.year : ''}" data-age="${record && record.age != null ? record.age : ''}" data-investable-assets="${record && record.investable_assets != null ? record.investable_assets : ''}" d="${coord.d}" fill="none" stroke="#9E2A2B" stroke-linecap="round" stroke-linejoin="round" stroke-width="${isInspected ? '2.2' : '1.8'}" opacity="${isInspected ? '0.96' : '0.86'}"/>
        ${stopWall}
        <g class="risk-node ${isInspected ? 'is-active' : ''}" data-action="inspect-risk" data-risk-index="${idx}" data-risk-stage="${originIdx}" transform="translate(${coord.x} ${coord.y})" role="button" tabindex="0" aria-label="${esc(nodeLabel)}">
          <circle class="risk-hit" cx="0" cy="0" r="16" fill="transparent"/>
          <circle class="risk-node-halo" cx="0" cy="0" r="${isInspected ? '6.5' : '5'}" fill="#9E2A2B" opacity="${isInspected ? '0.26' : '0.16'}"/>
          <circle cx="0" cy="0" r="3.1" fill="#9E2A2B" stroke="#ffffff" stroke-width="0.9"/>
          <text x="5.5" y="1.2" fill="#9E2A2B" font-size="3.4" font-weight="600" font-family="system-ui">${esc(nodeLabel)}</text>
        </g>
      </g>`;
    }).join('');

    const partners = couple
      ? `<path id="partnerRopeA" class="partner-rope" d="${TRAIL_PATH}" transform="translate(-1.4 -1)" stroke="var(--partner-a)" stroke-width="1.35" stroke-dasharray="${TRAIL_LENGTH}" stroke-dashoffset="${activeOffset}" opacity="${activeOffset < TRAIL_LENGTH ? '.72' : '0'}"/><path id="partnerRopeB" class="partner-rope" d="${TRAIL_PATH}" transform="translate(1.4 1)" stroke="var(--partner-b)" stroke-width="1.35" stroke-dasharray="${TRAIL_LENGTH}" stroke-dashoffset="${activeOffset}" opacity="${activeOffset < TRAIL_LENGTH ? '.72' : '0'}"/>`
      : '';

    const campNodes = [
      `<g class="micro-camp ${activeStage === 0 ? 'is-active' : ''} ${activeStage > 0 ? 'is-reached' : ''}" data-action="focus-node" data-node="0" transform="translate(312 491)">
        <circle class="camp-hit" cx="0" cy="0" r="18" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="7.5"/>
        <path class="camp-tent" d="M -3.2 1.8 L 0 -3.8 L 3.2 1.8 Z" fill="#ffffff" stroke="#141414" stroke-width="0.65" stroke-linejoin="round"/>
        <text x="0" y="9.5" text-anchor="middle" font-size="3.6" font-family="system-ui" font-weight="600" fill="#141414" opacity=".82">${esc(shortLabels[0])} · 2,800m</text>
      </g>`,
      `<g class="micro-camp ${activeStage === 1 ? 'is-active' : ''} ${activeStage > 1 ? 'is-reached' : ''}" data-action="focus-node" data-node="1" transform="translate(564 382)">
        <circle class="camp-hit" cx="0" cy="0" r="18" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="7.5"/>
        <path class="camp-tent" d="M -3.2 1.8 L 0 -3.8 L 3.2 1.8 Z" fill="#ffffff" stroke="#141414" stroke-width="0.65" stroke-linejoin="round"/>
        <text x="0" y="9.5" text-anchor="middle" font-size="3.6" font-family="system-ui" font-weight="600" fill="#141414" opacity=".82">${esc(shortLabels[1])} · 4,600m</text>
      </g>`,
      `<g class="micro-camp ${activeStage === 2 ? 'is-active' : ''} ${activeStage > 2 ? 'is-reached' : ''}" data-action="focus-node" data-node="2" transform="translate(684 319)">
        <circle class="camp-hit" cx="0" cy="0" r="18" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="7.5"/>
        <path class="camp-tent" d="M -3.4 1.8 Q 0 -4.2 3.4 1.8 Z" fill="#ffffff" stroke="#141414" stroke-width="0.65"/>
        <text x="0" y="9.5" text-anchor="middle" font-size="3.6" font-family="system-ui" font-weight="600" fill="#141414" opacity=".82">${esc(shortLabels[2])} · 6,900m</text>
      </g>`,
      `<g class="micro-camp ${activeStage === 3 ? 'is-active' : ''}" data-action="focus-node" data-node="3" transform="translate(858 145)">
        <circle class="camp-hit" cx="0" cy="0" r="18" fill="transparent"/>
        <circle class="camp-beacon" cx="0" cy="0" r="7.5"/>
        <circle cx="0" cy="0" r="2.2" fill="#141414" opacity=".82"/>
        <text x="0" y="9.5" text-anchor="middle" font-size="3.6" font-family="system-ui" font-weight="700" fill="#141414" opacity=".88">${esc(shortLabels[3])} · 8,848m</text>
      </g>`
    ].join('');

    const peopleInit = (opts && Array.isArray(opts.people) && opts.people.length >= 2)
      ? [String(opts.people[0] || 'A').charAt(0).toUpperCase(), String(opts.people[1] || 'B').charAt(0).toUpperCase()]
      : ['A', 'B'];
    const climber = couple
      ? `<g id="climberMarker" class="climber-rig" data-cx="${x}" data-cy="${y}">
          <g id="climberMarkerA" class="climber-member" transform="translate(${x - 4} ${y})">
            <circle cx="0" cy="0" r="6" fill="var(--partner-a)" opacity=".18"/>
            <circle cx="0" cy="0" r="4" fill="var(--partner-a)" stroke="#ffffff" stroke-width="1.15"/>
            <text x="0" y="1.3" text-anchor="middle" fill="#ffffff" font-size="3.6" font-weight="700" font-family="system-ui">${esc(peopleInit[0])}</text>
          </g>
          <g id="climberMarkerB" class="climber-member" transform="translate(${x + 4} ${y})">
            <circle cx="0" cy="0" r="6" fill="var(--partner-b)" opacity=".18"/>
            <circle cx="0" cy="0" r="4" fill="var(--partner-b)" stroke="#ffffff" stroke-width="1.15"/>
            <text x="0" y="1.3" text-anchor="middle" fill="#ffffff" font-size="3.6" font-weight="700" font-family="system-ui">${esc(peopleInit[1])}</text>
          </g>
        </g>`
      : `<g id="climberMarker" class="climber-rig" transform="translate(${x} ${y})" data-cx="${x}" data-cy="${y}">
          <circle cx="0" cy="0" r="5.5" fill="#141414" opacity=".16"/>
          <circle cx="0" cy="0" r="3.1" fill="#141414" stroke="#ffffff" stroke-width="1.2"/>
        </g>`;

    const activeBiome = (opts && Object.prototype.hasOwnProperty.call(opts, 'activeBiome'))
      ? (opts.activeBiome && BIOME_ASSETS[opts.activeBiome] ? opts.activeBiome : null)
      : null;
    const biomeLayers = BIOME_ORDER.map(id => {
      const isActive = activeBiome === id;
      return `<image id="biomeLayer-${id}" class="mountain-biome-layer${isActive ? ' is-active' : ''}" data-biome-layer="${id}" href="${BIOME_ASSETS[id]}" x="0" y="38" width="1200" height="675" preserveAspectRatio="xMidYMid meet"/>`;
    }).join('\n        ');

    return `<svg class="mountain-svg" data-camera="mountain" viewBox="${initialBox}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="${lang === 'EN' ? 'Sumi-e mountain expedition route' : 'Ruta de montaña sumi-e de la expedición'}">
      <defs>
        <filter id="dryBrush" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="3" result="noise"/>
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="1.8" xChannelSelector="R" yChannelSelector="G"/>
        </filter>
      </defs>
      <g id="cameraRig">
        <image id="sumiMountainArt" class="mountain-art-base${activeBiome ? ' is-covered' : ''}" href="assets/mountain-sumi.jpg" x="0" y="38" width="1200" height="675" preserveAspectRatio="xMidYMid meet"/>
        ${biomeLayers}
        <path class="route-guide" d="${TRAIL_PATH}" stroke-width="1.4" filter="url(#dryBrush)"/>
        <path id="activeTrail" class="route-ink" d="${TRAIL_PATH}" stroke-width="2.5" stroke-dasharray="${TRAIL_LENGTH}" stroke-dashoffset="${activeOffset}" filter="url(#dryBrush)"/>
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

  const formatUSD = n => {
    const num = Math.round(Number(n) || 0);
    return `${num < 0 ? '-' : ''}$${Math.abs(num).toLocaleString('en-US')}`;
  };

  const formatRatePct = rate => {
    const pct = Number(rate) * 100;
    if (!Number.isFinite(pct) || pct <= 0) return '0%';
    const rounded = Math.round(pct * 10) / 10;
    return `${Number.isInteger(rounded) ? rounded.toFixed(0) : rounded.toFixed(1)}%`;
  };

  const PILLAR_META = [
    { key: 'liquidity', match: /liq/i, ES: 'Liquidez', EN: 'Liquidity' },
    { key: 'cashflow', match: /cash|sav/i, ES: 'Flujo de caja', EN: 'Cash flow' },
    { key: 'debt', match: /debt/i, ES: 'Deuda', EN: 'Debt' },
    { key: 'protection', match: /insur|prot/i, ES: 'Protección', EN: 'Protection' },
    { key: 'investments', match: /inv/i, ES: 'Inversión', EN: 'Investments' }
  ];

  function canonicalPillarKey(name) {
    const s = String(name || '');
    const found = PILLAR_META.find(m => m.match.test(s));
    return found ? found.key : 'investments';
  }

  function explainerSection(explainer, heading) {
    if (!explainer) return '';
    const re = new RegExp(`##\\s*${heading}\\s*\\n([\\s\\S]*?)(?=\\n##\\s|$)`, 'i');
    const m = String(explainer).match(re);
    return m ? m[1] : '';
  }

  function pillarSubline(key, data, lang) {
    const es = lang !== 'EN';
    const exp = (data && data.score && data.score.explainer) || '';
    const facts = (data && data.facts) || {};
    const ratios = facts.ratios || {};
    const prot = facts.protection || {};

    if (key === 'liquidity') {
      const sec = explainerSection(exp, 'Liquidity');
      const mCashAndLiq = sec.match(/about\s+([\d.]+)\s+months[\s\S]*?total liquid assets cover about\s+([\d.]+)\s+months/i);
      if (mCashAndLiq) {
        return es
          ? `${mCashAndLiq[1]} meses en caja · ${mCashAndLiq[2]} meses líquidos`
          : `${mCashAndLiq[1]} months in cash · ${mCashAndLiq[2]} liquid months`;
      }
      const mAfterGoals = sec.match(/covering\s+([\d.]+)\s+months[\s\S]*?falls to\s+([\d.]+)\s+months/i);
      if (mAfterGoals) {
        return es
          ? `${mAfterGoals[1]} meses en caja · ${mAfterGoals[2]} tras metas`
          : `${mAfterGoals[1]} months in cash · ${mAfterGoals[2]} after goals`;
      }
      const mThin = sec.match(/Cash is\s+(\$[\d,]+),\s+about\s+([\d.]+)\s+months/i);
      if (mThin) {
        return es
          ? `${mThin[2]} meses en caja (${mThin[1]})`
          : `${mThin[2]} months in cash (${mThin[1]})`;
      }
      const ef = ratios.emergencyFund || {};
      const months = ef.emergencyFundMonths != null ? ef.emergencyFundMonths : (prot.emergencyFund && prot.emergencyFund.emergencyFundCoverageEvaluation && prot.emergencyFund.emergencyFundCoverageEvaluation.monthsCovered);
      const cashAmt = ef.emergencyFund != null ? ef.emergencyFund : (prot.emergencyFund && prot.emergencyFund.cashAndExpensesOverview && prot.emergencyFund.cashAndExpensesOverview.cashReserves);
      const minM = ef.minRecommendedEFMonths;
      if (months != null) {
        const mNum = Number(months);
        const mWord = es ? (mNum === 1 ? 'mes' : 'meses') : (mNum === 1 ? 'month' : 'months');
        const targetPart = minM ? (es ? ` vs. ${minM} meses` : ` vs. ${minM} months`) : '';
        return es
          ? `${months} ${mWord} en caja (${formatUSD(cashAmt)})${targetPart}`
          : `${months} ${mWord} in cash (${formatUSD(cashAmt)})${targetPart}`;
      }
      return '';
    }

    if (key === 'cashflow') {
      const sec = explainerSection(exp, 'Cash flow');
      const mRet = sec.match(/Retirement saving is about\s+([\d.]+%)\s+of income/i);
      if (mRet) {
        return es ? `${mRet[1]} de ingresos a jubilación` : `${mRet[1]} of income to retirement`;
      }
      const mDraw = sec.match(/Withdrawals run at about\s+([\d.]+%)\s+of investable assets[\s\S]*?([\d.]+%)\s+sustainable/i);
      if (mDraw) {
        return es ? `Retiros al ${mDraw[1]} vs. ${mDraw[2]} sostenible` : `${mDraw[1]} withdrawals vs. ${mDraw[2]} sustainable`;
      }
      const mSavNone = sec.match(/savings rate is\s+([\d.]+%),\s+but retirement accounts receive none/i);
      if (mSavNone) {
        return es ? `Ahorro ${mSavNone[1]} · 0% a jubilación` : `${mSavNone[1]} savings rate · 0% to retirement`;
      }
      const sl = ratios.savingsLevel || {};
      if (sl.ratio != null) {
        const pct = (Number(sl.ratio) * 100).toFixed(1).replace(/\.0$/, '');
        return es
          ? `Ahorro ${pct}% (${formatUSD(sl.savingAmount)}/año)`
          : `${pct}% savings (${formatUSD(sl.savingAmount)}/yr)`;
      }
      return '';
    }

    if (key === 'debt') {
      const sec = explainerSection(exp, 'Debt');
      if (/has no debt/i.test(sec)) {
        return es ? 'Sin deudas · DTI 0%' : 'No debt · 0% DTI';
      }
      const mUseApr = sec.match(/revolving use is\s+([\d.]+%)\s+at an\s+([\d.]+%)\s+rate/i);
      if (mUseApr) {
        return es ? `Tarjeta al ${mUseApr[2]} (${mUseApr[1]} de uso)` : `Card at ${mUseApr[2]} APR (${mUseApr[1]} use)`;
      }
      const mApr = sec.match(/revolving card balance at\s+([\d.]+%)\s+APR/i);
      if (mApr) {
        return es ? `Pagos manejables · tarjeta al ${mApr[1]}` : `Manageable payments · ${mApr[1]} APR card`;
      }
      const dti = ratios.debtToIncome && ratios.debtToIncome.debtOnlyDti != null
        ? `${(Number(ratios.debtToIncome.debtOnlyDti) * 100).toFixed(1).replace(/\.0$/, '')}%`
        : null;
      const debts = ((facts.debtManagement && facts.debtManagement.listOfDebts) || []).slice(1).filter(r => Number(r[2]) > 0);
      const topApr = debts.reduce((max, r) => Math.max(max, Number(r[3]) || 0), 0);
      if (debts.length === 0) return es ? 'Sin deudas · DTI 0%' : 'No debt · 0% DTI';
      if (dti && topApr >= 0.15) {
        return es ? `DTI ${dti} · tarjeta al ${formatRatePct(topApr)}` : `${dti} DTI · ${formatRatePct(topApr)} APR card`;
      }
      if (dti) return es ? `DTI ${dti}` : `${dti} DTI`;
      return '';
    }

    if (key === 'investments') {
      const sec = explainerSection(exp, 'Investing');
      const mVti = sec.match(/VTI[^\n]*?([\d.]+%)\s+of investable assets/i);
      const mGlide = sec.match(/Growth assets are about\s+([\d.]+%)[\s\S]*?([\d.]+%)\s+glide target/i);
      if (mVti && mGlide) {
        return es
          ? `VTI ${mVti[1]} · ${mGlide[1]} crecimiento vs. ${mGlide[2]} objetivo`
          : `VTI ${mVti[1]} · ${mGlide[1]} growth vs. ${mGlide[2]} target`;
      }
      const mMix = sec.match(/invested mix is about\s+([\d.]+%)\s+growth/i);
      if (mVti && mMix) {
        return es
          ? `VTI ${mVti[1]} · ${mMix[1]} en crecimiento`
          : `VTI ${mVti[1]} · ${mMix[1]} growth mix`;
      }
      if (mVti && /Growth is a large share/i.test(sec)) {
        return es
          ? `VTI ${mVti[1]} · alta exposición a crecimiento`
          : `VTI ${mVti[1]} · high growth exposure`;
      }
      const invAmt = ratios.investableAssetLevel && ratios.investableAssetLevel.investableAssets;
      const eqTarget = facts.assetsAndInvestments && facts.assetsAndInvestments.retirementGlidePath && facts.assetsAndInvestments.retirementGlidePath.retirementGlideEquityForClient;
      if (invAmt != null && eqTarget != null) {
        const eqPct = `${Math.round(Number(eqTarget) * 100)}%`;
        return es
          ? `${formatUSD(invAmt)} invertidos · objetivo ${eqPct} acciones`
          : `${formatUSD(invAmt)} invested · ${eqPct} equity target`;
      }
      return '';
    }

    if (key === 'protection') {
      const sec = explainerSection(exp, 'Protection');
      const mMort = sec.match(/([\d.]+%)\s+mortality ratio|mortality ratio is\s+([\d.]+%)/i);
      const mortPct = mMort ? (mMort[1] || mMort[2]) : null;
      const noUmbrella = /no umbrella|none now/i.test(sec);
      const hasUmbrella = /umbrella policy is in place/i.test(sec);
      const uninsuredHome = /home[\s\S]*?uninsured/i.test(sec);
      if (mortPct && hasUmbrella && uninsuredHome) {
        return es
          ? `Vida ${mortPct} + paraguas · hogar/auto sin póliza`
          : `Life ${mortPct} + umbrella · home/auto uninsured`;
      }
      if (mortPct && noUmbrella) {
        return es
          ? `Cobertura vida al ${mortPct} · sin paraguas`
          : `Life cover at ${mortPct} · no umbrella`;
      }
      const li = ratios.lifeInsurance || {};
      const cov = (Number(li.clientCoverage) || 0) + (Number(li.coClientCoverage) || 0);
      const rec = (Number(li.recommendedClientMinCoverage) || 0) + (Number(li.recommendedCoClientMinCoverage) || 0);
      const umb = ratios.umbrella || {};
      const hasU = Number(umb.currentCoverage) > 0;
      if (rec > 0) {
        const pct = `${Math.round((cov / rec) * 100)}%`;
        return es
          ? `Cobertura vida al ${pct} · ${hasU ? 'con paraguas' : 'sin paraguas'}`
          : `Life cover at ${pct} · ${hasU ? 'umbrella active' : 'no umbrella'}`;
      }
      return '';
    }
    return '';
  }

  function shortDebtLabel(rawName, rawType, lang) {
    const es = lang !== 'EN';
    const name = String(rawName || '').trim();
    const type = String(rawType || '').toLowerCase();
    if (/mortgage/i.test(type) || /mortgage/i.test(name)) return es ? 'Hipoteca' : 'Mortgage';
    if (/student/i.test(type) || /student/i.test(name)) return es ? 'Estudios' : 'Student loan';
    if (/vehicle/i.test(type) || /\b(tesla|bmw|toyota|car|auto)\b/i.test(name)) return es ? 'Vehículo' : 'Vehicle loan';
    if (/credit card/i.test(type) || /\bcc\b/i.test(name)) {
      if (/^chase\s+cc$/i.test(name)) return es ? 'Tarjeta Chase' : 'Chase card';
      return name;
    }
    return name || (es ? 'Deuda' : 'Debt');
  }

  function backpackIconSvg(size) {
    const s = size || 18;
    return `<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M9 6V5a3 3 0 0 1 6 0v1"/>
      <path d="M6 10a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v9a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-9Z"/>
      <path d="M6 13H4.5A1.5 1.5 0 0 0 3 14.5v3A1.5 1.5 0 0 0 4.5 19H6"/>
      <path d="M18 13h1.5a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5H18"/>
      <path d="M9 10h6"/>
      <rect x="9" y="13.5" width="6" height="4.5" rx="1"/>
    </svg>`;
  }

  function renderPackPopover(state, data) {
    const lang = langOf(state);
    const es = lang !== 'EN';
    const facts = (data && data.facts) || {};
    const nw = facts.netWorthStatement || {};
    const netTotal = (nw.netWorth && nw.netWorth.total) || 0;
    const assetsObj = nw.assets || {};
    const assetsTotal = assetsObj.total || 0;
    const liabObj = nw.liabilities || {};
    const liabTotal = liabObj.total || 0;

    const byName = {};
    let otherAssets = 0;
    (assetsObj.items || []).forEach(item => {
      const val = Number(item && item.total) || 0;
      if (val <= 0) return;
      if (item.name === 'Cash account' || item.name === 'Investment account' || item.name === 'Real estate') {
        byName[item.name] = (byName[item.name] || 0) + val;
      } else {
        otherAssets += val;
      }
    });

    const assetRows = [
      { label: es ? 'Efectivo' : 'Cash', val: byName['Cash account'] || 0 },
      { label: es ? 'Inversiones' : 'Investments', val: byName['Investment account'] || 0 },
      { label: es ? 'Vivienda' : 'Real estate', val: byName['Real estate'] || 0 },
      { label: es ? 'Vehículos y otros' : 'Vehicles & other', val: otherAssets }
    ].filter(r => r.val > 0);

    const rawDebts = ((facts.debtManagement && facts.debtManagement.listOfDebts) || []).slice(1);
    const activeDebts = rawDebts
      .map(r => ({
        name: shortDebtLabel(r[0], r[1], lang),
        balance: Number(r[2]) || 0,
        rate: Number(r[3]) || 0
      }))
      .filter(d => d.balance > 0)
      .sort((a, b) => b.balance - a.balance);

    const debtRowsHtml = activeDebts.length
      ? activeDebts.map(d => {
          const rateCls = d.rate >= 0.15 ? 'pack-apr is-high-apr' : 'pack-apr';
          return `<div class="pack-row">
            <span class="pack-row-label">${esc(d.name)} <span class="pack-sep">·</span> <span class="${rateCls}">${esc(formatRatePct(d.rate))}</span></span>
            <span class="pack-row-val">${esc(formatUSD(d.balance))}</span>
          </div>`;
        }).join('')
      : `<div class="pack-row is-empty">
          <span class="pack-row-label">${es ? 'Sin deudas pendientes' : 'No outstanding debt'}</span>
          <span class="pack-row-val">$0</span>
        </div>`;

    const cf = facts.cashflowStatement || {};
    const inflowsTotal = (cf.inflows && cf.inflows.total) || 0;
    const savingsItem = ((cf.outflows && cf.outflows.items) || []).find(it => it && it.name === 'Savings');
    const savingsTotal = (savingsItem && Number(savingsItem.total)) || 0;
    const yrSuffix = es ? '/año' : '/yr';
    const footerParts = [`${es ? 'Ingresos' : 'Income'} ${formatUSD(inflowsTotal)}${yrSuffix}`];
    if (savingsTotal > 0) {
      footerParts.push(`${es ? 'Ahorro' : 'Savings'} ${formatUSD(savingsTotal)}${yrSuffix}`);
    }

    return `<div class="pack-popover" role="dialog" aria-label="${es ? 'Tu mochila · Balance real' : 'Your pack · Real balance'}" data-overlay="pack">
      <div class="pack-head">
        <div class="pack-title-wrap">
          ${backpackIconSvg(18)}
          <span class="pack-title">${es ? 'Tu mochila' : 'Your pack'}</span>
        </div>
        <div class="pack-net">
          <span class="pack-net-kicker">${es ? 'Patrimonio neto' : 'Net worth'}</span>
          <span class="pack-net-val"><span class="pack-net-prefix">${es ? 'Neto' : 'Net'}</span> <strong>${esc(formatUSD(netTotal))}</strong></span>
        </div>
      </div>
      <div class="pack-section">
        <div class="pack-section-head">
          <span>${es ? 'Lo que tienes' : 'What you own'}</span>
          <strong>${esc(formatUSD(assetsTotal))}</strong>
        </div>
        <div class="pack-rows">
          ${assetRows.map(r => `<div class="pack-row">
            <span class="pack-row-label">${esc(r.label)}</span>
            <span class="pack-row-val">${esc(formatUSD(r.val))}</span>
          </div>`).join('')}
        </div>
      </div>
      <div class="pack-section">
        <div class="pack-section-head">
          <span>${es ? 'Lo que debes' : 'What you owe'}</span>
          <strong>${esc(formatUSD(liabTotal))}</strong>
        </div>
        <div class="pack-rows">
          ${debtRowsHtml}
        </div>
      </div>
      <div class="pack-footer">${esc(footerParts.join(' · '))}</div>
    </div>`;
  }

  function renderHealthModal(state, data) {
    const lang = langOf(state);
    const es = lang !== 'EN';
    const household = (data && data.meta && data.meta.household) || state.caseId;
    const score = (data && data.score) || {};
    const published = score.published_score != null ? score.published_score : 0;

    const byKey = {};
    (score.pillars || []).forEach(p => {
      byKey[canonicalPillarKey(p.pillar)] = Math.max(0, Math.min(100, Number(p.score) || 0));
    });

    const radarItems = PILLAR_META.map(m => ({
      key: m.key,
      label: m[lang],
      score: byKey[m.key] != null ? byKey[m.key] : 0,
      subline: pillarSubline(m.key, data, lang)
    }));

    const cx = 190;
    const cy = 158;
    const maxR = 98;
    const pt = (idx, frac) => {
      const angle = (-90 + idx * 72) * (Math.PI / 180);
      return [cx + Math.cos(angle) * maxR * frac, cy + Math.sin(angle) * maxR * frac];
    };
    const ringPolys = [0.2, 0.4, 0.6, 0.8, 1].map(f => {
      const pts = [0, 1, 2, 3, 4].map(i => pt(i, f).map(v => v.toFixed(1)).join(',')).join(' ');
      return `<polygon points="${pts}" fill="none" stroke="#E2E8F0" stroke-width="1"/>`;
    }).join('');
    const axesLines = [0, 1, 2, 3, 4].map(i => {
      const [x, y] = pt(i, 1);
      return `<line x1="${cx}" y1="${cy}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" stroke="#E2E8F0" stroke-width="1"/>`;
    }).join('');

    const dataPts = radarItems.map((it, i) => pt(i, it.score / 100));
    const dataPoly = dataPts.map(p => p.map(v => v.toFixed(1)).join(',')).join(' ');
    const dataDots = dataPts.map(p => `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="3.5" fill="#4A5D75"/>`).join('');

    const labelCoords = [
      { dx: 0, dy: -14, anchor: 'middle' },
      { dx: 12, dy: 4, anchor: 'start' },
      { dx: 8, dy: 18, anchor: 'start' },
      { dx: -8, dy: 18, anchor: 'end' },
      { dx: -12, dy: 4, anchor: 'end' }
    ];
    const radarLabels = radarItems.map((it, i) => {
      const [vx, vy] = pt(i, 1);
      const cfg = labelCoords[i];
      return `<text x="${(vx + cfg.dx).toFixed(1)}" y="${(vy + cfg.dy).toFixed(1)}" text-anchor="${cfg.anchor}" class="health-radar-label">${esc(it.label)}</text>`;
    }).join('');

    const sortedPillars = radarItems.slice().sort((a, b) => b.score - a.score);
    const listHtml = sortedPillars.map(it => {
      const dotColor = it.score >= 75 ? '#2E9E75' : it.score >= 45 ? '#D4A04A' : '#E07A68';
      return `<li class="health-pillar-item">
        <div class="health-pillar-main">
          <span class="health-dot" style="background:${dotColor}" aria-hidden="true"></span>
          <span class="health-pillar-name">${esc(it.label)}</span>
          <span class="health-pillar-score">${esc(it.score)}</span>
        </div>
        ${it.subline ? `<p class="health-pillar-sub">${esc(it.subline)}</p>` : ''}
      </li>`;
    }).join('');

    return `<div class="health-modal-backdrop" data-overlay="health" role="dialog" aria-modal="true" aria-label="${esc(household)} · ${es ? 'Salud financiera' : 'Financial health'}">
      <div class="health-modal-card">
        <div class="health-modal-head">
          <h2 class="health-modal-title">${esc(household)} <span class="health-title-sep">·</span> ${es ? 'Salud financiera' : 'Financial health'}</h2>
          <div class="health-modal-head-right">
            <span class="health-score-badge"><strong>${esc(published)}</strong> <span>/ 100</span></span>
            <button type="button" class="health-close-btn" data-action="close-overlay" aria-label="${es ? 'Cerrar' : 'Close'}">×</button>
          </div>
        </div>
        <div class="health-modal-body">
          <div class="health-radar-col">
            <svg class="health-radar-svg" viewBox="0 0 380 310" role="img" aria-label="${es ? 'Pentágono de 5 pilares de salud financiera' : '5-pillar financial health radar'}">
              ${ringPolys}
              ${axesLines}
              <polygon points="${dataPoly}" fill="rgba(74, 93, 117, 0.28)" stroke="#4A5D75" stroke-width="1.75" stroke-linejoin="round"/>
              ${dataDots}
              ${radarLabels}
            </svg>
          </div>
          <ul class="health-pillars-list">
            ${listHtml}
          </ul>
        </div>
      </div>
    </div>`;
  }

  function telegramRadioUrl(state) {
    const cleanPart = (val, fallback) => {
      const s = String(val || '').trim().replace(/\s+/g, '_').replace(/[^A-Za-z0-9_-]/g, '');
      return s || fallback;
    };
    const casePart = cleanPart(state && state.caseId, 'demo');
    const voterRaw = (state && Array.isArray(state.voters) && state.voters[0]) ? state.voters[0] : '';
    const voterPart = cleanPart(voterRaw, 'client');
    return `https://t.me/SherpasRadioBot?start=${`${casePart}_${voterPart}`.slice(0, 64)}`;
  }

  function renderHeader(state, data) {
    const lang = langOf(state);
    const es = lang !== 'EN';
    const view = viewKey(state.view);
    const basecampActive = view === 'expedition' || view === 'overview';
    const dayActive = view === 'current';
    const briefActive = view === 'brief';
    const packOpen = state.openOverlay === 'pack';
    const healthOpen = state.openOverlay === 'health';
    const options = ids.map(id => `<option value="${id}" ${id === state.caseId ? 'selected' : ''}>${esc(((dataFor(id) || {}).meta || {}).household || id)}</option>`).join('');

    const currentLabel = dayLabel(lang, state.irlDay);
    const briefTitle = words[lang].brief;
    const radioTitle = es ? 'Sintonizar Radio en Telegram' : 'Tune Radio on Telegram';
    const radioHref = telegramRadioUrl(state);
    const packAria = es ? 'Tu mochila · Balance real' : 'Your pack · Real balance';
    const redoAria = es ? 'Rehacer encuesta de miedos' : 'Redo priorities survey';
    const healthLabel = es ? 'Salud' : 'Health';

    return `<header class="site-header header-floating">
      <a class="brand" href="#" data-action="nav" data-view="Basecamp">sherpas</a>
      <select class="case-select" aria-label="${t(state, 'select')}" data-case>${options}</select>
      <div class="pack-anchor">
        <button type="button" class="pack-btn ${packOpen ? 'is-active' : ''}" data-action="toggle-pack" aria-expanded="${packOpen ? 'true' : 'false'}" aria-haspopup="dialog" aria-label="${esc(packAria)}" title="${esc(packAria)}">
          ${backpackIconSvg(18)}
        </button>
        ${packOpen ? renderPackPopover(state, data) : ''}
      </div>
      <button type="button" class="redo-survey-btn" data-action="redo-eval" aria-label="${esc(redoAria)}" title="${esc(redoAria)}">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
      </button>
      <nav class="site-nav" aria-label="${t(state, 'nav')}">
        <button type="button" class="health-pill-btn ${healthOpen ? 'is-active' : ''}" data-action="toggle-health" aria-expanded="${healthOpen ? 'true' : 'false'}" aria-haspopup="dialog">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12h4l2.5-6 4 12 2.5-6H21"/></svg>
          <span>${esc(healthLabel)}</span>
        </button>
        <button class="nav-tab ${basecampActive ? 'active' : ''}" data-action="nav" data-view="Basecamp">Basecamp</button>
        <button class="nav-tab ${dayActive ? 'active' : ''}" data-action="nav" data-view="${esc(currentLabel)}">${esc(currentLabel)}</button>
        <button class="nav-icon-btn ${briefActive ? 'active' : ''}" data-action="nav" data-view="${esc(briefTitle)}" title="${esc(briefTitle)}" aria-label="${esc(briefTitle)}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12h6M9 16h4"/></svg>
        </button>
        <a class="nav-icon-btn" href="${esc(radioHref)}" target="_blank" rel="noopener noreferrer" title="${esc(radioTitle)}" aria-label="${esc(radioTitle)}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5M19.1 4.9C23 8.8 23 15.2 19.1 19.1"/><circle cx="12" cy="12" r="2"/></svg>
        </a>
      </nav>
      <div class="language-toggle" aria-label="${lang === 'ES' ? 'Idioma' : 'Language'}">
        <button data-action="lang" data-lang="ES" class="${lang === 'ES' ? 'active' : ''}">ES</button>
        <button data-action="lang" data-lang="EN" class="${lang === 'EN' ? 'active' : ''}">EN</button>
      </div>
    </header>${healthOpen ? renderHealthModal(state, data) : ''}`;
  }

  function renderRiskInspectionCard(state, data, persona, s, riskIdx) {
    const lang = langOf(state);
    const es = lang === 'ES';
    const entries = buildHistoryEntries(state.history, state.blocked, state.stage);
    const entry = entries[Math.max(0, Math.min(entries.length - 1, Number(riskIdx) || 0))] || { stage: state.stage };
    const originStage = Math.max(0, Math.min(3, Number(entry.stage) || 0));
    const shortLabels = campShorts[lang];
    const campTitle = `${shortLabels[originStage]} · ${campAlts[originStage]}`;
    const goodMove = stepGoodOption(state, data, s, originStage);
    const rec = riskRecord(state.caseId, lang);
    const heading = rec.hasExhaustion
      ? `${rec.year}${rec.age != null ? (es ? ` · edad ${rec.age}` : ` · age ${rec.age}`) : ''}`
      : `${es ? 'Brecha en' : 'Gap at'} ${campTitle}`;
    const oneLineImpact = rec.hasExhaustion
      ? `${es ? 'Activos invertibles' : 'Investable assets'} ${exactMoney(rec.investable_assets)} · ${es ? 'omitiste' : 'skipped'} ${shortWords(goodMove.title, 5)}`
      : `${es ? 'Sin agotamiento anual · omitiste' : 'No yearly depletion · skipped'} ${shortWords(goodMove.title, 5)} (${goodMove.scoreBefore} → ${goodMove.scoreAfter})`;
    const tensionsHtml = (persona.tensions || []).map(x => `<p>${detail(x.id, x, lang)}</p>`).join('') || `<p>${esc(persona.D3 || '')}</p>`;
    const compactMath = mathSummary(data, state)
      .replace('<details class="exact-math">', '<details class="exact-math compact-math">')
      .replace(`<summary>${t(state, 'exact')}</summary>`, `<summary>${es ? 'Cálculo' : 'Math'}</summary>`)
      .replace('<ul>', `<div class="exact-context-notes"><p><strong>${campTitle}:</strong> ${esc(goodMove.label)}</p>${tensionsHtml}</div><ul>`);

    return `<aside class="floating-dialog compact-card" data-dialog="blocked">
      <div class="floating-dialog-head">
        <span class="camp-line-title is-risk">${esc(heading)}</span>
        <button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button>
      </div>
      <div class="crack compact-crack">
        <span class="blocked-impact">${esc(oneLineImpact)}</span>
      </div>
      <div class="dialog-footer-bar">
        ${compactMath}
        ${state.blocked
          ? `<button class="primary" data-action="rewind">${t(state, 'rewind')}</button>`
          : `<button class="primary" data-action="focus-active">${t(state, 'focusActive')}</button>`}
      </div>
    </aside>`;
  }

  // Compact multi-device room bar for couples
  function renderCoupleRoomBar(state, s, couple) {
    if (!couple) return '';
    const people = (state.voters && state.voters.length ? state.voters : s.people) || ['A', 'B'];
    const role = state.memberRole === 'B' ? 'B' : 'A';
    const me = people[role === 'B' ? 1 : 0] || people[0];
    const partner = people[role === 'B' ? 0 : 1] || people[1] || 'B';
    const isRemote = state.coupleSyncMode !== 'local';
    if (!isRemote) {
      return `<div class="room-bar is-local">
        <span class="room-badge"><span class="room-dot is-${role.toLowerCase()}"></span>${t(state, 'sameDevice')}</span>
        <button type="button" class="room-btn-ghost" data-action="toggle-sync-mode">${t(state, 'twoDevices')}</button>
      </div>`;
    }
    return `<div class="room-bar" data-room="${esc(state.roomId || '')}" data-member="${role}">
      <span class="room-badge"><span class="room-dot is-${role.toLowerCase()}"></span>${t(state, 'youAre')} <strong>${esc(me)}</strong> <small class="room-code">${esc(state.roomId || '')}</small></span>
      <div class="room-bar-actions">
        <button type="button" class="room-btn" data-action="copy-room-link">${state.roomCopied ? t(state, 'copied') : `${t(state, 'copyLinkFor')} ${esc(partner)}`}</button>
        <button type="button" class="room-btn-ghost" data-action="open-partner-tab">${t(state, 'openPartnerTab')} ${esc(partner)} ${t(state, 'inNewTab')}</button>
        <button type="button" class="room-btn-ghost" data-action="toggle-sync-mode">${t(state, 'sameDevice')}</button>
      </div>
    </div>`;
  }

  // Render Phase 1A: Ultra-scannable 2x3 centered grid with Top-3 ranking, minimalist thermometer, optional 1-line note, and unified couple multi-device / local turn
  function renderEvaluationOverlay(state, data, persona, s, couple) {
    const lang = langOf(state);
    const es = lang === 'ES';
    const isRemoteCouple = couple && state.coupleSyncMode !== 'local';
    const turn = isRemoteCouple ? (state.memberRole === 'B' ? 'B' : 'A') : (state.voteTurn === 'B' ? 'B' : 'A');
    const people = (state.voters && state.voters.length ? state.voters : s.people) || ['A', 'B'];
    const currentPerson = people[turn === 'B' ? 1 : 0] || people[0];
    const partnerPerson = people[turn === 'B' ? 0 : 1] || people[1] || 'B';
    const top3 = activeTop3(state);
    const thermo = activeThermometer(state);
    const rankLabels = words[lang].rankBadge;
    const turnVotes = (couple && state.votes && state.votes[turn]) || {};
    const currentPriority = turnVotes.priority || state.priorityFocus || 'deuda-proteccion';
    const currentSubjective = couple ? (turnVotes.subjective != null ? turnVotes.subjective : '') : (state.subjectiveConcern || '');
    const allConcerns = persona.objectiveConcerns || [];
    const roomBarHtml = renderCoupleRoomBar(state, s, couple);

    if (isRemoteCouple && state.roomWaiting === 'eval') {
      const myChips = top3.map((id, i) => {
        const found = allConcerns.find(x => x.id === id);
        return `<span class="top3-chip"><strong>${esc(rankLabels[i])}</strong> ${esc(found ? (found.shortTitle || found.title) : id)}</span>`;
      }).join(' ');
      return `<aside class="floating-panel eval-overlay" data-phase="fears" data-waiting="eval">
        ${roomBarHtml}
        <div class="room-wait-box">
          <p class="eyebrow">${t(state, 'team')}</p>
          <h1>${t(state, 'waitingFor')} ${esc(partnerPerson)}...</h1>
          <p class="compact-line">${t(state, 'waitingEvalSub')}</p>
          <div class="top3-chips">${myChips}</div>
          <div class="button-row">
            <button type="button" class="primary" data-action="copy-room-link">${state.roomCopied ? t(state, 'copied') : `${t(state, 'copyLinkFor')} ${esc(partnerPerson)}`}</button>
            <button type="button" data-action="open-partner-tab">${t(state, 'openPartnerTab')} ${esc(partnerPerson)} ${t(state, 'inNewTab')}</button>
            <button type="button" data-action="toggle-sync-mode">${t(state, 'sameDevice')}</button>
          </div>
        </div>
      </aside>`;
    }

    const cardsHtml = allConcerns.map(c => {
      const rankIdx = top3.indexOf(c.id);
      const isSelected = rankIdx >= 0;
      const badgeText = isSelected ? rankLabels[rankIdx] : words[lang].pickRank;
      const rankClass = isSelected ? `is-selected is-rank-${rankIdx + 1}` : '';
      return `<div class="concern-card ${rankClass}" data-action="toggle-concern" data-concern-id="${esc(c.id)}" role="button" tabindex="0" aria-pressed="${isSelected ? 'true' : 'false'}">
        <input type="checkbox" class="sr-only" data-fear="${esc(c.id)}" ${isSelected ? 'checked' : ''} tabindex="-1" aria-hidden="true">
        <div class="concern-card-head">
          <span class="concern-title">${esc(c.shortTitle || c.title)}</span>
          <span class="rank-badge ${rankClass}" data-rank="${isSelected ? rankIdx + 1 : ''}">${esc(badgeText)}</span>
        </div>
        <span class="concern-metric">${esc(c.keyMetric || '')}</span>
      </div>`;
    }).join('');

    const thermoButtons = [1, 2, 3, 4, 5].map(lvl => {
      const active = thermo === lvl;
      return `<button type="button" class="thermo-pill ${active ? 'active' : ''}" data-action="set-thermometer" data-level="${lvl}" aria-pressed="${active ? 'true' : 'false'}">${esc(thermoLabels[lang][lvl])}</button>`;
    }).join('');

    const coupleHeader = couple
      ? `<div class="couple-turn-banner" data-turn="${turn}">
          <span class="turn-pill">${isRemoteCouple ? `${t(state, 'youAre')} <strong>${esc(currentPerson)}</strong>` : `${es ? `Turno ${turn === 'A' ? '1/2' : '2/2'}` : `Turn ${turn === 'A' ? '1/2' : '2/2'}`} · <strong>${esc(currentPerson)}</strong>`}</span>
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
          const found = allConcerns.find(x => x.id === id);
          return `<span class="top3-chip"><strong>${esc(rankLabels[i])}</strong> ${esc(found ? (found.shortTitle || found.title) : id)}</span>`;
        }).join(' ')
      : `<span class="top3-empty">${t(state, 'fearHelp')}</span>`;

    const primaryCtaLabel = couple
      ? (isRemoteCouple ? t(state, 'submitEval') : (turn === 'A' ? `${t(state, 'save')} ${esc(partnerPerson)}` : t(state, 'matches')))
      : t(state, 'continue');

    return `<aside class="floating-panel eval-overlay" data-phase="fears">
      ${roomBarHtml}
      <div class="eval-head">
        <div>
          <p class="eyebrow">${couple ? t(state, 'team') : t(state, 'fears')}</p>
          <h1>${couple ? `${esc(currentPerson)} · ${t(state, 'fearTitle')}` : t(state, 'fearTitle')}</h1>
        </div>
        <div class="top3-status" aria-live="polite">
          <div class="top3-chips">${selectedSummary}</div>
        </div>
      </div>
      ${coupleHeader}
      <div class="concerns-grid" role="group" aria-label="${t(state, 'fearTitle')}">
        ${cardsHtml}
      </div>
      <div class="eval-actions">
        ${mathSummary(data, state)}
        <div class="button-row">
          <button class="primary" data-action="next-fears">${esc(primaryCtaLabel)}</button>
        </div>
      </div>
    </aside>`;
  }

  // Render Pre-Basecamp Contrast & Couple Diagnosis screen: 100% visible without scroll, extended text folded inside <details>
  function renderContrastOverlay(state, data, persona, s, couple) {
    const lang = langOf(state);
    const es = lang === 'ES';
    const contrast = buildContrastSummary(state, data);
    const reframeText = buildThermometerReframe(state, data);
    const rankLabels = words[lang].rankBadge;
    const allConcerns = persona.objectiveConcerns || [];
    const top3Ids = (state.fearOrder || []).slice(0, 3);
    const top3Html = top3Ids.map((id, i) => {
      const c = allConcerns.find(x => x.id === id);
      return `<span class="top3-chip"><strong>${esc(rankLabels[i] || `#${i + 1}`)}</strong> ${esc(c ? (c.shortTitle || c.title) : id)}</span>`;
    }).join(' ');

    let coupleRowHtml = '';
    let coupleDetailsHtml = '';
    if (couple) {
      const a = (state.votes && state.votes.A) || { fears: top3Ids, thermometer: state.thermometer || 3, priority: 'crecimiento' };
      const b = (state.votes && state.votes.B) || { fears: top3Ids, thermometer: state.thermometer || 3, priority: 'deuda-proteccion' };
      const people = (state.voters && state.voters.length ? state.voters : s.people) || ['A', 'B'];
      const ownersMeta = ((data.meta && data.meta.owners) || []);
      const profLabel = p => {
        if (!es) return p || 'Moderate';
        return { Growth: 'Crecimiento', Moderate: 'Moderado', Aggressive: 'Agresivo', Conservative: 'Conservador' }[p] || p || 'Moderado';
      };
      const profA = profLabel(ownersMeta[0] && ownersMeta[0].risk_profile);
      const profB = profLabel(ownersMeta[1] && ownersMeta[1].risk_profile);
      const thermoA = Number(a.thermometer) || 3;
      const thermoB = Number(b.thermometer) || 3;
      const common = (a.fears || []).filter(id => (b.fears || []).includes(id));
      const sharedChips = common.length
        ? common.map(id => {
            const c = allConcerns.find(x => x.id === id);
            return `<span class="top3-chip">${esc(c ? (c.shortTitle || c.title) : id)}</span>`;
          }).join(' ')
        : `<span class="top3-chip">${es ? 'Protección familiar' : 'Family protection'}</span>`;

      const pactText = (state.aiPact && state.aiPact.lang === lang && state.aiPact.text) || s.pact;

      coupleRowHtml = `<div class="couple-diagnosis-grid">
        <div class="contrast-card">
          <p class="eyebrow">${t(state, 'agree')}</p>
          <div class="top3-chips">${sharedChips}</div>
        </div>
        <div class="contrast-card">
          <p class="eyebrow">${t(state, 'thermoGapTitle')}</p>
          <p class="compact-line"><strong>${esc(people[0])}</strong> (${esc(profA)}) vs <strong>${esc(people[1])}</strong> (${esc(profB)})</p>
          <p class="compact-sub"><strong>${t(state, 'pact')}:</strong> ${esc(pactText)}</p>
        </div>
      </div>`;

      coupleDetailsHtml = `<p><strong>${t(state, 'profileSplitTitle')}:</strong> ${esc(persona.D4Human || '')}</p>`
        + (persona.tensions || []).map(x => `<p>${detail(x.id, x, lang)}</p>`).join('');
    } else {
      coupleDetailsHtml = (persona.tensions || []).map(x => `<p>${detail(x.id, x, lang)}</p>`).join('');
    }

    const exactBlock = mathSummary(data, state).replace(
      '<ul>',
      `<div class="exact-context-notes"><p>${esc(contrast.worryText)}</p><p>${esc(contrast.impactText)}</p><p>${esc(reframeText)}</p>${coupleDetailsHtml}</div><ul>`
    );

    return `<aside class="floating-panel eval-overlay contrast-compact" data-phase="contrast">
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
          <h2>${esc(contrast.top1.shortTitle || contrast.top1.title)}</h2>
          <p class="compact-line">${esc(contrast.top1.keyMetric || '')}</p>
        </div>
        <div class="contrast-card is-impact">
          <p class="eyebrow">${t(state, 'whatImpacts')}</p>
          <h2>${esc(contrast.shortMoveTitle)}</h2>
          <p class="compact-line">${esc(contrast.shortImpactMetric)}</p>
        </div>
      </div>
      <div class="contrast-callout" data-ai-reframe>
        <strong>${t(state, 'blindSpot')}:</strong> ${esc(contrast.shortTakeaway)}
      </div>
      ${coupleRowHtml}
      <div class="eval-actions">
        ${exactBlock}
        <div class="button-row">
          <button class="primary" data-action="start-expedition">${t(state, 'enter')}</button>
          <button data-action="edit-fears">${t(state, 'backEval')}</button>
        </div>
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

    const resolvedBiome = resolveActiveBiome(state);
    const hasTransitionFrom = hasRaf() && Object.prototype.hasOwnProperty.call(state, '_biomeTransitionFrom');
    const renderedBiome = hasTransitionFrom ? state._biomeTransitionFrom : resolvedBiome;

    const wallpaper = `<div class="mountain-stage mountain-fullscreen ${state.blocked ? 'storm-shake' : ''}" data-biome="${renderedBiome || 'none'}" data-dialog-ready="${dialogVisible ? 'true' : 'false'}">
      ${svgMarkup(state.summit ? 0 : stage.offset, state.summit ? biomes[3].point : stage.point, state.history || [], state.blocked, couple, state.votes, fail, lang, { stage: state.summit ? 3 : stageIdx, initialViewBox: initBox, inspectedRisk: activeRiskIdx, people: s.people, activeBiome: renderedBiome })}
    </div>`;

    const contrast = buildContrastSummary(state, data);
    const rankLabels = words[lang].rankBadge;
    const top3Summary = (state.fearOrder || []).slice(0, 3).map((id, i) => {
      const c = (persona.objectiveConcerns || []).find(x => x.id === id);
      return `${rankLabels[i] || `#${i + 1}`} ${c ? c.title : id}`;
    }).join(' · ') || contrast.top1.title;
    const thermoText = thermoLabels[lang][activeThermometer(state)];

    let panel = '';
    const campFab = `<button type="button" class="floating-overview-cta ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'is-hidden'}" data-action="focus-active" title="${esc(t(state, 'focusActive'))}" aria-label="${esc(t(state, 'focusActive'))}" ${state.cameraMode === 'panoramic' && !dialogVisible ? '' : 'hidden'}><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 20h18M4.5 20L12 5l7.5 15M12 5V3M9.5 20l2.5-6 2.5 6"/></svg></button>`;

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
        <div class="button-row">
          <button type="button" class="room-btn-ghost" data-action="redo-eval">${t(state, 'redoEval')}</button>
        </div>
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
        + campFab;
    } else {
      const inspectingOther = (focusedIdx !== stageIdx) || state.summit || view === 'overview';
      const focusedMove = stepGoodOption(state, data, s, focusedIdx);
      const activeMove = stepGoodOption(state, data, s, stageIdx);
      const campRiskIdx = entries.findIndex(e => Number(e.stage) === focusedIdx);
      const es = lang === 'ES';
      const campLineTitle = `${shortLabels[stageIdx]} · ${campAlts[stageIdx]}`;
      const focusedLineTitle = `${shortLabels[focusedIdx]} · ${campAlts[focusedIdx]}`;
      const compactMath = mathSummary(data, state)
        .replace('<details class="exact-math">', '<details class="exact-math compact-math">')
        .replace(`<summary>${t(state, 'exact')}</summary>`, `<summary>${es ? 'Cálculo' : 'Math'}</summary>`);
      const isRemoteCouple = couple && state.coupleSyncMode !== 'local';
      const roomBarCampHtml = isRemoteCouple ? renderCoupleRoomBar(state, s, couple) : '';
      const stageDec = (state.roomDecisions && state.roomDecisions[String(stageIdx)]) || null;
      const peopleNames = (state.voters && state.voters.length ? state.voters : s.people) || ['A', 'B'];
      const myRole = state.memberRole === 'B' ? 'B' : 'A';
      const partnerName = peopleNames[myRole === 'B' ? 0 : 1] || 'B';
      const myStageVote = stageDec && stageDec[myRole];
      const showPathCompare = isRemoteCouple && stageDec && stageDec.ready && (!stageDec.aligned || stageDec.A.route === 'bad' || stageDec.B.route === 'bad');
      const showDecisionWait = isRemoteCouple && state.roomWaiting === 'decision' && myStageVote && !(stageDec && stageDec.ready);

      let activeCampBody = '';
      if (showDecisionWait) {
        activeCampBody = `${roomBarCampHtml}
          <div class="floating-dialog-head"><span class="camp-line-title">${esc(campLineTitle)}</span><button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
          <p class="compact-line"><strong>${t(state, 'waitingFor')} ${esc(partnerName)}...</strong></p>
          <p class="compact-sub">${t(state, 'yourChoice')}: ${esc(shortWords(myStageVote.label || (myStageVote.route === 'bad' ? t(state, 'riskRoute') : t(state, 'safeRoute')), 8))}</p>
          <div class="button-row">
            <button type="button" class="primary" data-action="copy-room-link">${state.roomCopied ? t(state, 'copied') : `${t(state, 'copyLinkFor')} ${esc(partnerName)}`}</button>
            <button type="button" data-action="open-partner-tab">${t(state, 'openPartnerTab')} ${esc(partnerName)} ${t(state, 'inNewTab')}</button>
          </div>`;
      } else if (showPathCompare) {
        const aIsBad = stageDec.A.route === 'bad';
        const bIsBad = stageDec.B.route === 'bad';
        const nextCampName = shortLabels[Math.min(3, stageIdx + 1)];
        const failShort = fail && fail.hasExhaustion
          ? (es ? `cayó en ${fail.year}` : `dropped in ${fail.year}`)
          : (es ? 'tomó el desvío de riesgo' : 'took the risk deviation');
        const aSummary = aIsBad ? failShort : (es ? `siguió hacia ${nextCampName}` : `climbed to ${nextCampName}`);
        const bSummary = bIsBad ? failShort : (es ? `siguió hacia ${nextCampName}` : `climbed to ${nextCampName}`);
        activeCampBody = `${roomBarCampHtml}
          <div class="floating-dialog-head"><span class="camp-line-title">${t(state, 'pathCompareTitle')} · ${esc(campLineTitle)}</span><button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
          <div class="path-compare-grid">
            <div class="path-card ${aIsBad ? 'is-risk' : 'is-safe'}">
              <span class="path-badge ${aIsBad ? 'is-risk' : 'is-safe'}">${esc(peopleNames[0])}</span>
              <p class="compact-sub">${esc(aSummary)}</p>
            </div>
            <div class="path-card ${bIsBad ? 'is-risk' : 'is-safe'}">
              <span class="path-badge ${bIsBad ? 'is-risk' : 'is-safe'}">${esc(peopleNames[1])}</span>
              <p class="compact-sub">${esc(bSummary)}</p>
            </div>
          </div>
          <div class="button-row">
            <button class="primary" data-action="room-agree-good">${t(state, 'agreeAdvance')}</button>
            <button data-action="rewind">${t(state, 'rewind')}</button>
          </div>`;
      } else {
        const goodText = activeMove.shortFact
          ? `${activeMove.title} · ${activeMove.shortFact}`
          : activeMove.title;
        const badText = activeMove.badLabel || neutralAlternativeCopy('overview', lang);
        const caseIdx = Math.max(0, ids.indexOf(state.caseId));
        const flipOrder = ((stageIdx + caseIdx) % 2) === 1;
        const optionsPair = flipOrder
          ? [{ value: 'bad', text: badText }, { value: 'good', text: goodText }]
          : [{ value: 'good', text: goodText }, { value: 'bad', text: badText }];
        const optionsHtml = optionsPair.map((opt, idx) => `<label class="choice choice-compact"><input type="radio" name="route" value="${opt.value}" ${idx === 0 ? 'checked' : ''}><span class="choice-text">${esc(opt.text)}</span></label>`).join('');
        activeCampBody = `${roomBarCampHtml}
           <div class="floating-dialog-head"><span class="camp-line-title">${esc(campLineTitle)}</span><button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
           ${state.roomAlignedBanner ? `<div class="focus-priority-pill">${t(state, 'alignedAdvancing')}</div>` : ''}
           <div class="choice-list compact-choices">
             ${optionsHtml}
           </div>
           <div class="dialog-footer-bar">
             ${compactMath}
             <button class="primary" data-action="advance">${es ? 'Confirmar' : 'Confirm'}</button>
           </div>`;
      }

      const dialogContent = inspectingOther
        ? `<div class="floating-dialog-head"><span class="camp-line-title">${esc(focusedLineTitle)}</span><button class="dialog-close-btn" data-action="zoom-out">${t(state, 'panoramic')}</button></div>
           <p class="compact-line"><strong>${esc(focusedMove.title)}</strong>${focusedMove.shortFact ? ` · ${esc(focusedMove.shortFact)}` : ''} <span class="score-pill">${esc(focusedMove.scoreBefore)} → ${esc(focusedMove.scoreAfter)}</span></p>
           ${campRiskIdx >= 0 ? `<div class="crack compact-crack">${esc(fail.label)} <button class="link-toggle-btn" data-action="inspect-risk" data-risk-index="${campRiskIdx}">${t(state, 'seeRedBranch')}</button></div>` : ''}
           <div class="dialog-footer-bar">
             ${compactMath}
             <div class="button-row compact-row">
               ${!state.summit && focusedIdx !== stageIdx ? `<button class="primary" data-action="focus-active">${t(state, 'focusActive')}</button>` : ''}
               ${state.summit ? `<button data-action="repeat">${t(state, 'repeat')}</button>` : ''}
             </div>
           </div>`
        : activeCampBody;
      panel = `<aside class="floating-dialog compact-card ${dialogVisible ? '' : 'is-dialog-hidden'}" data-dialog="decision" ${dialogVisible ? '' : 'hidden'}>${dialogContent}</aside>
        ${campFab}`;
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
  let activeMotionTimer = null;
  const cancelMotion = () => {
    activeToken++;
    cancelBiomeCrossfade();
    if (activeRaf && typeof root.cancelAnimationFrame === 'function') {
      root.cancelAnimationFrame(activeRaf);
      activeRaf = null;
    }
    if (activeMotionTimer) {
      clearTimeout(activeMotionTimer);
      activeMotionTimer = null;
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
    const moveClimbersTogether = (mx, my) => {
      const mA = svg.querySelector('#climberMarkerA');
      const mB = svg.querySelector('#climberMarkerB');
      if (mA && mB) {
        mA.setAttribute('transform', `translate(${(mx - 4).toFixed(2)} ${my.toFixed(2)})`);
        mB.setAttribute('transform', `translate(${(mx + 4).toFixed(2)} ${my.toFixed(2)})`);
      } else {
        const mSingle = svg.querySelector('#climberMarker');
        if (mSingle) mSingle.setAttribute('transform', `translate(${mx.toFixed(2)} ${my.toFixed(2)})`);
      }
    };

    if (type === 'couple-split') {
      const fromStage = Math.max(0, Math.min(3, Number(intent.fromStage != null ? intent.fromStage : stage)));
      const toStage = Math.max(0, Math.min(3, Number(intent.toStage != null ? intent.toStage : Math.min(3, fromStage + 1))));
      const goodMember = intent.goodMember === 'B' ? 'B' : 'A';
      const badMember = goodMember === 'A' ? 'B' : 'A';
      const goodMarker = svg.querySelector(`#climberMarker${goodMember}`);
      const badMarker = svg.querySelector(`#climberMarker${badMember}`);
      const goodRope = svg.querySelector(`#partnerRope${goodMember}`);
      const risks = svg.querySelectorAll('.risk-path');
      const risk = svg.querySelector('.risk-path[data-active-risk="true"]') || risks[risks.length - 1];
      const group = risk && risk.closest ? risk.closest('.risk-group') : null;
      const activeNode = group ? group.querySelector('.risk-node') : null;
      const pts = risk ? String(risk.dataset.riskBreak || '684,319').split(',').map(Number) : biomes[toStage].point;
      const toPt = biomes[toStage].point;
      const fromPt = biomes[fromStage].point;
      const minX = Math.min(fromPt[0], toPt[0], pts[0]) - 110;
      const maxX = Math.max(fromPt[0], toPt[0], pts[0]) + 140;
      const minY = Math.min(fromPt[1], toPt[1], pts[1]) - 90;
      const maxY = Math.max(fromPt[1], toPt[1], pts[1]) + 110;
      const boxW = Math.max(760, Math.min(fullCamera[2], maxX - minX));
      const boxH = Math.min(fullCamera[3], Math.max(475, boxW * (750 / 1200)));
      const midX = (minX + maxX) / 2;
      const midY = (minY + maxY) / 2;
      const splitBox = [
        Math.max(0, Math.min(fullCamera[2] - boxW, midX - boxW / 2)),
        Math.max(0, Math.min(fullCamera[3] - boxH, midY - boxH / 2)),
        boxW,
        boxH
      ];

      const fromOff = biomes[fromStage].offset;
      const toOff = biomes[toStage].offset;
      const fromFrac = TRAIL_FRACS[fromStage] != null ? TRAIL_FRACS[fromStage] : 0;
      const toFrac = TRAIL_FRACS[toStage] != null ? TRAIL_FRACS[toStage] : 1;
      const len = risk && risk.getTotalLength ? risk.getTotalLength() : 260;

      if (!hasRaf()) {
        if (risk) { risk.style.strokeDashoffset = '0'; risk.style.strokeDasharray = 'none'; }
        if (activeNode) activeNode.style.opacity = '1';
        if (goodRope) { goodRope.setAttribute('opacity', '.78'); goodRope.setAttribute('stroke-dashoffset', String(toOff)); }
        if (goodMarker) goodMarker.setAttribute('transform', `translate(${toPt[0]} ${toPt[1]})`);
        if (badMarker) badMarker.setAttribute('transform', `translate(${pts[0]} ${pts[1]})`);
        setViewBox(svg, splitBox);
        if (done) done();
        return;
      }

      if (risk) { risk.style.strokeDasharray = '1000'; risk.style.strokeDashoffset = '1000'; }
      if (activeNode) activeNode.style.opacity = '0';
      if (goodRope) goodRope.setAttribute('opacity', '.78');

      // Act 1 (470ms): pull back to frame both safe ridge camp and red deviation
      animateSteps(470, tk, p => {
        const e = easeInOut(p);
        setViewBox(svg, from.map((n, i) => n + (splitBox[i] - n) * e));
      }, () => {
        // Act 2 (1800ms): SIMULTANEOUS safe climb (goodMember) + red deviation (badMember)
        animateSteps(1800, tk, p => {
          const eSafe = easeInOut(p);
          if (goodRope) goodRope.setAttribute('stroke-dashoffset', String(fromOff + (toOff - fromOff) * eSafe));
          if (goodMarker) {
            const [gx, gy] = trailPointAt(svg, fromFrac + (toFrac - fromFrac) * eSafe);
            goodMarker.setAttribute('transform', `translate(${gx.toFixed(2)} ${gy.toFixed(2)})`);
          }
          const progBad = p < 0.7 ? (p / 0.7) * 0.75 : 0.75 + Math.pow((p - 0.7) / 0.3, 1.8) * 0.25;
          if (risk) {
            risk.style.strokeDashoffset = String((1000 * (1 - progBad)).toFixed(2));
            if (badMarker && typeof risk.getPointAtLength === 'function') {
              const bpt = risk.getPointAtLength(len * progBad);
              badMarker.setAttribute('transform', `translate(${bpt.x.toFixed(2)} ${bpt.y.toFixed(2)})`);
            }
          }
        }, () => {
          if (risk) { risk.style.strokeDashoffset = '0'; risk.style.strokeDasharray = 'none'; }
          // Act 3 (360ms): reveal red node + 145ms breath before showing comparison card
          animateSteps(360, tk, p => {
            if (activeNode) activeNode.style.opacity = String(easeOut(p).toFixed(3));
          }, () => {
            if (activeNode) activeNode.style.opacity = '1';
            if (done) setTimeout(() => { if (tk === activeToken) done(); }, 145);
          });
        });
      });
      return;
    }

    if (type === 'risk') {
      const risks = svg.querySelectorAll('.risk-path');
      const risk = svg.querySelector('.risk-path[data-active-risk="true"]') || risks[risks.length - 1];
      if (!risk) { if (done) done(); return; }
      const group = risk.closest ? risk.closest('.risk-group') : null;
      const activeNode = group ? group.querySelector('.risk-node') : null;
      const pts = String(risk.dataset.riskBreak || '684,319').split(',').map(Number);
      const w = 696, h = 435;
      const crash = [Math.max(0, Math.min(fullCamera[2] - w, pts[0] - w * 0.55)), Math.max(0, Math.min(fullCamera[3] - h, pts[1] - h * 0.45)), w, h];
      const len = risk.getTotalLength ? risk.getTotalLength() : 260;

      if (!hasRaf()) {
        risk.style.strokeDashoffset = '0';
        risk.style.strokeDasharray = 'none';
        if (activeNode) activeNode.style.opacity = '1';
        if (typeof risk.getPointAtLength === 'function') {
          const endPt = risk.getPointAtLength(len);
          moveClimbersTogether(endPt.x, endPt.y);
        }
        setViewBox(svg, crash);
        if (done) done();
        return;
      }

      risk.style.strokeDasharray = '1000';
      risk.style.strokeDashoffset = '1000';
      if (activeNode) activeNode.style.opacity = '0';

      // Natural 3-phase pacing: steady ridge ascent (0..0.68), tension pause at break (0.68..0.78), gravity drop (0.78..1)
      const riskPacing = p => {
        if (p < 0.68) return (p / 0.68) * 0.74;
        if (p < 0.78) return 0.74 + ((p - 0.68) / 0.10) * 0.04;
        const dropT = (p - 0.78) / 0.22;
        return 0.78 + (dropT * dropT) * 0.22;
      };

      const act2Ms = Math.max(1770, Math.min(2130, Math.round(1590 + len * 1.0)));
      let curBox = from.slice();

      // Act 1 (470ms, easeInOut): smooth pullback to open mountain context
      animateSteps(470, tk, p => {
        const e = easeInOut(p);
        curBox = from.map((n, i) => n + (fullCamera[i] - n) * e);
        setViewBox(svg, curBox);
      }, () => {
        // Act 2 (1770-2130ms): organic ink draw (normalized pathLength=1000) + climber riding tip + smooth camera follow
        animateSteps(act2Ms, tk, p => {
          const prog = riskPacing(p);
          risk.style.strokeDashoffset = String((1000 * (1 - prog)).toFixed(2));
          if (typeof risk.getPointAtLength === 'function') {
            const pt = risk.getPointAtLength(len * prog);
            moveClimbersTogether(pt.x, pt.y);
            const zoomT = easeInOut(Math.min(1, p * 1.05));
            const targetW = fullCamera[2] + (w - fullCamera[2]) * zoomT;
            const targetH = fullCamera[3] + (h - fullCamera[3]) * zoomT;
            const targetX = Math.max(0, Math.min(fullCamera[2] - targetW, pt.x - targetW * 0.55));
            const targetY = Math.max(0, Math.min(fullCamera[3] - targetH, pt.y - targetH * 0.45));
            const desired = [targetX, targetY, targetW, targetH];
            curBox = curBox.map((n, i) => n + (desired[i] - n) * 0.09);
            setViewBox(svg, curBox);
          } else {
            const desired = fullCamera.map((n, i) => n + (crash[i] - n) * easeInOut(p));
            curBox = curBox.map((n, i) => n + (desired[i] - n) * 0.09);
            setViewBox(svg, curBox);
          }
        }, () => {
          // Lock stroke visible so Chromium never hides or clips the red path after animation
          risk.style.strokeDashoffset = '0';
          risk.style.strokeDasharray = 'none';
          // Act 3 (380ms): fade in red node + settle camera into exact riskCameraBox, then 145ms breath before dialog
          const settleFrom = curBox.slice();
          animateSteps(380, tk, p => {
            const e = easeOut(p);
            if (activeNode) activeNode.style.opacity = String(e.toFixed(3));
            setViewBox(svg, settleFrom.map((n, i) => n + (crash[i] - n) * e));
          }, () => {
            if (activeNode) activeNode.style.opacity = '1';
            setViewBox(svg, crash);
            if (done) {
              setTimeout(() => { if (tk === activeToken) done(); }, 145);
            }
          });
        });
      });
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
      const fromFrac = TRAIL_FRACS[fromStage] != null ? TRAIL_FRACS[fromStage] : (1 - fromOff / TRAIL_LENGTH);
      const toFrac = TRAIL_FRACS[toStage] != null ? TRAIL_FRACS[toStage] : (1 - toOff / TRAIL_LENGTH);
      const trailEl = svg.querySelector('#activeTrail');
      const ropeA = svg.querySelector('#partnerRopeA');
      const ropeB = svg.querySelector('#partnerRopeB');
      const onBiomeTrigger = intent && typeof intent.onBiomeTrigger === 'function' ? intent.onBiomeTrigger : null;
      let biomeTriggered = false;
      const fireBiome = () => {
        if (biomeTriggered || tk !== activeToken) return;
        biomeTriggered = true;
        if (onBiomeTrigger) onBiomeTrigger();
      };
      if (ropeA) ropeA.setAttribute('opacity', '.72');
      if (ropeB) ropeB.setAttribute('opacity', '.72');
      animateViewBox(svg, from, fullCamera.slice(), 400, () => {
        animateSteps(560, tk, p => {
          const e = easeInOut(p);
          const offVal = String(fromOff + (toOff - fromOff) * e);
          if (trailEl) trailEl.setAttribute('stroke-dashoffset', offVal);
          if (ropeA) ropeA.setAttribute('stroke-dashoffset', offVal);
          if (ropeB) ropeB.setAttribute('stroke-dashoffset', offVal);
          const [mx, my] = trailPointAt(svg, fromFrac + (toFrac - fromFrac) * e);
          moveClimbersTogether(mx, my);
          if (!biomeTriggered && p >= 0.6) fireBiome();
        }, () => {
          fireBiome();
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
    const zoomedElsewhere = from[2] < 1050 && (Math.abs(from[0] - target[0]) > 40 || Math.abs(from[1] - target[1]) > 40);
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

  function ensureStageRiskEntry(state) {
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
      return existingIdx;
    }
    state.history.push(entry);
    return state.history.length - 1;
  }

  function animateAdvanceStage(el, state, rerender, onSummit) {
    const syncViewportClass = () => {
      if (root.document && root.document.body) root.document.body.classList.add('is-mountain-viewport');
    };
    const svg = el && el.querySelector ? el.querySelector('.mountain-svg[data-camera]') : null;
    const fromStage = Number(state.stage) || 0;
    const isSummitStep = fromStage >= 3;
    const toStage = isSummitStep ? 3 : fromStage + 1;
    const nextBiome = biomes[toStage].id;
    state.hasEnteredCamp = true;
    state.inspectedRisk = null;
    state.roomWaiting = false;
    if (el && el.querySelector) hideDialogs(el, state);
    if (hasRaf() && svg) {
      let biomeApplied = false;
      const triggerBiome = () => {
        if (biomeApplied) return;
        biomeApplied = true;
        state.activeBiome = nextBiome;
        applyBiomeToDom(el, nextBiome);
      };
      runCamera(svg, { type: 'advance', fromStage, toStage, onBiomeTrigger: triggerBiome }, () => {
        triggerBiome();
        if (isSummitStep) {
          const tk = activeToken;
          activeMotionTimer = setTimeout(() => {
            activeMotionTimer = null;
            if (tk !== activeToken) return;
            state.initialViewBox = null;
            if (typeof onSummit === 'function') onSummit();
            syncViewportClass();
          }, 340);
        } else {
          state.stage = toStage;
          state.focusedNode = toStage;
          state.cameraMode = 'camp';
          state.dialogVisible = true;
          state.initialViewBox = campCamera(toStage);
          if (typeof rerender === 'function') rerender();
          state.initialViewBox = null;
          syncViewportClass();
        }
      });
    } else {
      state.activeBiome = nextBiome;
      if (isSummitStep) {
        if (typeof onSummit === 'function') onSummit();
      } else {
        state.stage = toStage;
        state.focusedNode = toStage;
        state.cameraMode = 'camp';
        state.dialogVisible = true;
        state.initialViewBox = campCamera(toStage);
        if (typeof rerender === 'function') rerender();
        state.initialViewBox = null;
      }
      syncViewportClass();
    }
  }

  function animateRiskStage(el, state, rerender, opts) {
    const syncViewportClass = () => {
      if (root.document && root.document.body) root.document.body.classList.add('is-mountain-viewport');
    };
    const keepPathCompare = !!(opts && opts.keepPathCompare);
    const split = (opts && opts.split) || null;
    const svg = el && el.querySelector ? el.querySelector('.mountain-svg[data-camera]') : null;
    const prevBox = svg ? parseViewBox(svg) : fullCamera.slice();
    const riskIdx = ensureStageRiskEntry(state);
    state.roomWaiting = false;
    if (keepPathCompare) {
      state.inspectedRisk = null;
      state.blocked = false;
      state.phase = 'expedition';
    } else {
      state.inspectedRisk = riskIdx;
      state.blocked = true;
      state.phase = 'blocked';
    }
    state.cameraMode = 'camp';
    state.dialogVisible = !hasRaf();
    state.initialViewBox = hasRaf() ? prevBox : riskCameraBox(riskRecord(state.caseId, langOf(state)), biomes[state.stage].point, state.stage);
    if (typeof rerender === 'function') rerender();
    syncViewportClass();
    if (hasRaf() && el && el.querySelector) {
      const nextSvg = el.querySelector('.mountain-svg[data-camera]');
      const intent = split
        ? { type: 'couple-split', fromStage: state.stage, toStage: Math.min(3, (Number(state.stage) || 0) + 1), goodMember: split.goodMember, badMember: split.badMember }
        : { type: 'risk', stage: state.stage };
      runCamera(nextSvg, intent, () => {
        state.initialViewBox = null;
        revealDialog(el, state);
      });
    } else {
      state.initialViewBox = null;
    }
  }

  function applyRoomSnapshot(state, roomData, el, rerender, onSummit) {
    if (!state || !roomData || state.coupleSyncMode === 'local') return false;
    const raw = dataFor(state.caseId) || {};
    if (!(raw.meta && raw.meta.isCouple)) return false;
    let changed = false;

    const ev = roomData.evaluation || {};
    if (ev.A) {
      state.votes = state.votes || {};
      state.votes.A = {
        fears: (ev.A.fears || ev.A.top_fears || []).slice(0, 3),
        thermometer: Number(ev.A.thermometer) || 3,
        priority: ev.A.priority || 'crecimiento',
        subjective: ev.A.subjective || ''
      };
    }
    if (ev.B) {
      state.votes = state.votes || {};
      state.votes.B = {
        fears: (ev.B.fears || ev.B.top_fears || []).slice(0, 3),
        thermometer: Number(ev.B.thermometer) || 3,
        priority: ev.B.priority || 'deuda-proteccion',
        subjective: ev.B.subjective || ''
      };
    }

    if (roomData.evaluation_ready && state.phase === 'fears' && state.roomWaiting === 'eval') {
      const allConcernIds = ((raw.persona && raw.persona.objectiveConcerns) || []).map(c => c.id);
      const aFears = (state.votes.A && state.votes.A.fears) || [];
      const bFears = (state.votes.B && state.votes.B.fears) || [];
      const merged = [...new Set([aFears[0], bFears[0], ...aFears, ...bFears].filter(Boolean))].slice(0, 3);
      state.fearOrder = merged.length ? merged : allConcernIds.slice(0, 3);
      state.roomWaiting = false;
      state.evaluationDone = true;
      ProfileEvalStore.save(state.caseId, state);
      state.phase = 'cross';
      changed = true;
    }

    const decs = roomData.decisions || {};
    state.roomDecisions = Object.assign({}, decs);
    const stKey = String(Number(state.stage) || 0);
    const curDec = decs[stKey];
    if (curDec && curDec.ready && state.phase === 'expedition') {
      state.animatedCoupleKeys = state.animatedCoupleKeys || {};
      const decKey = `${stKey}:${curDec.A && curDec.A.route}:${curDec.B && curDec.B.route}`;
      if (!state.animatedCoupleKeys[decKey]) {
        state.animatedCoupleKeys[decKey] = true;
        if (curDec.aligned && curDec.A && curDec.A.route === 'good') {
          state.roomAlignedBanner = true;
          animateAdvanceStage(el, state, rerender, onSummit);
          return true;
        }
        if (!curDec.aligned || (curDec.A && curDec.A.route === 'bad') || (curDec.B && curDec.B.route === 'bad')) {
          const split = !curDec.aligned
            ? { goodMember: curDec.A.route === 'good' ? 'A' : 'B', badMember: curDec.A.route === 'bad' ? 'A' : 'B' }
            : null;
          animateRiskStage(el, state, rerender, { keepPathCompare: true, split });
          return true;
        }
      }
    }

    if (changed && typeof rerender === 'function') rerender();
    return changed;
  }

  function handleMountainAction(action, trigger, el, state, rerender, onSummit) {
    const syncViewportClass = () => {
      if (root.document && root.document.body) {
        root.document.body.classList.add('is-mountain-viewport');
      }
    };

    if (action === 'copy-room-link') {
      const url = buildPartnerUrl(state);
      try {
        if (root.navigator && root.navigator.clipboard && root.navigator.clipboard.writeText) {
          root.navigator.clipboard.writeText(url);
        }
      } catch (_) {}
      state.roomCopied = true;
      rerender();
      if (typeof setTimeout === 'function') {
        setTimeout(() => { state.roomCopied = false; try { rerender(); } catch (_) {} }, 1800);
      }
      return true;
    }

    if (action === 'open-partner-tab') {
      const url = buildPartnerUrl(state);
      CoupleRoomSync.createRoom(state.caseId, state.roomId);
      try { if (typeof root.open === 'function') root.open(url, '_blank'); } catch (_) {}
      return true;
    }

    if (action === 'toggle-sync-mode') {
      state.coupleSyncMode = state.coupleSyncMode === 'local' ? 'remote' : 'local';
      state.roomWaiting = false;
      state.voteTurn = state.coupleSyncMode === 'local' ? 'A' : (state.memberRole || 'A');
      rerender();
      return true;
    }

    if (action === 'toggle-concern') {
      const id = trigger.dataset.concernId;
      if (!id) return true;
      const raw = dataFor(state.caseId) || {};
      const isCouple = !!(raw.meta && raw.meta.isCouple);
      if (isCouple && state.phase === 'fears') {
        const turn = state.coupleSyncMode !== 'local' ? (state.memberRole === 'B' ? 'B' : 'A') : (state.voteTurn === 'B' ? 'B' : 'A');
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
        const turn = state.coupleSyncMode !== 'local' ? (state.memberRole === 'B' ? 'B' : 'A') : (state.voteTurn === 'B' ? 'B' : 'A');
        state.votes = state.votes || {};
        const cur = state.votes[turn] || { fears: [], thermometer: 3, priority: turn === 'A' ? 'crecimiento' : 'deuda-proteccion' };
        cur.thermometer = lvl;
        state.votes[turn] = cur;
      }
      state.thermometer = lvl;
      rerender();
      return true;
    }

    if (action === 'toggle-more-concerns') {
      state.showAllConcerns = !state.showAllConcerns;
      rerender();
      return true;
    }

    if (action === 'edit-fears') {
      state.phase = 'fears';
      state.roomWaiting = false;
      state.voteTurn = state.coupleSyncMode === 'local' ? 'A' : (state.memberRole || 'A');
      rerender();
      return true;
    }

    if (action === 'next-fears' || action === 'submit-vote') {
      const raw = dataFor(state.caseId) || {};
      const isCouple = !!(raw.meta && raw.meta.isCouple);
      const isRemoteCouple = isCouple && state.coupleSyncMode !== 'local';
      const allConcernIds = ((raw.persona && raw.persona.objectiveConcerns) || []).map(c => c.id);
      const checkedInDom = [...el.querySelectorAll('[data-fear]:checked,[data-vote-fear]:checked')].map(x => x.dataset.fear || x.dataset.voteFear).filter(Boolean);
      const subVal = ((el.querySelector('[data-subjective]') || {}).value || '').trim();
      const prioVal = (el.querySelector('[data-priority]:checked') || {}).value || 'deuda-proteccion';
      state.voters = getSpec(state.caseId, langOf(state), raw).people;

      if (isCouple) {
        const turn = isRemoteCouple ? (state.memberRole === 'B' ? 'B' : 'A') : (state.voteTurn === 'B' ? 'B' : 'A');
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
        if (isRemoteCouple) {
          const roomSnap = CoupleRoomSync.submitEvaluation(state.roomId, state.caseId, turn, state.votes[turn]);
          if (roomSnap.evaluation_ready) {
            state.roomWaiting = 'eval';
            applyRoomSnapshot(state, roomSnap, el, rerender, onSummit);
            SherpasAI.request('pact', { case_id: state.caseId, member_a_votes: state.votes.A, member_b_votes: state.votes.B }, { mode: 'deterministic' });
          } else {
            state.roomWaiting = 'eval';
            rerender();
          }
          return true;
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

    if (action === 'room-agree-good') {
      state.roomAlignedBanner = false;
      animateAdvanceStage(el, state, rerender, onSummit);
      return true;
    }

    if (action === 'redo-eval') {
      cancelMotion();
      ProfileEvalStore.clear(state.caseId);
      state.openOverlay = null;
      state.evaluationDone = false;
      state.phase = 'fears';
      state.view = viewName('expedition', langOf(state), state.irlDay);
      state.fearOrder = [];
      state.votes = {};
      state.voteTurn = state.coupleSyncMode === 'local' ? 'A' : (state.memberRole || 'A');
      state.roomWaiting = false;
      state.roomAlignedBanner = false;
      state.stage = 0;
      state.focusedNode = 0;
      state.hasEnteredCamp = false;
      state.activeBiome = null;
      state.inspectedRisk = null;
      state.cameraMode = 'panoramic';
      state.dialogVisible = false;
      state.initialViewBox = fullCamera.slice();
      state.summit = false;
      state.blocked = false;
      state.history = [];
      rerender();
      state.initialViewBox = null;
      syncViewportClass();
      return true;
    }

    if (action === 'start-expedition') {
      const targetStage = Math.max(0, Math.min(3, Number(state.stage) || 0));
      state.evaluationDone = true;
      ProfileEvalStore.save(state.caseId, state);
      state.phase = 'expedition';
      state.hasEnteredCamp = false;
      state.activeBiome = null;
      state.roomWaiting = false;
      state.roomAlignedBanner = false;
      state.view = viewName('expedition', langOf(state), state.irlDay);
      state.cameraMode = 'panoramic';
      state.focusedNode = targetStage;
      state.inspectedRisk = null;
      state.dialogVisible = false;
      state.initialViewBox = fullCamera.slice();
      SherpasAI.request('reframe', strictCasePayload(state.caseId, langOf(state), state.stage, state), { mode: 'deterministic' });
      rerender();
      state.initialViewBox = null;
      syncViewportClass();
      return true;
    }

    if (action === 'advance') {
      const route = (el.querySelector('[name="route"]:checked') || {}).value || 'good';
      const raw = dataFor(state.caseId) || {};
      const isRemoteCouple = !!(raw.meta && raw.meta.isCouple) && state.coupleSyncMode !== 'local';
      SherpasAI.request('reframe', strictCasePayload(state.caseId, langOf(state), state.stage, state), { mode: 'deterministic' });

      if (isRemoteCouple) {
        const loc = localizeData(raw, langOf(state));
        const opt = stepGoodOption(state, loc, getSpec(state.caseId, langOf(state), raw), state.stage);
        const chosenLabel = route === 'bad' ? (opt.badLabel || t(state, 'ignore')) : opt.title;
        const role = state.memberRole === 'B' ? 'B' : 'A';
        const stKey = String(Number(state.stage) || 0);
        const roomSnap = CoupleRoomSync.submitDecision(state.roomId, state.caseId, role, state.stage, route, chosenLabel);
        state.roomDecisions = Object.assign({}, roomSnap.decisions || {});
        const stDec = state.roomDecisions[stKey];
        if (stDec && stDec.ready) {
          state.animatedCoupleKeys = state.animatedCoupleKeys || {};
          const decKey = `${stKey}:${stDec.A && stDec.A.route}:${stDec.B && stDec.B.route}`;
          if (!state.animatedCoupleKeys[decKey]) {
            state.animatedCoupleKeys[decKey] = true;
            if (stDec.aligned && stDec.A.route === 'good') {
              state.roomAlignedBanner = true;
              animateAdvanceStage(el, state, rerender, onSummit);
            } else {
              const split = !stDec.aligned
                ? { goodMember: stDec.A.route === 'good' ? 'A' : 'B', badMember: stDec.A.route === 'bad' ? 'A' : 'B' }
                : null;
              animateRiskStage(el, state, rerender, { keepPathCompare: true, split });
            }
          }
          return true;
        }
        state.roomWaiting = 'decision';
        rerender();
        syncViewportClass();
        return true;
      }

      if (route === 'bad') {
        animateRiskStage(el, state, rerender, { keepPathCompare: false });
        return true;
      }

      animateAdvanceStage(el, state, rerender, onSummit);
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
      const prevBiome = resolveActiveBiome(state);
      const svg = el.querySelector('.mountain-svg[data-camera]');
      const prevBox = svg ? parseViewBox(svg) : fullCamera.slice();
      state.view = viewName('expedition', langOf(state), state.irlDay);
      state.inspectedRisk = null;
      state.focusedNode = targetStage;
      state.cameraMode = 'camp';
      if (!state.hasEnteredCamp && state.activeBiome == null && state.phase !== 'fears' && state.phase !== 'cross') {
        state.hasEnteredCamp = true;
        state.activeBiome = biomes[Math.max(0, Math.min(3, Number(state.stage) || 0))].id;
      }
      const nextBiome = resolveActiveBiome(state);
      state.dialogVisible = !hasRaf();
      state.initialViewBox = hasRaf() ? prevBox : campCamera(targetStage);
      if (hasRaf() && prevBiome !== nextBiome) state._biomeTransitionFrom = prevBiome;
      rerender();
      delete state._biomeTransitionFrom;
      syncViewportClass();
      if (hasRaf()) {
        if (prevBiome !== nextBiome) scheduleBiomeCrossfade(el, nextBiome);
        const nextSvg = el.querySelector('.mountain-svg[data-camera]');
        runCamera(nextSvg, { type: 'focus', stage: targetStage }, () => { state.initialViewBox = null; revealDialog(el, state); });
      }
      return true;
    }

    if (action === 'toggle-pack') {
      state.openOverlay = state.openOverlay === 'pack' ? null : 'pack';
      rerender();
      return true;
    }

    if (action === 'toggle-health') {
      state.openOverlay = state.openOverlay === 'health' ? null : 'health';
      rerender();
      return true;
    }

    if (action === 'close-overlay') {
      if (state.openOverlay) {
        state.openOverlay = null;
        rerender();
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

  function bindOverlayDismiss(el, getState, rerender) {
    if (!root.document) return () => {};
    const onKeyDown = ev => {
      if (ev.key !== 'Escape') return;
      const st = getState();
      if (st && st.openOverlay) {
        st.openOverlay = null;
        rerender();
      }
    };
    const onPointerDown = ev => {
      const st = getState();
      if (!st || !st.openOverlay) return;
      const target = ev.target;
      if (!target || typeof target.closest !== 'function') return;
      if (st.openOverlay === 'pack') {
        if (target.closest('.pack-anchor') || target.closest('.redo-survey-btn') || target.closest('.health-pill-btn') || target.closest('.language-toggle') || target.closest('.case-select')) return;
        st.openOverlay = null;
        rerender();
      } else if (st.openOverlay === 'health') {
        if (target.closest('.health-modal-card') || target.closest('.health-pill-btn') || target.closest('.pack-btn') || target.closest('.redo-survey-btn') || target.closest('.language-toggle')) return;
        st.openOverlay = null;
        rerender();
      }
    };
    root.document.addEventListener('keydown', onKeyDown);
    root.document.addEventListener('mousedown', onPointerDown);
    return () => {
      root.document.removeEventListener('keydown', onKeyDown);
      root.document.removeEventListener('mousedown', onPointerDown);
    };
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
    let unsubRoom = null;
    const attachRoom = () => {
      if (unsubRoom) { try { unsubRoom(); } catch (_) {} unsubRoom = null; }
      const raw = dataFor(state.caseId) || {};
      if (raw.meta && raw.meta.isCouple && state.roomId) {
        CoupleRoomSync.createRoom(state.caseId, state.roomId);
        unsubRoom = CoupleRoomSync.subscribe(state.roomId, state.caseId, roomData => {
          applyRoomSnapshot(state, roomData, el, update, onSummit);
        });
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
      state.hasEnteredCamp = true;
      state.activeBiome = 'summit';
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
        attachRoom();
        update();
      });
      el.querySelectorAll('[data-action]').forEach(n => n.onclick = (ev) => {
        if (n.tagName === 'A' && ev && ev.preventDefault) ev.preventDefault();
        const a = n.dataset.action;
        if (handleMountainAction(a, n, el, state, () => { el.innerHTML = render(state); syncViewportClass(); bind(); }, onSummit)) return;
        if (a === 'nav') {
          state.openOverlay = null;
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
            if (state.summit || vk === 'overview' || !state.hasEnteredCamp) {
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
        else if (a === 'repeat') { ProfileEvalStore.clear(state.caseId); const next = createInitialState(state.caseId); next.lang = state.lang; state = next; }
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

    if (isMountainPhase(state) && state.hasEnteredCamp && hasRaf()) {
      state.dialogVisible = false;
      state.initialViewBox = fullCamera.slice();
    }
    const unbindOverlay = bindOverlayDismiss(el, () => state, update);
    attachRoom();
    update();
    if (isMountainPhase(state) && state.hasEnteredCamp && hasRaf()) {
      const svg = el.querySelector('.mountain-svg[data-camera]');
      runCamera(svg, { type: 'enter', stage: state.focusedNode || 0 }, () => { state.initialViewBox = null; revealDialog(el, state); });
    }

    return {
      state,
      getState: () => state,
      render: () => render(state),
      setState(next) { state = next; attachRoom(); update(); return state; },
      dispatch(a, v) {
        if (a === 'mode') state.mode = v;
        else if (a === 'nav') { state.openOverlay = null; state.view = v; }
        else if (a === 'lang') { state.lang = v === 'EN' ? 'EN' : 'ES'; persistLanguage(state.lang); state.view = viewName(viewKey(state.view), state.lang, state.irlDay); }
        else if (a === 'summit') { state.summit = true; state.phase = 'summit'; state.hasEnteredCamp = true; state.activeBiome = 'summit'; state.view = viewName('current', langOf(state), state.irlDay); }
        update();
        return state;
      },
      unmount() { if (unsubRoom) { try { unsubRoom(); } catch (_) {} unsubRoom = null; } unbindOverlay(); cancelMotion(); el.innerHTML = ''; if (root.document && root.document.body) root.document.body.classList.remove('is-mountain-viewport'); }
    };
  }

  return {
    listCases,
    getScenario: id => { const data = dataFor(id); return data ? { id, data, spec: specs[id] } : null; },
    createInitialState,
    render,
    renderHeader,
    telegramRadioUrl,
    renderPackPopover,
    renderHealthModal,
    bindOverlayDismiss,
    mount,
    biomes,
    BIOME_ASSETS,
    resolveActiveBiome,
    applyBiomeToDom,
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
    CoupleRoomSync,
    ProfileEvalStore,
    applyRoomSnapshot,
    buildPartnerUrl,
    failTags,
    persistLanguage,
    SherpasAI,
    runCamera,
    cancelMotion,
    campCamera,
    fullCamera,
    isMountainPhase,
    handleMountainAction,
    preview,
    riskRecord,
    strictCasePayload
  };
});
