param(
    [switch]$ConTimer
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BinDir = Join-Path $RepoRoot "agentes\bin"
$ConfEjemplo = Join-Path $RepoRoot "agentes\agentes.conf.example"
$Conf = Join-Path $RepoRoot "agentes\agentes.conf"

# 1. Añadir agentes\bin al PATH de usuario si no está
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$parts = if ($userPath) { $userPath -split ";" | Where-Object { $_ } } else { @() }
if ($parts -notcontains $BinDir) {
    $newPath = ($parts + $BinDir) -join ";"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "PATH de usuario actualizado con: $BinDir (abre una nueva terminal para usarlo)"
} else {
    Write-Host "PATH ya incluye: $BinDir"
}

# 2. Copiar agentes.conf si no existe
if (-not (Test-Path $Conf) -and (Test-Path $ConfEjemplo)) {
    Copy-Item $ConfEjemplo $Conf
    Write-Host "Creado: $Conf"
}

# 3. Registrar tarea programada cada 10 minutos (opcional con -ConTimer)
if ($ConTimer) {
    $EstadoCmd = Join-Path $BinDir "estado.cmd"
    $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$EstadoCmd`""
    $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 10)
    Register-ScheduledTask -TaskName "SHERPAS-Estado" -Action $action -Trigger $trigger -Description "Publica estado de agentes cada 10 min" -Force | Out-Null
    Write-Host "Tarea programada 'SHERPAS-Estado' registrada (cada 10 min)."
}
