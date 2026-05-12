#!/usr/bin/env bash
set -euo pipefail
ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$ARTICLE_DIR/outputs"
mkdir -p "$OUTPUT_DIR"
find "$OUTPUT_DIR" -type f ! -name "README.md" -delete
echo "Cleaned generated outputs."
