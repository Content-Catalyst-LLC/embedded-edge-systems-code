from pathlib import Path


def test_expanded_stack_exists():
    root = Path(__file__).resolve().parents[1]
    expected_dirs = [
        "python", "r", "sql", "c", "cpp", "rust", "go", "micropython",
        "tinyml", "pynq", "hdl", "bash", "config", "notebooks",
        "docs", "data", "outputs", "tests", "firmware", "hardware",
        "digital_twin", "hil", "requirements"
    ]

    for directory in expected_dirs:
        assert (root / directory).exists(), f"Missing {directory}"


def test_research_grade_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    required_files = [
        root / "python" / "cps_timing_sensing_actuation_simulation.py",
        root / "python" / "uncertainty_budget_analysis.py",
        root / "python" / "traceability_matrix_validation.py",
        root / "python" / "hil_digital_twin_readiness.py",
        root / "config" / "physical_interface_spec.yml",
        root / "config" / "interface_contracts.yml",
        root / "config" / "uncertainty_budget.yml",
        root / "config" / "timing_budget.yml",
        root / "config" / "safety_envelope.yml",
        root / "data" / "requirements_traceability_matrix.csv",
        root / "digital_twin" / "model_assumptions.yml",
        root / "hil" / "hil_test_plan.yml",
        root / "hdl" / "verilog" / "adc_sampler.v",
        root / "hdl" / "verilog" / "safety_gate.v",
        root / "hdl" / "verilog" / "timing_monitor.v",
    ]

    for path in required_files:
        assert path.exists(), f"Missing expected CPS artifact: {path}"
