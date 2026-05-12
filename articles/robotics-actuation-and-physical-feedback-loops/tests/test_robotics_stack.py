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


def test_robotics_control_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    required_files = [
        root / "python" / "state_space_feedback_simulation.py",
        root / "python" / "kalman_state_estimation.py",
        root / "python" / "safety_envelope_validator.py",
        root / "c" / "pid_control_loop.c",
        root / "cpp" / "robot_state_machine.cpp",
        root / "hdl" / "verilog" / "pwm_generator.v",
        root / "hdl" / "verilog" / "quadrature_decoder.v",
        root / "config" / "controller_config.yml",
        root / "config" / "estimator_config.yml",
        root / "config" / "safety_envelope.yml",
    ]

    for path in required_files:
        assert path.exists(), f"Missing expected robotics artifact: {path}"
