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


def test_hdl_security_gate_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "hdl" / "verilog" / "secure_stream_gate.v").exists()
    assert (root / "hdl" / "vhdl" / "secure_stream_gate.vhd").exists()


def test_sample_security_data_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "sample_security_assets.csv").exists()
    assert (root / "data" / "sample_security_events.csv").exists()
