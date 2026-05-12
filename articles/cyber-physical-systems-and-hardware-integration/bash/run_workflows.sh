#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/cps_timing_sensing_actuation_simulation.py"
python3 "$ARTICLE_DIR/python/uncertainty_budget_analysis.py"
python3 "$ARTICLE_DIR/python/traceability_matrix_validation.py"
python3 "$ARTICLE_DIR/python/hil_digital_twin_readiness.py"
python3 "$ARTICLE_DIR/pynq/pynq_cps_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/cps_reliability_timing_integration_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
