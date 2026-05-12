from pathlib import Path
import json


def test_json_manifests_are_valid():
    root = Path(__file__).resolve().parents[1]
    json_files = list((root / "config").glob("*.json")) + list((root / "tinyml").glob("*.json")) + list((root / "pynq").glob("*.json"))
    assert json_files

    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))


def test_required_config_files_exist():
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "config" / "device_security_profile.json",
        root / "config" / "boot_policy.yml",
        root / "config" / "firmware_manifest.json",
        root / "config" / "runtime_policy.yml",
        root / "config" / "network_boundary_manifest.yml",
        root / "config" / "security_event_schema.json",
        root / "config" / "lifecycle_policy.yml",
    ]

    for path in required:
        assert path.exists(), f"Missing expected config file: {path}"
