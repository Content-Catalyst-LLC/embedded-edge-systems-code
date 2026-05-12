from __future__ import annotations

from pathlib import Path
import json


def main() -> None:
    manifest_path = Path(__file__).resolve().parent / "overlay_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    issues = []
    required_interfaces = {
        "sensor_stream",
        "feature_window_stream",
        "timestamp_counter",
        "event_trigger",
        "telemetry_frame",
    }

    interface_names = {item.get("name") for item in manifest.get("interfaces", [])}

    for required in required_interfaces:
        if required not in interface_names:
            issues.append(f"Missing interface: {required}")

    validation = manifest.get("validation", {})
    for required_flag in [
        "requires_overlay_validation",
        "records_timing_evidence",
        "records_feature_schema_version",
        "records_lineage_evidence",
        "requires_fallback_path",
    ]:
        if not validation.get(required_flag, False):
            issues.append(f"Missing validation flag: {required_flag}")

    print(f"Overlay: {manifest.get('overlay_name')} v{manifest.get('overlay_version')}")
    print("Edge analytics overlay validation passed:", not issues)

    for issue in issues:
        print("-", issue)


if __name__ == "__main__":
    main()
