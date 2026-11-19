# SHERPAS-19-11 — Conversación y Coordinación Multi-Máquina (Windows)

Adaptación nativa para Windows (PowerShell / CMD / Windows Terminal) del sistema de conversación entre agentes y coordinación multi-máquina de [BauDahn/claude-central](https://github.com/BauDahn/claude-central).

## Instalación en Windows

En PowerShell (dentro de la carpeta del repo):

```powershell
# Añade agentes\bin al PATH de usuario y crea agentes\agentes.conf
.\instalar.ps1

# Opcional: registra la tarea programada cada 10 min para publicar estado
.\instalar.ps1 -ConTimer
```

Requisitos: Python 3.10+, `git` y GitHub CLI (`gh auth login`).

## Uso diario

```powershell
# 1. Inicializar cada máquina (una sola vez por máquina):
equipo init --maquina gabriel --rol orquestador --repo Gabriel-Borras/Sherpas-MaximosLocales --dir .
equipo init --maquina compa   --rol miembro     --repo Gabriel-Borras/Sherpas-MaximosLocales --dir .

# 2. Coordinación entre máquinas:
equipo ver                          # (orquestador) estado de máquinas, issues y PRs
equipo asignar compa "Título" --cuerpo "Qué hacer y archivos"
equipo mias                         # ver issues asignados a esta máquina
equipo avisar gabriel "PR #1 listo" # enviar mensaje a otra máquina
equipo mensajes                     # leer mensajes nuevos
estado                              # guarda ESTADO.md y publica en GitHub

# 3. Agentes y tablero local:
lanzar --listar                     # ver agentes en agentes.conf
lanzar backend                      # abre pestaña en Windows Terminal con el rol
tareas add "Implementar API" -p app --para backend
tareas tomar 1 -p app --como backend
tareas listo 1 -p app --nota "hecho"
```

> Si aún no reiniciaste la terminal tras `.\instalar.ps1`, puedes invocar `.\agentes\bin\equipo.cmd`, `.\agentes\bin\tareas.cmd`, `.\agentes\bin\lanzar.cmd` y `.\agentes\bin\estado.cmd`.

## Tests

```powershell
python -m unittest tests/test_sistema.py -v
```
