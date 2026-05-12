from pathlib import Path
import json


def test_config_json_manifests_are_valid():
    root = Path(__file__).resolve().parents[1]
    config_dir = root / "config"

    assert config_dir.exists()

    json_files = list(config_dir.glob("*.json"))
    assert json_files, "Expected at least one JSON config manifest."

    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))


def test_required_config_files_exist():
    root = Path(__file__).resolve().parents[1]

    expected = [
        root / "config" / "article_manifest.yml",
        root / "config" / "device_profile.json",
        root / "config" / "telemetry_schema.json",
        root / "config" / "deployment_manifest.yml",
        root / "config" / "lifecycle_policy.yml",
        root / "config" / "update_policy.yml",
    ]

    for path in expected:
        assert path.exists(), f"Missing expected config file: {path}"
