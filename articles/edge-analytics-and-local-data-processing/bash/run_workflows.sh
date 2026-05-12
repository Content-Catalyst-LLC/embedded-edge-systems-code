#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/edge_stream_analytics_selective_uplink_simulation.py"
python3 "$ARTICLE_DIR/python/replay_backfill_integrity_validation.py"
python3 "$ARTICLE_DIR/python/analytics_slo_checks.py"
python3 "$ARTICLE_DIR/python/lineage_freshness_feature_quality_analysis.py"
python3 "$ARTICLE_DIR/python/deployment_readiness_gate.py"
python3 "$ARTICLE_DIR/pynq/pynq_edge_analytics_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/edge_analytics_fleet_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
