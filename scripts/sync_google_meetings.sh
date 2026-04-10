#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-${FGESTAO_BASE_URL:-https://aigestaoinovailab.com}}"
API_KEY="${FGESTAO_API_KEY:-${API_SECRET_KEY:-}}"
LIMIT="${FGESTAO_SYNC_LIMIT:-25}"

if [[ -z "${API_KEY}" ]]; then
  echo "Erro: defina FGESTAO_API_KEY ou API_SECRET_KEY antes de rodar o script." >&2
  exit 1
fi

curl --fail --silent --show-error \
  -X POST "${BASE_URL%/}/api/meetings/sync-google?limit=${LIMIT}" \
  -H "X-API-Key: ${API_KEY}" \
  -H "Content-Type: application/json"

echo
