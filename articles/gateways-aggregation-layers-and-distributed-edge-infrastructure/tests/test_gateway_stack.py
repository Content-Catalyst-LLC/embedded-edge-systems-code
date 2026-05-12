from pathlib import Path


def test_expanded_stack_exists():
    root = Path(__file__).resolve().parents[1]
    expected_dirs = [
        "python", "r", "sql", "c", "cpp", "rust", "go", "micropython",
        "tinyml", "pynq", "hdl", "bash", "config", "notebooks",
        "docs", "data", "outputs", "tests", "gateway_runtime",
        "aggregation_layer", "security"
    ]

    for directory in expected_dirs:
        assert (root / directory).exists(), f"Missing {directory}"


def test_engineering_grade_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    required_files = [
        root / "python" / "gateway_buffering_aggregation_simulation.py",
        root / "python" / "replay_dedup_validation.py",
        root / "python" / "gateway_slo_checks.py",
        root / "python" / "protocol_aggregation_quality_analysis.py",
        root / "config" / "gateway_manifest.yml",
        root / "config" / "protocol_map.yml",
        root / "config" / "aggregation_contract.yml",
        root / "config" / "buffer_policy.yml",
        root / "config" / "replay_policy.yml",
        root / "config" / "gateway_slo.yml",
        root / "data" / "child_device_registry.csv",
        root / "data" / "sample_gateway_events.csv",
        root / "data" / "replay_events.csv",
        root / "hdl" / "verilog" / "stream_timestamper.v",
        root / "hdl" / "verilog" / "buffer_watermark_monitor.v",
        root / "hdl" / "verilog" / "sync_pulse_generator.v",
        root / "hdl" / "verilog" / "telemetry_framer.v",
    ]

    for path in required_files:
        assert path.exists(), f"Missing expected gateway artifact: {path}"
