@echo off
setlocal enabledelayedexpansion

set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

:: Parse .env file if it exists
if exist "%REPO_ROOT%\.env" (
    for /f "usebackq eol=# tokens=1,* delims==" %%A in ("%REPO_ROOT%\.env") do (
        set "KEY=%%A"
        set "VAL=%%B"
        if not "!KEY!"=="" (
            :: Trim leading/trailing spaces if any
            for /f "tokens=* delims= " %%K in ("!KEY!") do set "KEY=%%K"
            if "!KEY!"=="SONAR_HOST_URL" if not defined SONAR_HOST_URL set "SONAR_HOST_URL=!VAL!"
            if "!KEY!"=="SONAR_TOKEN" if not defined SONAR_TOKEN set "SONAR_TOKEN=!VAL!"
        )
    )
)

:: Command-line argument overrides
if not "%~1"=="" set "SONAR_HOST_URL=%~1"
if not "%~2"=="" set "SONAR_TOKEN=%~2"

:: Default host URL for Docker Desktop on Windows
if "%SONAR_HOST_URL%"=="" set "SONAR_HOST_URL=http://host.docker.internal:9000"

:: Auto-fix localhost or 127.0.0.1 for container networking
echo %SONAR_HOST_URL% | findstr /i "localhost 127.0.0.1" >nul
if not errorlevel 1 (
    echo [INFO] Detected localhost in SONAR_HOST_URL.
    echo [INFO] Remapping to host.docker.internal so the scanner container can reach the host.
    set "SONAR_HOST_URL=!SONAR_HOST_URL:localhost=host.docker.internal!"
    set "SONAR_HOST_URL=!SONAR_HOST_URL:127.0.0.1=host.docker.internal!"
)

:: Check if Docker CLI is available
where docker >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker command was not found in PATH.
    echo Please make sure Docker Desktop is installed.
    exit /b 1
)

:: Check if Docker daemon is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to connect to Docker daemon.
    echo Docker Desktop is not currently running.
    echo Please start Docker Desktop, wait for it to report "Engine running", and try again.
    exit /b 1
)

:: Check if SONAR_TOKEN is set
if "%SONAR_TOKEN%"=="" (
    echo [ERROR] SONAR_TOKEN is required.
    echo Please set SONAR_TOKEN in your .env file or pass it as an argument:
    echo   run-scan.bat ^<SONAR_HOST_URL^> ^<SONAR_TOKEN^>
    exit /b 1
)

echo ============================================================
echo SonarLens Scanner Launcher
echo ============================================================
echo Sonar Host: %SONAR_HOST_URL%
echo Project Dir: %REPO_ROOT%
echo ============================================================

docker run --rm ^
  --add-host=host.docker.internal:host-gateway ^
  -e SONAR_HOST_URL="%SONAR_HOST_URL%" ^
  -e SONAR_TOKEN="%SONAR_TOKEN%" ^
  -v "%REPO_ROOT%:/usr/src" ^
  sonarsource/sonar-scanner-cli

exit /b %ERRORLEVEL%
