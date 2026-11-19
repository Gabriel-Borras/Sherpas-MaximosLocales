# Propuesta de Proyecto: *Sherpa Basecamp*

> **Documento histórico del proceso del hackathon (18–19 nov).** Refleja un estado intermedio y puede no coincidir con la versión final. Para el estado actual: [`README.md`](../../README.md) y [`docs/CAPACIDADES_BACKEND.md`](../CAPACIDADES_BACKEND.md).

**De un PDF muerto de 22 páginas a una expedición financiera centrada en las personas y sus emociones**

---

## 1. El contexto y las "pistas ocultas" que encontramos en los datos

Sherpas Wealth ya tiene resuelta la parte analítica y matemática (recoger datos y calcular el plan financiero). El reto del hackathon consiste al 100% en **cómo la familia entiende su plan, supera el bloqueo inicial y pasa a la acción**, teniendo en cuenta dos reglas clave del `README.md` oficial:
- No debemos recalcular las finanzas ni inventar números nuevos: hay que usar los datos reales de los casos (`cases/`).
- Hacer únicamente un dashboard tradicional o un chat de IA sobre el plan puntúa bajo en creatividad (Sherpas ya dispone de tours guiados y chat).

Al analizar en profundidad los `report.pdf`, los JSON (`financial-health.json`, `investment-analysis.json`) y los perfiles `persona.md`, encontramos **4 pistas ocultas** que la mayoría de equipos está pasando por alto:

1. **El fallo emocional del formato actual (`report.pdf`):** El informe actual es un PDF corporativo de 22 páginas basado en una proyección determinista limpia (una línea suave sin turbulencias). Como consecuencia, quien tiene una puntuación alta (como Samantha, score 82) no percibe que a los 73 años se queda a \$0, y quien tiene una puntuación baja (como Michael, score 26) se asusta y deja de mirar. Irónicamente, la empresa se llama **Sherpas** y la portada del PDF ya incluye curvas topográficas de montaña.
2. **El oro sin explotar de `persona.md`:** Contiene inteligencia psicológica que un dashboard normal ignora: parejas con estilos de decisión divididos (`D5: DUAL`, donde uno ahorra y el otro arrastra deuda), riesgo real desalineado con el riesgo que creen asumir (`MISALIGNED`), y un campo explícitamente vacío llamado **`Subjective concerns`** (*"None recorded"*): el plan calcula números, pero nadie ha preguntado a la familia qué miedo concreto le quita el sueño.
3. **Impactos y tormentas reales ya calculadas en los JSON:** No hace falta inventar modelos matemáticos ni porcentajes arbitrarios:
   - `projections.yearly` ya da la curva año a año hasta los 91 años (`net_worth`, `net_worth_needed`, `total_debts`, `investable_assets`).
   - `score.top_moves` ya calcula cuánto sube exactamente el score con cada acción concreta (ej. subir seguro de vida, contratar *umbrella* o redirigir el flujo de caja libre).
   - `analysis.events` y `periods` ya documentan cómo reaccionó y se recuperó exactamente la cartera de esa familia ante caídas reales recientes (ej. el shock arancelario de abril de 2025, la corrección de agosto de 2024 o el shock de DeepSeek).
4. **Nadie mira un plan a 30 años todos los días:** A diferencia de una app bancaria diaria, un plan financiero se consulta de forma puntual. El verdadero reto es impactar y alinear en el **Día 1**, y saber reaparecer **fuera de la app** en los momentos críticos (Día 3, Día 30, una caída brusca de la bolsa o un hito vital como la matrícula universitaria de agosto).

---

## 2. Nuestra propuesta: *Sherpa Basecamp* (3 pilares conectados)

### Pilar 1 — La Montaña de Decisiones (Expedición de 3 minutos)
Convertimos el PDF de 22 páginas en una **expedición topográfica** construida sobre la silueta real de `projections.yearly` (desde la edad actual hasta los 91 años), dividida en **3–4 campamentos base** que representan los hitos y tensiones reales de esa familia (deuda cara, fondo de emergencia, universidad, jubilación).

- En cada campamento, el usuario toma decisiones ágiles estilo juego narrativo (*BitLife* directo y rápido) repartiendo su flujo de caja libre real: **antes de confirmar cada elección, ve visualmente hacia dónde apuntan las líneas de su ruta (arriba, plano o caída)** apoyándose en los `score.top_moves` y métricas reales de Sherpas.
- **Accesible para todos:** Incluye un selector **"Modo Simple / Modo Experto"** para que quien no sabe nada de finanzas lo entienda de forma visual y humana, y quien quiera rigor técnico pueda desplegar las cifras exactas del plan.

### Pilar 2 — Cordada Asimétrica (Minijuego de conciliación para parejas)
En los casos de pareja (`D5: DUAL`, con perfiles de riesgo distintos como *Growth* frente a *Moderate*), la app rompe el enfoque de "pantalla única para todo el hogar" y propone una **entrada asimétrica de 60 segundos por persona**:

