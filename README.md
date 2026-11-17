# Sistema de Conversación y Organización Multi-Máquina

Implementación multiplataforma (Windows / Linux / macOS) del sistema de conversación entre agentes y coordinación entre máquinas adaptado de [BauDahn/claude-central](https://github.com/BauDahn/claude-central).

## Estructura

| Ruta | Qué hace |
|---|---|
| `agentes/bin/equipo` (`equipo.cmd`) | Coordinación multi-máquina vía GitHub (`gh`): estado, issues por máquina, PRs y mensajería. |
| `agentes/bin/tareas` (`tareas.cmd`) | Tablero local de tareas con bloqueo de archivo atómico (`pendiente → en_curso → hecha`). |
| `central/CLAUDE.md` | Prompt del coordinador `central` (único punto de contacto con el usuario). |
| `agentes/roles/` | Protocolo de conversación (`_comun.md`) y roles (`orquestador`, `backend`, `frontend`, `revisor`, `seguridad`, `ideas`, `optimizador`). |
| `docs/ARQUITECTURA.md` | Detalle del protocolo de mensajes, roles y flujo multi-máquina. |

## Uso rápido

```bash
# 1. Configurar cada máquina (requiere `gh auth status` activo):
python agentes/bin/equipo init --maquina ana --rol orquestador --repo dueno/repo --dir .
python agentes/bin/equipo init --maquina beto --rol miembro --repo dueno/repo --dir .

# 2. Coordinar entre máquinas:
python agentes/bin/equipo ver                         # (orquestador) estado, issues y PRs
python agentes/bin/equipo asignar beto "título" --cuerpo "qué y archivos"
python agentes/bin/equipo mias                        # issues asignados a esta máquina
python agentes/bin/equipo avisar ana "PR #12 listo"   # mensaje a otra máquina
python agentes/bin/equipo mensajes                    # mensajes nuevos
python agentes/bin/equipo publicar                    # publica estado actual

# 3. Tablero local de subtareas:
python agentes/bin/tareas add "Implementar API" -p app --para backend
python agentes/bin/tareas tomar 1 -p app --como backend
python agentes/bin/tareas listo 1 -p app --nota "endpoints listos"
```

## Tests

```bash
python -m unittest tests/test_sistema.py -v
```
