from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_required_directories_exist():
    required = [
        "docs", "data", "outputs", "notebooks", "python", "r", "sql", "c", "cpp",
        "rust/src", "go", "micropython", "tinyml", "pynq", "hdl/verilog",
        "hdl/vhdl", "hdl/constraints", "bash", "config", "tests",
        "silicon_fit", "platform_selection", "memory_budget", "peripherals",
        "pin_mapping", "package_review", "clocking", "timing", "interrupts",
        "dma", "bus_interconnect", "power_domains", "energy_model", "boot_flow",
        "secure_boot", "updates", "debug_control", "security", "lifecycle",
        "diagnostics", "telemetry", "field_validation", "hil_validation",
        "accelerators", "heterogeneous_compute", "edge_inference", "software_ecosystem"
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"missing {rel}"

def test_platform_manifest_is_valid_json():
    manifest = json.loads((ROOT / "config/platform_manifest.json").read_text())
    assert manifest["platform_selection_dimensions"]
    assert manifest["candidate_requirements"]

def test_sample_data_exists():
    assert (ROOT / "data/candidate_platforms.csv").exists()
    assert (ROOT / "data/device_requirements.csv").exists()
    assert (ROOT / "data/peripheral_manifest.csv").exists()
    assert (ROOT / "data/power_domains.csv").exists()
    assert (ROOT / "data/security_lifecycle.csv").exists()
