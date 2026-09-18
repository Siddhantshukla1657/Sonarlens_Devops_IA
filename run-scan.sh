#!/usr/bin/env bash
# SonarLens scan launcher. DEMO ONLY - intentionally not hardened.
#
# Wraps the official sonarsource/sonar-scanner-cli image in a single
# command. Reads the repo's sonar-project.properties and pushes results
# to the local SonarQube server.
#
# Usage:
#   ./run-scan.sh [SONAR_HOST_URL] [SONAR_TOKEN]
#
# Examples:
#   SONAR_TOKEN=<token> ./run-scan.sh                       # Uses .env or defaults
#   ./run-scan.sh http://host.docker.internal:9000 <token>  # Override environment
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

if [ -f "$REPO_ROOT/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$REPO_ROOT/.env"
  set +a
fi

SONAR_HOST_URL="${1:-${SONAR_HOST_URL:-http://host.docker.internal:9000}}"
SONAR_TOKEN="${2:-${SONAR_TOKEN:-}}"

if [ -z "$SONAR_TOKEN" ]; then
  echo "SONAR_TOKEN is required. Set it in .env or pass it as the second argument." >&2
  exit 1
fi

docker run --rm \
  -e SONAR_HOST_URL="$SONAR_HOST_URL" \
  -e SONAR_TOKEN="$SONAR_TOKEN" \
  -v "$REPO_ROOT:/usr/src" \
  sonarsource/sonar-scanner-cli
