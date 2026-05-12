from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_required_directories_exist():
    required = [
        "docs", "data", "outputs", "notebooks", "python", "r", "sql", "c", "cpp",
        "rust/src", "go", "micropython", "tinyml", "pynq", "hdl/verilog",
        "hdl/vhdl", "hdl/constraints", "bash", "config", "tests",
        "task_models", "scheduling", "priority_assignment", "interrupts",
        "deferred_work", "synchronization", "queues", "stack_memory", "jitter",
        "deadline_analysis", "response_time", "priority_inversion", "power_management",
        "tickless_idle", "observability", "tracing", "telemetry", "overload",
        "watchdog", "field_validation", "hil_validation", "lifecycle"
    ]
    for rel in required:
        assert (ROOT / rel).exists(), f"missing {rel}"

def test_task_manifest_is_valid_json():
    manifest = json.loads((ROOT / "config/task_manifest.json").read_text())
    assert manifest["tasks"]
    assert all("task_name" in item for item in manifest["tasks"])

def test_sample_data_exists():
    assert (ROOT / "data/task_manifest.csv").exists()
    assert (ROOT / "data/runtime_trace.csv").exists()
    assert (ROOT / "data/queue_trace.csv").exists()
    assert (ROOT / "data/rtos_fleet_telemetry.csv").exists()
