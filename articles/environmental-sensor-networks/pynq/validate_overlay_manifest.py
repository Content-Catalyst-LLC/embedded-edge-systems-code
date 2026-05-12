import json
from pathlib import Path

manifest = json.loads(Path("overlay_manifest.json").read_text())
required = {"overlay_name", "purpose", "interfaces", "outputs"}
missing = required - set(manifest)
if missing:
    raise SystemExit(f"missing required overlay fields: {missing}")
print("environmental overlay manifest valid")
