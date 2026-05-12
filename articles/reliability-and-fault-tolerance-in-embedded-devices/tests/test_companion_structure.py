from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_required_directories_exist():
    required = [
        "docs", "data", "outputs", "notebooks", "python", "r", "sql", "c", "cpp",
        "rust/src", "go", "micropython", "tinyml", "pynq", "hdl/verilog",
        "hdl/vhdl", "hdl/constraints", "bash", "config", "tests",
        "fault_model", "watchdog", "recovery", "safe_state", "diagnostics",
        "observability", "field_evidence", "firmware", "telemetry", "runtime_validation",
        "lifecycle"
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"missing {rel}"

def test_fault_model_is_valid_json():
    manifest = json.loads((ROOT / "config/fault_model.json").read_text())
    assert manifest["fault_classes"]
    assert all("class" in item for item in manifest["fault_classes"])

def test_sample_data_exists():
    assert (ROOT / "data/fault_events.csv").exists()
    assert (ROOT / "data/device_fleet.csv").exists()
    assert (ROOT / "data/reset_log.csv").exists()
