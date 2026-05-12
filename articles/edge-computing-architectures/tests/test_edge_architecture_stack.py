from pathlib import Path

def test_expanded_stack_exists():
    root = Path(__file__).resolve().parents[1]
    expected_dirs = [
        "python", "r", "sql", "c", "cpp", "rust", "go", "micropython", "tinyml",
        "pynq", "hdl", "bash", "config", "notebooks", "docs", "data", "outputs",
        "tests", "runtime_assurance", "security", "deployment", "replay_offline"
    ]
    for directory in expected_dirs:
        assert (root / directory).exists(), f"Missing {directory}"
