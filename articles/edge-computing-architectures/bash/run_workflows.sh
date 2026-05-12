#!/usr/bin/env bash
set -euo pipefail
ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/edge_workload_placement_continuity_simulation.py"
python3 "$ARTICLE_DIR/python/runtime_assurance_degraded_mode_checks.py"
python3 "$ARTICLE_DIR/python/trust_boundary_security_validation.py"
python3 "$ARTICLE_DIR/python/deployment_readiness_gate.py"
python3 "$ARTICLE_DIR/python/edge_observability_fleet_health_analysis.py"
python3 "$ARTICLE_DIR/pynq/pynq_edge_architecture_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/edge_fleet_reporting_architecture_health.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
