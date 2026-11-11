#!/usr/bin/env bash
# Build dist/research-writing.zip for upload in claude.ai (Settings > Capabilities > Skills).
set -euo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$REPO_DIR/dist"
OUT="$REPO_DIR/dist/research-writing.zip"
rm -f "$OUT"
cd "$REPO_DIR/skills"
zip -rq "$OUT" research-writing -x '*/__pycache__/*' '*.pyc' '*/.DS_Store'
echo "Created $OUT"
