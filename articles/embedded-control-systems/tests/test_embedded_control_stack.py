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


def test_control_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    required_files = [
        root / "python" / "embedded_control_simulation.py",
        root / "python" / "dc_motor_speed_control.py",
        root / "python" / "timing_budget_analysis.py",
        root / "c" / "embedded_pid_controller.c",
        root / "cpp" / "supervisory_control_state_machine.cpp",
        root / "hdl" / "verilog" / "pwm_generator.v",
        root / "hdl" / "verilog" / "quadrature_decoder.v",
        root / "hdl" / "verilog" / "timing_monitor.v",
        root / "hdl" / "verilog" / "safety_gate.v",
        root / "config" / "controller_config.yml",
        root / "config" / "timing_budget.yml",
        root / "config" / "safety_envelope.yml",
        root / "config" / "supervisory_state_machine.yml",
    ]

    for path in required_files:
        assert path.exists(), f"Missing expected embedded control artifact: {path}"
