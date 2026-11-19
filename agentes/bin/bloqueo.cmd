@echo off
where python >nul 2>nul
if errorlevel 1 goto try_py
python "%~dp0bloqueo" %*
exit /b %errorlevel%
:try_py
py -3 "%~dp0bloqueo" %*
