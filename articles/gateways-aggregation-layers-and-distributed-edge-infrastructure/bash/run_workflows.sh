#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ARTICLE_DIR/python/gateway_buffering_aggregation_simulation.py"
python3 "$ARTICLE_DIR/python/replay_dedup_validation.py"
python3 "$ARTICLE_DIR/python/gateway_slo_checks.py"
python3 "$ARTICLE_DIR/python/protocol_aggregation_quality_analysis.py"
python3 "$ARTICLE_DIR/pynq/pynq_gateway_overlay_validation.py"

if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/gateway_fleet_reliability_aggregation_reporting.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
