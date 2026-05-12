from __future__ import annotations

from pathlib import Path
import json


def main() -> None:
    manifest_path = Path(__file__).resolve().parent / "overlay_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    issues = []
    governance = manifest.get("governance", {})

    if not governance.get("requires_overlay_validation", False):
        issues.append("Overlay validation requirement is missing.")

    if not governance.get("requires_runtime_compatibility_check", False):
        issues.append("Runtime compatibility check is missing.")

    if not governance.get("runtime_assurance_required", False):
        issues.append("Runtime assurance requirement is missing.")

    if not governance.get("records_timing_evidence", False):
        issues.append("Timing evidence recording is missing.")

    if not manifest.get("interfaces"):
        issues.append("No stream interfaces declared.")

    print(f"Overlay: {manifest.get('overlay_name')} v{manifest.get('overlay_version')}")
    print("Autonomy overlay validation passed:", not issues)

    for issue in issues:
        print("-", issue)


if __name__ == "__main__":
    main()
