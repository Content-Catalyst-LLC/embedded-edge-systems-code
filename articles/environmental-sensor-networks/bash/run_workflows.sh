#!/usr/bin/env bash
set -euo pipefail

python3 python/environmental_network_simulation.py

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/environmental_network_report.R
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
