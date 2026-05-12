from pathlib import Path
import json
import yaml

def test_expanded_stack_exists():
    root = Path(__file__).resolve().parents[1]
    expected_dirs = [
        "python", "r", "sql", "c", "cpp", "rust", "go", "micropython",
        "tinyml", "pynq", "hdl", "bash", "config", "notebooks",
        "docs", "data", "outputs", "tests"
    ]
    for directory in expected_dirs:
        assert (root / directory).exists(), f"Missing {directory}"

def test_json_manifests_are_valid():
    root = Path(__file__).resolve().parents[1]
    for path in list((root / "config").glob("*.json")) + list((root / "tinyml").glob("*.json")) + list((root / "pynq").glob("*.json")):
        json.loads(path.read_text())

def test_yaml_manifests_are_valid():
    root = Path(__file__).resolve().parents[1]
    for path in (root / "config").glob("*.yml"):
        yaml.safe_load(path.read_text())
