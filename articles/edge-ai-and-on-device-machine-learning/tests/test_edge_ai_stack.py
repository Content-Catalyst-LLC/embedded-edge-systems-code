from pathlib import Path


def test_expanded_stack_exists():
    root = Path(__file__).resolve().parents[1]
    expected_dirs = [
        "python", "r", "sql", "c", "cpp", "rust", "go", "micropython",
        "tinyml", "pynq", "hdl", "bash", "config", "notebooks",
        "docs", "data", "outputs", "tests", "model_lifecycle",
        "runtime_validation", "security"
    ]

    for directory in expected_dirs:
        assert (root / directory).exists(), f"Missing {directory}"


def test_engineering_grade_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    required_files = [
        root / "python" / "edge_ai_model_budget_quantization_simulation.py",
        root / "python" / "runtime_backend_validation.py",
        root / "python" / "confidence_fallback_decision_simulation.py",
        root / "python" / "fleet_drift_version_monitoring.py",
        root / "python" / "deployment_readiness_gate.py",
        root / "config" / "device_capability_profile.yml",
        root / "config" / "model_budget.yml",
        root / "config" / "sensor_feature_schema.json",
        root / "config" / "quantization_profile.yml",
        root / "config" / "runtime_manifest.yml",
        root / "config" / "backend_validation.yml",
        root / "config" / "decision_policy.yml",
        root / "config" / "deployment_readiness.yml",
        root / "data" / "sample_inference_events.csv",
        root / "data" / "backend_validation_report.csv",
        root / "data" / "model_inventory.csv",
        root / "hdl" / "verilog" / "stream_timestamper.v",
        root / "hdl" / "verilog" / "feature_window_counter.v",
        root / "hdl" / "verilog" / "inference_trigger.v",
        root / "hdl" / "verilog" / "telemetry_framer.v",
    ]

    for path in required_files:
        assert path.exists(), f"Missing expected edge AI artifact: {path}"
