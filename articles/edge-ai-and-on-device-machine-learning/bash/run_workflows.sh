#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/edge_ai_model_budget_quantization_simulation.py"
python3 "$ARTICLE_DIR/python/runtime_backend_validation.py"
python3 "$ARTICLE_DIR/python/confidence_fallback_decision_simulation.py"
python3 "$ARTICLE_DIR/python/fleet_drift_version_monitoring.py"
python3 "$ARTICLE_DIR/python/deployment_readiness_gate.py"
python3 "$ARTICLE_DIR/pynq/pynq_edge_ai_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/edge_ai_fleet_monitoring_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
