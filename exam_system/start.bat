@echo off
chcp 65001 >nul
echo ==============================================
echo      SCAU Online Exam System
echo ==============================================
echo.
set "CURRENT_DIR=%~dp0"
cd /d "%CURRENT_DIR%"
echo Python: %CURRENT_DIR%venv\Scripts\python.exe
echo.
venv\Scripts\python.exe start_no_debug.py
