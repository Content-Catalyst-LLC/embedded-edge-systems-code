from __future__ import annotations

from pathlib import Path
import json


def main() -> None:
    manifest_path = Path(__file__).resolve().parent / "overlay_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    issues = []
    integrity = manifest.get("integrity", {})
    governance = manifest.get("governance", {})

    if not integrity.get("signature_required", False):
        issues.append("Overlay signature requirement is missing.")

    if not integrity.get("hash"):
        issues.append("Overlay hash is missing.")

    if not governance.get("requires_overlay_validation", False):
        issues.append("Overlay validation requirement is missing.")

    if not governance.get("fallback_overlay_version"):
        issues.append("Fallback overlay version is missing.")

    print(f"Overlay: {manifest.get('overlay_name')} v{manifest.get('overlay_version')}")
    print("Security validation passed:", not issues)

    for issue in issues:
        print("-", issue)


if __name__ == "__main__":
    main()
