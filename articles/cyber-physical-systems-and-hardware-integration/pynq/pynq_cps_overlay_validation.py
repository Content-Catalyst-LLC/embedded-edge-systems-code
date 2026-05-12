from __future__ import annotations

from pathlib import Path
import json


def main() -> None:
    manifest_path = Path(__file__).resolve().parent / "overlay_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    issues = []
    governance = manifest.get("governance", {})

    required_governance = [
        "requires_overlay_validation",
        "requires_runtime_compatibility_check",
        "records_timing_evidence",
        "records_lifecycle_evidence",
        "runtime_assurance_required",
    ]

    for key in required_governance:
        if not governance.get(key, False):
            issues.append(f"Missing governance flag: {key}")

    interface_names = {item.get("name") for item in manifest.get("interfaces", [])}
    for required in {"adc_stream", "encoder_stream", "filtered_state_stream", "pwm_command_stream", "safety_gate"}:
        if required not in interface_names:
            issues.append(f"Missing interface: {required}")

    print(f"Overlay: {manifest.get('overlay_name')} v{manifest.get('overlay_version')}")
    print("CPS overlay validation passed:", not issues)

    for issue in issues:
        print("-", issue)


if __name__ == "__main__":
    main()
