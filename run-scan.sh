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

# Remap localhost to host.docker.internal if running in Docker Desktop / bridge mode
if [[ "$SONAR_HOST_URL" == *"localhost"* ]] || [[ "$SONAR_HOST_URL" == *"127.0.0.1"* ]]; then
  echo "[INFO] Detected localhost in SONAR_HOST_URL. Remapping to host.docker.internal for container networking."
  SONAR_HOST_URL="${SONAR_HOST_URL//localhost/host.docker.internal}"
  SONAR_HOST_URL="${SONAR_HOST_URL//127.0.0.1/host.docker.internal}"
fi

if [ -z "$SONAR_TOKEN" ]; then
  echo "SONAR_TOKEN is required. Set it in .env or pass it as the second argument." >&2
  exit 1
fi

docker run --rm \
  --add-host=host.docker.internal:host-gateway \
  -e SONAR_HOST_URL="$SONAR_HOST_URL" \
  -e SONAR_TOKEN="$SONAR_TOKEN" \
  -v "$REPO_ROOT:/usr/src" \
  sonarsource/sonar-scanner-cli
