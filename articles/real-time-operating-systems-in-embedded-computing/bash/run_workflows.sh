#!/usr/bin/env bash
set -euo pipefail

python3 python/scheduling_deadline_jitter_simulation.py

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/runtime_trace_fleet_analysis.R
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
