from pathlib import Path


def test_expanded_stack_exists():
    root = Path(__file__).resolve().parents[1]
    expected_dirs = [
        "python", "r", "sql", "c", "cpp", "rust", "go", "micropython",
        "tinyml", "pynq", "hdl", "bash", "config", "notebooks",
        "docs", "data", "outputs", "tests", "analytics_runtime",
        "replay_backfill", "security"
    ]

    for directory in expected_dirs:
        assert (root / directory).exists(), f"Missing {directory}"


def test_engineering_grade_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    required_files = [
        root / "python" / "edge_stream_analytics_selective_uplink_simulation.py",
        root / "python" / "replay_backfill_integrity_validation.py",
        root / "python" / "analytics_slo_checks.py",
        root / "python" / "lineage_freshness_feature_quality_analysis.py",
        root / "python" / "deployment_readiness_gate.py",
        root / "config" / "signal_manifest.yml",
        root / "config" / "preprocessing_contract.yml",
        root / "config" / "window_policy.yml",
        root / "config" / "feature_schema.json",
        root / "config" / "event_logic_manifest.yml",
        root / "config" / "buffer_policy.yml",
        root / "config" / "replay_policy.yml",
        root / "config" / "selective_uplink_policy.yml",
        root / "config" / "analytics_slo.yml",
        root / "data" / "sample_analytics_events.csv",
        root / "data" / "sample_signal_windows.csv",
        root / "data" / "replay_records.csv",
        root / "hdl" / "verilog" / "stream_timestamper.v",
        root / "hdl" / "verilog" / "feature_window_counter.v",
        root / "hdl" / "verilog" / "feature_accumulator.v",
        root / "hdl" / "verilog" / "event_trigger.v",
        root / "hdl" / "verilog" / "telemetry_framer.v",
    ]

    for path in required_files:
        assert path.exists(), f"Missing expected edge analytics artifact: {path}"
