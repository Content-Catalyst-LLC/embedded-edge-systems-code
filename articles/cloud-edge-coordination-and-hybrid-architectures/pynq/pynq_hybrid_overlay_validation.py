from __future__ import annotations

from pathlib import Path
import json


def main() -> None:
    manifest_path = Path(__file__).resolve().parent / "overlay_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    issues = []
    required_interfaces = {
        "sensor_stream",
        "feature_stream",
        "timestamp_counter",
        "buffer_watermark",
        "selective_uplink_trigger",
    }

    interface_names = {item.get("name") for item in manifest.get("interfaces", [])}

    for required in required_interfaces:
        if required not in interface_names:
            issues.append(f"Missing interface: {required}")

    governance = manifest.get("governance", {})
    for required_flag in [
        "requires_overlay_validation",
        "records_timing_evidence",
        "records_lifecycle_evidence",
        "selective_uplink_policy_required",
    ]:
        if not governance.get(required_flag, False):
            issues.append(f"Missing governance flag: {required_flag}")

    print(f"Overlay: {manifest.get('overlay_name')} v{manifest.get('overlay_version')}")
    print("Hybrid overlay validation passed:", not issues)

    for issue in issues:
        print("-", issue)


if __name__ == "__main__":
    main()
