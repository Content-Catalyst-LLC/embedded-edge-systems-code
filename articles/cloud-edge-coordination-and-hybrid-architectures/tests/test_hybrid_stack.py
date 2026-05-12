from pathlib import Path


def test_expanded_stack_exists():
    root = Path(__file__).resolve().parents[1]
    expected_dirs = [
        "python", "r", "sql", "c", "cpp", "rust", "go", "micropython",
        "tinyml", "pynq", "hdl", "bash", "config", "notebooks",
        "docs", "data", "outputs", "tests", "gateway", "edge_runtime",
        "cloud_control_plane", "model_lifecycle", "security"
    ]

    for directory in expected_dirs:
        assert (root / directory).exists(), f"Missing {directory}"


def test_engineering_grade_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    required_files = [
        root / "python" / "cloud_edge_placement_sync_simulation.py",
        root / "python" / "rollout_convergence_analysis.py",
        root / "python" / "sync_reconciliation_validation.py",
        root / "python" / "hybrid_slo_authority_checks.py",
        root / "config" / "authority_policy.yml",
        root / "config" / "synchronization_contract.yml",
        root / "config" / "conflict_resolution_policy.yml",
        root / "config" / "degraded_mode_policy.yml",
        root / "config" / "rollout_policy.yml",
        root / "config" / "model_lifecycle_manifest.yml",
        root / "data" / "sample_hybrid_events.csv",
        root / "data" / "rollout_nodes.csv",
        root / "hdl" / "verilog" / "stream_timestamper.v",
        root / "hdl" / "verilog" / "buffer_watermark_monitor.v",
        root / "hdl" / "verilog" / "sync_pulse_generator.v",
        root / "hdl" / "verilog" / "telemetry_framer.v",
    ]

    for path in required_files:
        assert path.exists(), f"Missing expected hybrid artifact: {path}"
