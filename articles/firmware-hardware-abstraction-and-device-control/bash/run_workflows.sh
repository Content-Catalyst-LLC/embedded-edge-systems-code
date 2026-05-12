#!/usr/bin/env bash
set -euo pipefail

python3 python/driver_state_timing_simulation.py

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/firmware_telemetry_report.R
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
