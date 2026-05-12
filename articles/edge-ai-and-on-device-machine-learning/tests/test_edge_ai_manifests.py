from pathlib import Path
import json
import yaml


def test_json_manifests_are_valid():
    root = Path(__file__).resolve().parents[1]
    json_files = list((root / "config").glob("*.json")) + list((root / "tinyml").glob("*.json")) + list((root / "pynq").glob("*.json"))
    assert json_files

    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))


def test_yaml_manifests_are_valid():
    root = Path(__file__).resolve().parents[1]
    yaml_files = list((root / "config").glob("*.yml"))
    assert yaml_files

    for path in yaml_files:
        yaml.safe_load(path.read_text(encoding="utf-8"))
