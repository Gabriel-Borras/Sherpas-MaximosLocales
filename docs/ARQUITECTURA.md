# Arquitectura: conversación entre agentes y coordinación multi-máquina (Windows)

Sistema adaptado de [BauDahn/claude-central](https://github.com/BauDahn/claude-central) para correr de forma nativa en Windows (PowerShell, CMD y Windows Terminal) manteniendo compatibilidad con POSIX.

## 1. Organización local de agentes

- **`central`** (`central\CLAUDE.md`): único punto de contacto con el usuario. Supervisa sesiones, delega trabajo y resume resultados.
- **`orquestador`** (`agentes\roles\orquestador.md`): descompone tareas grandes en subtareas, crea tickets en el tablero (`tareas`) y asigna trabajo sin pisar archivos.
- **Especialistas** (`agentes\roles\*.md`): `backend`, `frontend`, `revisor`, `seguridad`, `ideas`, `optimizador`.
- **Lanzador en Windows (`agentes\bin\lanzar.cmd`)**: abre cada agente en una pestaña de Windows Terminal (`wt.exe`) o nueva ventana PowerShell con `$env:AGENTE` y su prompt de rol (`roles\<rol>.md` + `_comun.md`).

### Protocolo de mensajes entre sesiones

| Mensaje | De → a | Significado |
|---|---|---|
| `ASIGNA: <agente> <tarea> \| contexto: <rutas>` | orquestador → agente | Encargo de tarea y rutas de contexto. |
| `NECESITA: <agente> <qué>` | agente → orquestador | Falta contexto o dependencia de otro agente. |
| `LISTO: <resumen> \| archivos: <rutas>` | agente → orquestador | Subtarea terminada y archivos tocados. |
| `PEDIR-CONTEXTO: <qué> \| fuente: <ruta/url> \| para: <agente>` | agente → optimizador | Solicitud de resumen/mapa compacto. |
| `CONTEXTO-LISTO: <ruta> (~N tokens) — <resumen>` | optimizador → agente | Contexto compacto disponible en disco. |

## 2. Tablero atómico de tareas (`agentes\bin\tareas.cmd`)

Almacena el estado en `agentes\tareas\<proyecto>.json` (o `$env:AGENTES_HOME\tareas\`) con bloqueo exclusivo nativo en Windows (`msvcrt.locking`, y `fcntl.flock` en POSIX):

- `pendiente` → `en_curso` → `hecha` (o `bloqueada`).
- `tomar` es atómico: evita que dos agentes tomen la misma tarea o ignoren dependencias (`--dep`).

## 3. Estado local y publicación periódica (`agentes\bin\estado.cmd`)

Reemplaza al script bash y timer de `systemd`: genera `agentes\estado\ESTADO.md` con agentes abiertos y tareas pendientes, y si existe `agentes\equipo.conf` ejecuta `equipo publicar`. Se puede programar cada 10 min en el Programador de tareas de Windows ejecutando `.\instalar.ps1 -ConTimer`.

## 4. Coordinación multi-máquina (`agentes\bin\equipo.cmd`)

Varias máquinas Windows (cada una con su `central`) se coordinan usando el repo compartido de GitHub mediante `gh`:

1. **Issue de estado (`equipo-estado`)**: cada máquina mantiene su propio comentario (`<!-- equipo:estado:<maquina> -->`) con rama, cambios sin commitear, commits respecto a `origin/main`, agentes abiertos y tareas en curso.
2. **Asignación de trabajo (`maquina:<nombre>`)**: `equipo asignar` crea un issue etiquetado para esa máquina (un issue = una rama = un PR).
3. **Mensajería entre máquinas**: `equipo avisar` publica comentarios dirigidos (`<!-- equipo:msg:<destino> -->`) en el issue de estado; `equipo mensajes` lee solo los no vistos y guarda el cursor en `agentes\estado\equipo-visto.json`.
