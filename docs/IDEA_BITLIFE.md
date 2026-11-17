# Propuesta: Sherpas Living Timeline (mecánica tipo BitLife)

> **Estado:** Borrador conceptual validado · **Rama:** `bitlife`  
> **Objetivo:** Resolver el **Paso 3 del asesor** (*Bring the plan to life*) pasando de un PDF/web estática a una experiencia que enganche en <10s, se entienda sin saber finanzas, alinee a parejas y mueva a actuar desde el Día 0 hasta el Día 30.

---

## 1. La idea en palabras simples

En lugar de enviar un informe largo o un chat genérico, convertimos el plan calculado por Sherpas en una **simulación interactiva de tu vida futura (mecánica tipo BitLife con estética editorial adulta, limpia y fiable)**.

Abres el enlace desde el móvil, indicas qué te preocupa hoy, avanzas por los hitos clave de tu vida tomando decisiones basadas en tus datos reales para ver cómo cambia tu futuro y sales con **un único primer paso real** que la aplicación continúa contigo en el **Día 3**, el **Día 30** y tus fechas críticas reales.

---

## 2. Flujo principal (4 piezas conectadas)

1. **Pulse Check inicial (5s):**  
   * No abre con una nota fría (`26/100 Critical` o `82/100 Strong`).  
   * Pregunta quién está mirando (ej. *Timothy / Melanie / Ambos*) y su inquietud principal (*"What keeps you up at night?"*) para arrancar por lo que les importa.
2. **Simulador de hitos + Dual-Lens (`Plain ↔ Math`) + Co-op de pareja:**  
   * Avanzas por los años clave reales de `financial-health.json` y `persona.md`.  
   * **Toggle `Plain ↔ Math`:** traduce cada cifra a impacto cotidiano en *Plain* o muestra los datos exactos del asesor en *Math*.  
   * **Parejas:** cada miembro vota según su tolerancia al riesgo (`D4`); si chocan, la IA propone el punto medio basado en sus datos reales.
3. **Fast-Forward al punto de tensión (con diagnóstico real, sin *Game Over* irreal):**  
   * Salta años vacíos hasta el punto donde el plan actual falla o pierde eficiencia, muestra la causa raíz y da botón directo para volver a la decisión de origen o corregir sobre la marcha.
4. **Tu vida real como partida guardada (`Día 0 → Día 3 → Día 30`):**  
   * Al cerrar la simulación, bloquea **una sola micro-acción de 3 minutos** (*Step 1*) con pasos concretos para ejecutarla hoy.  
   * La partida queda en pausa esperando tu acción real:  
     * **Día 3:** check-in para confirmar si la completaste o resolver en 30s la duda que te frenó.  
     * **Día 30 / Fechas reales:** siguiente evento del plan (ej. factura de universidad en agosto).

---

## 3. Respuesta a los 11 problemas detectados por Sherpas

