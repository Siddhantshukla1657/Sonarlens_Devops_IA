@echo off
setlocal enabledelayedexpansion

set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"
cd /d "%REPO_ROOT%"

:: Auto-create .env from .env.example if missing
if not exist "%REPO_ROOT%\.env" (
    if exist "%REPO_ROOT%\.env.example" (
        echo [INFO] .env not found. Creating .env from .env.example...
        copy "%REPO_ROOT%\.env.example" "%REPO_ROOT%\.env" >nul
    )
)

:: Route based on first command-line argument (if provided)
set "COMMAND=%~1"
if /i "%COMMAND%"=="app" goto cmd_app
if /i "%COMMAND%"=="web" goto cmd_app
if /i "%COMMAND%"=="up" goto cmd_up
if /i "%COMMAND%"=="start" goto cmd_up
if /i "%COMMAND%"=="scan" goto cmd_scan
if /i "%COMMAND%"=="down" goto cmd_down
if /i "%COMMAND%"=="stop" goto cmd_down
if /i "%COMMAND%"=="status" goto cmd_status
if /i "%COMMAND%"=="help" goto cmd_help
if /i "%COMMAND%"=="--help" goto cmd_help
if /i "%COMMAND%"=="-h" goto cmd_help
if not "%COMMAND%"=="" (
    echo [ERROR] Unknown command "%COMMAND%".
    echo.
    goto cmd_help
)

:menu
cls
echo ============================================================
echo                      SonarLens Control
echo ============================================================
echo.
echo   [1] Start Flask Demo Application  (http://127.0.0.1:5000)
echo   [2] Start SonarQube Server        (Docker Compose up)
echo   [3] Run SonarQube Static Scan     (Docker Scanner container)
echo   [4] Check System and Status       (Docker, SonarQube, Python)
echo   [5] Stop SonarQube Server         (Docker Compose down)
echo   [6] Help / Command Reference
echo   [0] Exit
echo.
echo ============================================================
set "CHOICE="
set /p "CHOICE=Enter choice [0-6]: "

if "%CHOICE%"=="1" goto cmd_app
if "%CHOICE%"=="2" goto cmd_up
if "%CHOICE%"=="3" goto cmd_scan
if "%CHOICE%"=="4" goto cmd_status
if "%CHOICE%"=="5" goto cmd_down
if "%CHOICE%"=="6" goto cmd_help
if "%CHOICE%"=="0" goto :eof

echo Invalid option. Please enter a number between 0 and 6.
pause
goto menu

:check_python
set "PY_EXE="
if exist "%REPO_ROOT%\.venv\Scripts\python.exe" (
    set "PY_EXE=%REPO_ROOT%\.venv\Scripts\python.exe"
) else if exist "%REPO_ROOT%\venv\Scripts\python.exe" (
    set "PY_EXE=%REPO_ROOT%\venv\Scripts\python.exe"
) else (
    where python >nul 2>&1
    if not errorlevel 1 set "PY_EXE=python"
)

if "%PY_EXE%"=="" (
    echo [ERROR] Python was not found in .venv, venv, or system PATH.
    echo Please install Python 3.12+ or set up a virtual environment:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r app\requirements.txt
)
goto :eof

:check_docker
where docker >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker command was not found in PATH.
    echo Please ensure Docker Desktop is installed and added to PATH.
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker daemon is not running.
    echo Please start Docker Desktop and wait for the engine to report "Engine running".
    if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
        echo Docker Desktop executable detected at: "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    )
    exit /b 1
)
exit /b 0

:cmd_app
call :check_python
if "%PY_EXE%"=="" (
    if "%COMMAND%"=="" (pause & goto menu) else exit /b 1
)
echo.
echo ============================================================
echo Starting SonarLens Flask Application
echo Using: %PY_EXE%
echo URL:   http://127.0.0.1:5000
echo Endpoints:
echo   GET  http://127.0.0.1:5000/          ^<-- start here (index page)
echo   GET  http://127.0.0.1:5000/health
echo   GET  http://127.0.0.1:5000/tasks
echo   POST http://127.0.0.1:5000/tasks
echo   GET  http://127.0.0.1:5000/tasks/0
echo.
echo Press Ctrl+C to stop the application server.
echo ============================================================
echo.
set "PYTHONPATH=%REPO_ROOT%\app;%REPO_ROOT%;%PYTHONPATH%"
"%PY_EXE%" "%REPO_ROOT%\app\main.py"
goto :eof

:cmd_up
echo.
echo ============================================================
echo Starting SonarQube and Postgres containers...
echo ============================================================
call :check_docker
if errorlevel 1 (
    if "%COMMAND%"=="" (pause & goto menu) else exit /b 1
)
docker compose up -d
if errorlevel 1 (
    echo [ERROR] docker compose up failed.
) else (
    echo.
    echo [SUCCESS] SonarQube and Postgres containers started.
    echo Web UI will be available at: http://localhost:9000
    echo Note: First startup may take 1-2 minutes for database migration.
    echo Check logs anytime with: docker compose logs -f sonarqube
)
if "%COMMAND%"=="" (pause & goto menu) else exit /b 0

:cmd_scan
echo.
call "%REPO_ROOT%\run-scan.bat" %2 %3
if "%COMMAND%"=="" (pause & goto menu) else exit /b %ERRORLEVEL%

:cmd_down
echo.
echo ============================================================
echo Stopping SonarQube stack...
echo ============================================================
call :check_docker
if errorlevel 1 (
    if "%COMMAND%"=="" (pause & goto menu) else exit /b 1
)
docker compose down
echo Containers stopped.
if "%COMMAND%"=="" (pause & goto menu) else exit /b 0

:cmd_status
echo.
echo ============================================================
echo SonarLens Environment Status
echo ============================================================
echo.
echo [1] Python Environment:
call :check_python
if not "%PY_EXE%"=="" (
    echo   Python executable: %PY_EXE%
    "%PY_EXE%" --version
) else (
    echo   Python not found.
)
echo.
echo [2] Configuration:
if exist "%REPO_ROOT%\.env" (
    echo   .env file: Present
) else (
    echo   .env file: Missing ^(copy .env.example .env^)
)
echo.
echo [3] Docker Daemon:
where docker >nul 2>&1
if errorlevel 1 (
    echo   Docker CLI: Not found in PATH
) else (
    echo   Docker CLI: Installed
    docker info >nul 2>&1
    if errorlevel 1 (
        echo   Docker Daemon: NOT RUNNING ^(Start Docker Desktop^)
    ) else (
        echo   Docker Daemon: Running
        echo.
        echo [4] Containers:
        docker compose ps
    )
)
echo ============================================================
if "%COMMAND%"=="" (pause & goto menu) else exit /b 0

:cmd_help
echo ============================================================
echo SonarLens Batch Launcher Usage
echo ============================================================
echo.
echo Interactive mode:
echo   run.bat                  Open interactive menu
echo.
echo Direct commands:
echo   run.bat app              Start the Flask web app (http://127.0.0.1:5000)
echo   run.bat up               Start SonarQube server via Docker Compose
echo   run.bat scan [URL] [TOK] Run Sonar static code analysis
echo   run.bat status           Check Docker, SonarQube, and Python status
echo   run.bat down             Stop SonarQube Docker containers
echo   run.bat help             Show this help screen
echo ============================================================
if "%COMMAND%"=="" (pause & goto menu) else exit /b 0
