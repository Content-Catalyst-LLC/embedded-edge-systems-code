#!/usr/bin/env bash
set -euo pipefail

find outputs -maxdepth 1 -type f ! -name README.md -delete
echo "Cleaned generated outputs."
