from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_required_directories_exist():
    required = [
        "docs", "data", "outputs", "notebooks", "python", "r", "sql", "c", "cpp",
        "rust/src", "go", "micropython", "tinyml", "pynq", "hdl/verilog",
        "hdl/vhdl", "hdl/constraints", "bash", "config", "tests"
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"missing {rel}"

def test_sensor_manifest_is_valid_json():
    manifest = json.loads((ROOT / "config/sensor_interface_manifest.json").read_text())
    assert manifest["interfaces"]
    assert all("channels" in item for item in manifest["interfaces"])

def test_sample_data_exists():
    assert (ROOT / "data/acquisition_events.csv").exists()
    assert (ROOT / "data/channel_manifest.csv").exists()