- Cada miembro responde por separado (sin ver lo que vota su pareja) cuál es su mayor preocupación real —capturando por fin los **`Subjective concerns`**— y ordena sus 3 prioridades en la montaña.
- Al cruzar ambas respuestas en la pantalla de conciliación, la app destaca primero **"En qué coincidís al 100%"** (su ancla motivacional común, como proteger a sus hijos) y aísla **únicamente los 1–2 puntos de fricción**, proponiendo un **punto medio realista** ajustado a su flujo de caja. Sin culpas ni reproches.

### Pilar 3 — La Radio del Sherpa (El giro *outside the box*: el plan sale fuera de la app)
En lugar de obligar al usuario a volver cada semana a rejugar o mirar gráficas estáticas, una vez terminada la expedición la app queda en segundo plano y **sale al encuentro del usuario solo cuando la realidad aprieta**:

- **Notificaciones de calma y refuerzo estratégico ante caídas de mercado:** Cuando ocurre un evento fuera de su control (ej. caída fuerte de la bolsa), recibe un micro-mensaje anti-pánico respaldado por sus propios datos históricos (`analysis.events`), recordándole que su estrategia y sus *assets* ya superaron turbulencias similares y que su plan a largo plazo sigue intacto.
- **Disparadores de momentos reales:** Avisos puntuales para el Día 3, el Día 30 o fechas clave del caso (como la factura de la universidad en agosto o el hito de liquidar una tarjeta), exportables a calendario (`.ics`) y demostrables en vivo durante la presentación.

---

## 3. Alineación directa con la rúbrica (100 puntos)

- **Captivating (20 pts):** Narrativa visual de montaña topográfica y decisiones en vivo desde el segundo 1, frente a un PDF o gráficas convencionales.
- **Understanding (20 pts):** Explicación intuitiva para novatos + toggle técnico con métricas reales para expertos.
- **Motivation to act (20 pts):** Deja definido un primer paso inmediato tras la expedición y cubre los días posteriores (Día 3 / Día 30) con disparadores fuera de la app.
- **Personal (15 pts):** Personalizado por familia **y por cada individuo dentro de la pareja**, recogiendo sus miedos subjetivos reales.
- **Creativity (15 pts):** Explota `persona.md` (`D4`, `D5`, `Subjective concerns`), `top_moves` y `analysis.events` sin inventar cálculos, resolviendo el seguimiento fuera de la app.
- **Friday plan (10 pts):** Alcance claro y foco explícito en evitar otro dashboard o chatbot genérico.

---

## Apéndice: Por qué el núcleo del proyecto es **resolver el miedo y gestionar las emociones**

Los números por sí solos casi nunca hacen que una familia actúe; lo que paraliza o provoca malas decisiones financieras es **el miedo**. Un informe de 22 páginas responde a la lógica matemática, pero fracasa porque ignora la psicología humana. *Sherpa Basecamp* está diseñado específicamente para **identificar, contener y transformar esas emociones**:

1. **Transformar la parálisis en agencia humana (*Efecto IKEA*):**
   Ver un score crítico de 26 o un déficit millonario en un PDF genera bloqueo y rechazo (*"esto no tiene arreglo, mejor no miro"*). Cuando la persona participa activamente en la montaña eligiendo sus propios pasos y viendo cómo cambia la dirección de la línea con cada decisión, **siente control sobre su futuro**. Psicológicamente, valoramos, entendemos y ejecutamos muchísimo más un plan que hemos ayudado a construir que una lista de órdenes impuestas en un documento.
2. **Desactivar la tensión emocional en pareja cuando piensan diferente:**
   En muchos hogares no se habla de dinero por miedo a discutir o señalarse culpables (*uno gasta/tiene la tarjeta, el otro ahorra; uno quiere asumir más riesgo, el otro busca seguridad*). La **entrada asimétrica** protege el espacio emocional de cada miembro: les permite expresar qué les da miedo sin sentirse juzgados en el momento, descubre primero lo que sí comparten (proteger a su familia) y convierte un conflicto emocional en una negociación objetiva sobre un punto medio.
3. **Controlar el pánico ante sucesos fuera de nuestro control:**
   El mayor enemigo de una buena estrategia financiera no es la falta de rentabilidad, sino **la duda y el impulso emocional cuando ocurren eventos externos que no controlamos** (una caída brusca de la bolsa, titulares alarmistas, volatilidad geopolítica). En esos días, el cliente se pregunta si debería venderlo todo y salirse del plan.
   * La **Radio del Sherpa** actúa justo en ese instante vulnerable como un ancla emocional basada en hechos reales de su propia cartera: les recuerda con datos reales de `investment-analysis.json` que **el año pasado / en las caídas recientes (como los aranceles de abril de 2025 o las correcciones de mercado) ya pasaron por tormentas parecidas y, manteniendo sus *assets* y su estrategia, lo aguantaron como campeones y se recuperaron**. Reforzar la confianza en su estrategia actual cuando más tiembla el mercado evita errores irreversibles y mantiene viva la relación con el plan.
