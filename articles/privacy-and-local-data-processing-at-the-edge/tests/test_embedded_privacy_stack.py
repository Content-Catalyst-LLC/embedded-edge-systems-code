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


def test_hdl_privacy_filter_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "hdl" / "verilog" / "privacy_stream_filter.v").exists()
    assert (root / "hdl" / "vhdl" / "privacy_stream_filter.vhd").exists()
