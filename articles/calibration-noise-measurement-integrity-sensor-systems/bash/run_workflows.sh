#!/usr/bin/env bash
set -euo pipefail
ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/sensor_calibration_noise_integrity_analysis.py"
python3 "$ARTICLE_DIR/python/measurement_quality_gate_evaluation.py"
python3 "$ARTICLE_DIR/python/drift_recalibration_monitoring.py"
python3 "$ARTICLE_DIR/python/traceability_calibration_control_validation.py"
python3 "$ARTICLE_DIR/python/deployment_readiness_gate.py"
python3 "$ARTICLE_DIR/pynq/pynq_measurement_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/sensor_fleet_measurement_quality_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
