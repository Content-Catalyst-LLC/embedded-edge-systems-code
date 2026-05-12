#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/local_privacy_risk_scoring.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/edge_privacy_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

python3 "$ARTICLE_DIR/pynq/pynq_privacy_overlay_validation.py"
