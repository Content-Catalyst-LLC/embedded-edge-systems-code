#!/usr/bin/env bash
set -euo pipefail
ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/distributed_monitoring_health_coverage_analysis.py"
python3 "$ARTICLE_DIR/python/inference_boundary_fault_containment_evaluation.py"
python3 "$ARTICLE_DIR/python/replay_freshness_synchronization_validation.py"
python3 "$ARTICLE_DIR/python/aggregation_lineage_confidence_evaluation.py"
python3 "$ARTICLE_DIR/python/deployment_readiness_gate.py"
python3 "$ARTICLE_DIR/pynq/pynq_distributed_monitoring_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/distributed_monitoring_fleet_quality_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
