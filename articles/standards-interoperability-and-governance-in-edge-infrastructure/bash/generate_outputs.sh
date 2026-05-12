#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$ARTICLE_DIR/outputs"

mkdir -p "$OUTPUT_DIR"

echo "Generating output inventory..."

{
  echo "# Output Inventory"
  echo ""
  echo "Generated on: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo ""
  echo "Article directory: $ARTICLE_DIR"
  echo ""
  echo "Files:"
  find "$ARTICLE_DIR" -maxdepth 3 -type f | sed "s|$ARTICLE_DIR/|- |" | sort
} > "$OUTPUT_DIR/output_inventory.md"

echo "Wrote $OUTPUT_DIR/output_inventory.md"
