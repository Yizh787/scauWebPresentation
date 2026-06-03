@echo off
echo ==============================================
echo      四川农业大学在线考试系统
echo ==============================================
echo 启动中，请稍候...
echo.
set "CURRENT_DIR=%~dp0"
cd /d "%CURRENT_DIR%"
echo 服务已启动，访问地址：http://127.0.0.1:5000
echo.
venv\Scripts\python.exe app.py