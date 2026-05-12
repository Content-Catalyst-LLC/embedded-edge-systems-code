from pathlib import Path
import json


def test_json_manifests_are_valid():
    root = Path(__file__).resolve().parents[1]
    json_files = list((root / "config").glob("*.json")) + list((root / "tinyml").glob("*.json")) + list((root / "pynq").glob("*.json"))
    assert json_files
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))


def test_privacy_workflow_data_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "sample_edge_privacy_events.csv").exists()
    assert (root / "data" / "sample_retention_policy.csv").exists()
