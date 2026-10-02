@echo off
setlocal
cd /d "%~dp0"
set "RESUME_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%RESUME_PYTHON%" (
  "%RESUME_PYTHON%" scripts\editor_server.py
) else (
  py -3 scripts\editor_server.py
)
if errorlevel 1 pause