| # | Problema actual (según `README.md` de Sherpas) | Cómo lo resuelve esta propuesta |
| :-: | :--- | :--- |
| **1** | No ven cómo una decisión hoy cambia su futuro (Michael: casa 2027 vs. jubilarse a los 58). | Simulador año a año por hitos reales con botón **Rewind** para comparar futuros al instante. |
| **2** | Cifras grandes y porcentajes sin sentido (`"$2.37M left"`). | Toggle **Plain ↔ Math**: traduce cifras a impacto real (*"$3,240/año en intereses"*) y deja el cálculo exacto a un clic. |
| **3** | Un buen *score* oculta un problema grave (Samantha: 82, pero sin ahorros a los 73). | La primera pantalla ignora el "82" tranquilizador y abre con la alerta real de los 73 años llevándote a ese hito. |
| **4** | El plan responde a lo calculable, no al miedo que les quita el sueño. | El *Pulse Check* inicial pregunta qué les preocupa y ordena la experiencia alrededor de ese miedo. |
| **5** | No leen planes largos; lo miran en ráfagas cortas desde el móvil (Weah). | Formato *mobile-first* por tarjetas breves de 10 segundos en vez de un PDF de decenas de páginas. |
| **6** | Malas noticias hacen mirar hacia otro lado (Michael: 26 "critical"). | Evita el castigo visual del "26 rojo"; abre con la meta deseada y convierte el problema en una decisión accionable. |
| **7** | Temas como muerte y seguros se evitan (Daniel: \$250k vs. \$1.6M). | Integra la protección como un evento concreto dentro de la línea temporal (*qué queda cubierto para tus hijos si algo pasa*). |
| **8** | Parejas: un plan, dos personas con distinto riesgo (Timothy vs. Melanie). | Selector **Partner A / Partner B / Both** + doble voto en hitos con mediación IA para desbloquear acuerdos. |
| **9** | Las dudas llegan en Día 3 / Día 30 y a la semana se olvida casi todo. | La partida sigue viva fuera de la web: en Día 3 pregunta qué te frenó y te deja simular tu duda en 10s. |
| **10** | El plan llega fuera de las fechas reales de acción (agosto universidad, casa 2030). | Los eventos futuros del timeline se anclan a las fechas reales del caso (ej. alerta previa a agosto en Samantha). |
| **11** | Demasiadas opciones sin "Paso 1", sin guía ni confirmación. | Entrega una única micro-acción de 3 minutos con pasos concretos; al marcarla hecha, actualiza el estado real del plan. |

---

## 4. Realidad técnica verificada en los JSON de Sherpas (`cases/`)

Para cumplir la regla estricta del hackathon (**no inventar números**), hemos inspeccionado los `financial-health.json` reales de los 4 casos:

| Caso | Score actual | ¿Llega a \$0 en `projections.yearly`? | Palancas reales en `top_moves` / `combined_moves` |
| :--- | :---: | :--- | :--- |
| **Michael Carter** | `26` | **Sí** (`investable_assets` negativos en **2075**, edad 86) | Umbrella (`26→31`), bajar tasa de retiro (`26→62`), subir asignación growth (`26→31`). |
| **Samantha Lewis** | `82` | **Sí** (`investable_assets` negativos en **2053**, edad 74; `net_worth` negativo en 2070) | Cerrar brecha cobertura (`82→84`), reducir concentración (`82→83`), ajustar growth (`82→83`). |
| **Timothy & Melanie Weah** | `60` | **No** (terminan 2079 con \$16.1M net worth) | Pagar tarjeta (`60→62`), añadir seguro vida y umbrella; **combinados suben a `78`**. |
| **Daniel & Emily Johnson** | `52` | **No** (terminan 2075 con \$4.3M net worth) | Subir cobertura mortalidad (`52→57`), añadir umbrella (`52→56`), subir ahorro (`52→55`); **combinados suben a `60`**. |

### Implicación directa para la implementación
* **Una sola curva anual base:** `projections.yearly` solo trae la proyección del plan actual (no incluye curvas precalculadas para ramas inventadas).
* **Cómo evitar el *"Bad Ending" falso*:** En **Michael** y **Samantha** sí existe el año exacto en que se agota el dinero; en **Weah** y **Johnson**, el punto de tensión debe reflejar la pérdida real por intereses (18%–24.9%), brecha de protección o estancamiento en el score (`60` / `52`), usando el salto real que sí calcula `combined_moves` (`60→78` / `52→60`).
* **Rol del LLM (`TEAM_KEY` proxy):** Traducir, narrar y adaptar el tono a cada miembro/miedo usando **únicamente** las cifras del JSON/MCP.

---

## 5. Prototipo inicial incluido

* [`demo-bitlife/index.html`](../demo-bitlife/index.html): micro-demo estática centrada en **Michael Carter** para validar la mecánica de `+ Age Up`, el toggle `Plain / Math`, el `Rewind` y la transición a `Step 1`.
