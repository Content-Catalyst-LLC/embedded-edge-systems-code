"""
PYNQ Companion Example: Overlay Lifecycle and Compatibility Validation

This script is a portable governance scaffold. It does not require PYNQ hardware
to run. On an actual PYNQ board, the validation step can be extended to load a
.bit file with pynq.Overlay and verify that the deployed overlay matches the
expected lifecycle and interface contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Dict, List


@dataclass(frozen=True)
class OverlayValidationResult:
    overlay_name: str
    overlay_version: str
    compatible: bool
    issues: List[str]


def load_manifest(path: Path) -> Dict[str, Any]:
    """Load a PYNQ overlay manifest."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_overlay_manifest(manifest: Dict[str, Any]) -> OverlayValidationResult:
    """Validate minimal governance requirements for an FPGA overlay."""
    issues: List[str] = []

    required_top_level = [
        "overlay_name",
        "overlay_version",
        "bitstream_file",
        "hardware_target",
        "interfaces",
        "governance",
    ]

    for field in required_top_level:
        if field not in manifest:
            issues.append(f"Missing required field: {field}")

    governance = manifest.get("governance", {})
    if not governance.get("requires_overlay_validation", False):
        issues.append("Overlay validation requirement is not enabled.")

    if not governance.get("requires_runtime_compatibility_check", False):
        issues.append("Runtime compatibility check is not enabled.")

    if not governance.get("fallback_overlay_version"):
        issues.append("Fallback overlay version is not declared.")

    interfaces = manifest.get("interfaces", [])
    if not interfaces:
        issues.append("No hardware/software interfaces are declared.")

    return OverlayValidationResult(
        overlay_name=manifest.get("overlay_name", "unknown"),
        overlay_version=manifest.get("overlay_version", "unknown"),
        compatible=len(issues) == 0,
        issues=issues,
    )


def main() -> None:
    manifest_path = Path(__file__).resolve().parent / "overlay_manifest.json"
    manifest = load_manifest(manifest_path)
    result = validate_overlay_manifest(manifest)

    print(f"Overlay: {result.overlay_name} v{result.overlay_version}")
    print(f"Compatible: {result.compatible}")

    if result.issues:
        print("Issues:")
        for issue in result.issues:
            print(f"- {issue}")


if __name__ == "__main__":
    main()
