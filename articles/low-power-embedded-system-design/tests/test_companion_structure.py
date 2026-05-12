from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_required_directories_exist():
    required = [
        "docs", "data", "outputs", "notebooks", "python", "r", "sql", "c", "cpp",
        "rust/src", "go", "micropython", "tinyml", "pynq", "hdl/verilog",
        "hdl/vhdl", "hdl/constraints", "bash", "config", "tests",
        "energy_budget", "power_states", "wake_sources", "retention", "peripherals",
        "communications", "sensing", "batteries", "energy_harvesting", "regulators",
        "brownout", "telemetry", "observability", "field_validation", "runtime_validation",
        "lifecycle", "firmware"
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"missing {rel}"

def test_power_manifest_is_valid_json():
    manifest = json.loads((ROOT / "config/power_manifest.json").read_text())
    assert manifest["power_states"]
    assert all("state" in item for item in manifest["power_states"])

def test_sample_data_exists():
    assert (ROOT / "data/power_states.csv").exists()
    assert (ROOT / "data/device_power_telemetry.csv").exists()
    assert (ROOT / "data/battery_profiles.csv").exists()
    assert (ROOT / "data/communication_energy.csv").exists()
