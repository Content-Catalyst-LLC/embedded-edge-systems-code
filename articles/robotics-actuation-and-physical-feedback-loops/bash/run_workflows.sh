#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/state_space_feedback_simulation.py"
python3 "$ARTICLE_DIR/python/kalman_state_estimation.py"
python3 "$ARTICLE_DIR/python/safety_envelope_validator.py"
python3 "$ARTICLE_DIR/pynq/pynq_robotics_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/robotics_performance_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
