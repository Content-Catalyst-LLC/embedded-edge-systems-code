#!/usr/bin/env bash
set -euo pipefail

test -f companion_manifest.yml
test -f config/acquisition_policy.yml
test -f config/sensor_interface_manifest.json
python3 -m json.tool config/sensor_interface_manifest.json >/dev/null
python3 -m json.tool pynq/overlay_manifest.json >/dev/null

echo "Manifest validation passed."
