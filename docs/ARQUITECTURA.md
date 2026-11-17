# Arquitectura: conversación entre agentes y coordinación multi-máquina

Sistema adaptado de [BauDahn/claude-central](https://github.com/BauDahn/claude-central) para organizar agentes en paralelo dentro de una máquina y coordinar varias máquinas entre sí a través de GitHub.

## 1. Organización local de agentes

- **`central`** (`central/CLAUDE.md`): único punto de contacto con el usuario. Supervisa sesiones, delega trabajo y resume resultados.
- **`orquestador`** (`agentes/roles/orquestador.md`): descompone tareas grandes en subtareas, crea tickets en el tablero (`tareas`) y asigna trabajo sin pisar archivos.
- **Especialistas** (`agentes/roles/*.md`): `backend`, `frontend`, `revisor`, `seguridad`, `ideas`, `optimizador`.
- **Reglas comunes** (`agentes/roles/_comun.md`): protocolo de mensajes y ahorro de tokens mediante `agentes/contexto/INDEX.md`.

### Protocolo de mensajes entre sesiones

| Mensaje | De → a | Significado |
|---|---|---|
| `ASIGNA: <agente> <tarea> \| contexto: <rutas>` | orquestador → agente | Encargo de tarea y rutas de contexto. |
| `NECESITA: <agente> <qué>` | agente → orquestador | Falta contexto o dependencia de otro agente. |
| `LISTO: <resumen> \| archivos: <rutas>` | agente → orquestador | Subtarea terminada y archivos tocados. |
| `PEDIR-CONTEXTO: <qué> \| fuente: <ruta/url> \| para: <agente>` | agente → optimizador | Solicitud de resumen/mapa compacto. |
| `CONTEXTO-LISTO: <ruta> (~N tokens) — <resumen>` | optimizador → agente | Contexto compacto disponible en disco. |

## 2. Tablero atómico de tareas (`agentes/bin/tareas`)

Almacena el estado en `$AGENTES_HOME/tareas/<proyecto>.json` (por defecto `~/agentes/tareas/`) con bloqueo exclusivo multiplataforma (`msvcrt` en Windows, `fcntl` en POSIX):

- `pendiente` → `en_curso` → `hecha` (o `bloqueada`).
- `tomar` es atómico: evita que dos agentes tomen la misma tarea o ignoren dependencias (`--dep`).

## 3. Coordinación multi-máquina (`agentes/bin/equipo`)

Varias máquinas (cada una con su `central`) se coordinan usando un repo compartido de GitHub mediante `gh`:

1. **Issue de estado (`equipo-estado`)**: cada máquina mantiene su propio comentario (`<!-- equipo:estado:<maquina> -->`) con rama actual, archivos sin commitear, commits respecto a `origin/main`, agentes abiertos y tareas en curso.
2. **Asignación de trabajo (`maquina:<nombre>`)**: `equipo asignar` crea un issue etiquetado para esa máquina (un issue = una rama = un PR).
3. **Mensajería entre máquinas**: `equipo avisar` publica comentarios dirigidos (`<!-- equipo:msg:<destino> -->`) en el issue de estado; `equipo mensajes` lee solo los no vistos y guarda el cursor en `$AGENTES_HOME/estado/equipo-visto.json`.
