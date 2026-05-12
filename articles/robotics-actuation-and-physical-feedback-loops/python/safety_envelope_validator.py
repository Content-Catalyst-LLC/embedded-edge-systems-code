"""
Python Workflow: Safety Envelope and Command-Bound Validation

This script validates robot control-loop events against safety constraints.
"""

from __future__ import annotations

from pathlib import Path
import json

import pandas as pd
import yaml


def load_safety_envelope(path: Path) -> dict:
    """Load a YAML safety envelope."""
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)["safety_envelope"]


def validate_control_log(control_log: pd.DataFrame, envelope: dict) -> pd.DataFrame:
    """Validate control-loop events against configured safety thresholds."""
    rows = []

    for _, row in control_log.iterrows():
        violations = []

        if abs(row["tracking_error"]) >= envelope["tracking_error_fault"]:
            violations.append("tracking_error_fault")
        elif abs(row["tracking_error"]) >= envelope["tracking_error_warning"]:
            violations.append("tracking_error_warning")

        if abs(row["command"]) > envelope["command_max_abs"]:
            violations.append("command_bound_violation")

        if row["actuator_current_a"] > envelope["current_max_a"]:
            violations.append("current_limit_violation")

        if row["loop_jitter_ms"] >= envelope["loop_jitter_fault_ms"]:
            violations.append("loop_jitter_fault")
        elif row["loop_jitter_ms"] >= envelope["loop_jitter_warning_ms"]:
            violations.append("loop_jitter_warning")

        rows.append({
            "timestamp": row["timestamp"],
            "robot_id": row["robot_id"],
            "joint_id": row["joint_id"],
            "violations": ",".join(violations) if violations else "none",
            "violation_count": len(violations),
            "safe": len(violations) == 0,
        })

    return pd.DataFrame(rows)


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    data_path = article_root / "data" / "sample_control_loop_log.csv"
    envelope_path = article_root / "config" / "safety_envelope.yml"
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    control_log = pd.read_csv(data_path)
    envelope = load_safety_envelope(envelope_path)
    validation = validate_control_log(control_log, envelope)

    validation.to_csv(output_dir / "python_safety_envelope_validation.csv", index=False)

    summary = pd.DataFrame([{
        "events": len(validation),
        "safe_events": int(validation["safe"].sum()),
        "violating_events": int((~validation["safe"]).sum()),
        "violation_rate": float((~validation["safe"]).mean()),
    }]).round(4)

    summary.to_csv(output_dir / "python_safety_validation_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
