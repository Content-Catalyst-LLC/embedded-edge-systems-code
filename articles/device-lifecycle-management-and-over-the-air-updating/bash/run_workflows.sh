#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running available article workflows from: $ARTICLE_DIR"

if compgen -G "$ARTICLE_DIR/python/*.py" > /dev/null; then
  for script in "$ARTICLE_DIR"/python/*.py; do
    echo "Running Python workflow: $script"
    python3 "$script" || true
  done
fi

if compgen -G "$ARTICLE_DIR/r/*.R" > /dev/null; then
  for script in "$ARTICLE_DIR"/r/*.R; do
    echo "Running R workflow: $script"
    Rscript "$script" || true
  done
fi

if [ -f "$ARTICLE_DIR/pynq/pynq_overlay_lifecycle.py" ]; then
  echo "Running PYNQ manifest validation scaffold."
  python3 "$ARTICLE_DIR/pynq/pynq_overlay_lifecycle.py" || true
fi

echo "Workflow run complete."
