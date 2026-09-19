param(
    [string]$SonarHostUrl,
    [string]$SonarToken
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

if (Test-Path (Join-Path $RepoRoot '.env')) {
    Get-Content (Join-Path $RepoRoot '.env') | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith('#')) {
            return
        }

        $parts = $line -split '=', 2
        if ($parts.Count -lt 2) {
            return
        }

        $key = $parts[0].Trim()
        $value = $parts[1].Trim().Trim('"').Trim("'")

        if ($key -and $value) {
            [System.Environment]::SetEnvironmentVariable($key, $value)
        }
    }
}

if (-not $SonarHostUrl) {
    $SonarHostUrl = $env:SONAR_HOST_URL
}
if (-not $SonarHostUrl) {
    $SonarHostUrl = 'http://host.docker.internal:9000'
}

if (-not $SonarToken) {
    $SonarToken = $env:SONAR_TOKEN
}

if ($SonarHostUrl -match 'localhost' -or $SonarHostUrl -match '127\.0\.0\.1') {
    Write-Host "[INFO] Detected localhost in SonarHostUrl. Remapping to host.docker.internal for container networking."
    $SonarHostUrl = $SonarHostUrl -replace 'localhost', 'host.docker.internal' -replace '127\.0\.0\.1', 'host.docker.internal'
}

if (-not $SonarToken) {
    Write-Error "SONAR_TOKEN is required. Set it in .env or pass it as the second argument."
    exit 1
}

# Pre-flight check: Docker CLI and Daemon
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker command was not found in PATH. Please install Docker Desktop."
    exit 1
}

& docker info 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to connect to Docker daemon. Docker Desktop is not running. Please launch Docker Desktop, wait for it to report 'Engine running', and try again."
    exit 1
}

& docker run --rm `
    --add-host="host.docker.internal:host-gateway" `
    -e "SONAR_HOST_URL=$SonarHostUrl" `
    -e "SONAR_TOKEN=$SonarToken" `
    -v "${RepoRoot}:/usr/src" `
    sonarsource/sonar-scanner-cli

exit $LASTEXITCODE
