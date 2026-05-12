#!/usr/bin/env bash
set -euo pipefail
ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/iot_sensor_fleet_architecture_analysis.py"
python3 "$ARTICLE_DIR/python/replay_idempotency_freshness_validation.py"
python3 "$ARTICLE_DIR/python/trust_identity_lifecycle_validation.py"
python3 "$ARTICLE_DIR/python/command_authority_safety_boundary_evaluation.py"
python3 "$ARTICLE_DIR/python/deployment_readiness_gate.py"
python3 "$ARTICLE_DIR/pynq/pynq_iot_gateway_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/iot_sensor_fleet_health_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
