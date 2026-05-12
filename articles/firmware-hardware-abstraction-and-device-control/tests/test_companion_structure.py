from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_required_directories_exist():
    required = [
        "docs", "data", "outputs", "notebooks", "python", "r", "sql", "c", "cpp",
        "rust/src", "go", "micropython", "tinyml", "pynq", "hdl/verilog",
        "hdl/vhdl", "hdl/constraints", "bash", "config", "tests",
        "firmware", "hal", "drivers", "device_model", "register_access", "bsp",
        "startup", "interrupts", "power_management", "suspend_resume",
        "diagnostics", "telemetry", "observability", "updates", "security",
        "hil_validation", "concurrency", "lifecycle", "resource_arbitration"
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"missing {rel}"

def test_driver_manifest_is_valid_json():
    manifest = json.loads((ROOT / "config/driver_manifest.json").read_text())
    assert manifest["drivers"]
    assert all("driver_id" in item for item in manifest["drivers"])

def test_sample_data_exists():
    assert (ROOT / "data/driver_contracts.csv").exists()
    assert (ROOT / "data/device_lifecycle_events.csv").exists()
    assert (ROOT / "data/firmware_fleet_telemetry.csv").exists()
    assert (ROOT / "data/update_manifest.csv").exists()
