#!/usr/bin/env bash
set -euo pipefail

python3 python/fault_injection_availability_simulation.py

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/fleet_reliability_report.R
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
