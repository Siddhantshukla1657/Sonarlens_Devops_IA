#!/usr/bin/env bash
# SonarLens scan launcher. DEMO ONLY - intentionally not hardened.
#
# Wraps the official sonarsource/sonar-scanner-cli image in a single
# command. Reads the repo's sonar-project.properties and pushes results
# to the local SonarQube server.
#
# Usage:
#   ./run-scan.sh <SONAR_HOST_URL> <SONAR_TOKEN>
#
# Examples:
#   ./run-scan.sh http://host.docker.internal:9000 <token>   # Docker Desktop
#   ./run-scan.sh http://172.17.0.1:9000 <token>             # Linux
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <SONAR_HOST_URL> <SONAR_TOKEN>" >&2
  exit 1
fi

SONAR_HOST_URL="$1"
SONAR_TOKEN="$2"
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

docker run --rm \
  -e SONAR_HOST_URL="$SONAR_HOST_URL" \
  -e SONAR_TOKEN="$SONAR_TOKEN" \
  -v "$REPO_ROOT:/usr/src" \
  sonarsource/sonar-scanner-cli
