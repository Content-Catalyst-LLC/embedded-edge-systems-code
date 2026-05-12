from __future__ import annotations

from pathlib import Path
import json


def main() -> None:
    manifest_path = Path(__file__).resolve().parent / "overlay_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    governance = manifest.get("governance", {})
    issues = []

    if governance.get("raw_stream_export_allowed", True):
        issues.append("Raw stream export should be disabled for privacy-preserving overlay.")

    if not governance.get("requires_overlay_validation", False):
        issues.append("Overlay validation requirement is missing.")

    if not governance.get("records_privacy_evidence", False):
        issues.append("Privacy evidence recording is missing.")

    print(f"Overlay: {manifest.get('overlay_name')} v{manifest.get('overlay_version')}")
    print("Compatible:", not issues)

    for issue in issues:
        print("-", issue)


if __name__ == "__main__":
    main()
