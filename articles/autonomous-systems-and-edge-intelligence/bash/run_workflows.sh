#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/autonomous_edge_decision_simulation.py"
python3 "$ARTICLE_DIR/python/runtime_assurance_filter.py"
python3 "$ARTICLE_DIR/python/autonomy_drift_monitoring.py"
python3 "$ARTICLE_DIR/pynq/pynq_autonomy_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/autonomy_monitoring_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
