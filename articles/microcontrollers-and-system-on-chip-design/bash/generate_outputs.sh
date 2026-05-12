#!/usr/bin/env bash
set -euo pipefail

bash bash/run_workflows.sh
echo "Generated outputs:"
find outputs -maxdepth 1 -type f -print | sort
