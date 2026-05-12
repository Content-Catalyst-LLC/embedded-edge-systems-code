#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/cloud_edge_placement_sync_simulation.py"
python3 "$ARTICLE_DIR/python/rollout_convergence_analysis.py"
python3 "$ARTICLE_DIR/python/sync_reconciliation_validation.py"
python3 "$ARTICLE_DIR/python/hybrid_slo_authority_checks.py"
python3 "$ARTICLE_DIR/pynq/pynq_hybrid_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/hybrid_fleet_reliability_sync_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
