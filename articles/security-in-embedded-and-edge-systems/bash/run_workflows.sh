#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/security_readiness_scoring.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/fleet_security_posture_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

python3 "$ARTICLE_DIR/pynq/pynq_overlay_security_validation.py"

echo "Workflow run complete."
