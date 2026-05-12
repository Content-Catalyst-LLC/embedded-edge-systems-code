from pathlib import Path


def test_hdl_scaffold_exists():
    root = Path(__file__).resolve().parents[1]

    assert (root / "hdl" / "verilog" / "edge_stream_filter.v").exists()
    assert (root / "hdl" / "vhdl" / "edge_stream_filter.vhd").exists()
    assert (root / "hdl" / "constraints" / "README.md").exists()


def test_micropython_scaffold_exists():
    root = Path(__file__).resolve().parents[1]

    assert (root / "micropython" / "boot.py").exists()
    assert (root / "micropython" / "main.py").exists()
    assert (root / "micropython" / "sensor_reader.py").exists()
    assert (root / "micropython" / "telemetry_publisher.py").exists()


def test_bash_scaffold_exists():
    root = Path(__file__).resolve().parents[1]

    assert (root / "bash" / "run_workflows.sh").exists()
    assert (root / "bash" / "validate_manifests.sh").exists()
    assert (root / "bash" / "generate_outputs.sh").exists()
    assert (root / "bash" / "clean_outputs.sh").exists()
