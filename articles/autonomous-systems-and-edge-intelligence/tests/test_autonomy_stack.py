from pathlib import Path


def test_expanded_stack_exists():
    root = Path(__file__).resolve().parents[1]
    expected_dirs = [
        "python", "r", "sql", "c", "cpp", "rust", "go", "micropython",
        "tinyml", "pynq", "hdl", "bash", "config", "notebooks",
        "docs", "data", "outputs", "tests", "firmware", "hardware"
    ]

    for directory in expected_dirs:
        assert (root / directory).exists(), f"Missing {directory}"


def test_autonomy_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    required_files = [
        root / "python" / "autonomous_edge_decision_simulation.py",
        root / "python" / "runtime_assurance_filter.py",
        root / "python" / "autonomy_drift_monitoring.py",
        root / "c" / "bounded_autonomy_controller.c",
        root / "cpp" / "autonomy_state_machine.cpp",
        root / "hdl" / "verilog" / "timing_monitor.v",
        root / "hdl" / "verilog" / "safety_gate.v",
        root / "config" / "autonomy_profile.yml",
        root / "config" / "runtime_assurance.yml",
        root / "config" / "safety_envelope.yml",
        root / "config" / "compute_budget.yml",
    ]

    for path in required_files:
        assert path.exists(), f"Missing expected autonomy artifact: {path}"
