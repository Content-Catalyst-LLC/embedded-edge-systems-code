#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/embedded_control_simulation.py"
python3 "$ARTICLE_DIR/python/dc_motor_speed_control.py"
python3 "$ARTICLE_DIR/python/timing_budget_analysis.py"
python3 "$ARTICLE_DIR/pynq/pynq_control_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/control_loop_performance_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
