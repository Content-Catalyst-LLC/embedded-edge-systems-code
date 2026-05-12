#!/usr/bin/env bash
set -euo pipefail

python3 python/power_budget_lifetime_simulation.py

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/fleet_power_report.R
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
