#!/usr/bin/env bash
set -euo pipefail

python3 python/silicon_fit_power_memory_model.py

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/platform_portfolio_comparison.R
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Workflow run complete."
