"""
Python Workflow: DC Motor Speed-Control Loop with Safety Filtering

This focused worked example mirrors the article's DC motor example:
setpoint -> encoder measurement -> speed estimate -> PID candidate command ->
safety filter -> PWM command -> log.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

from embedded_control_simulation import simulate


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    sim = simulate(duration_s=1.25, seed=21)

    focused = sim[[
        "time_s",
        "setpoint",
        "measurement",
        "estimate",
        "control_error",
        "candidate_command",
        "filtered_command",
        "saturated",
        "loop_jitter_ms",
        "deadline_slack_ms",
        "safety_filter_reason",
        "supervisory_state",
        "true_speed_rpm",
    ]].copy()

    focused.to_csv(output_dir / "python_dc_motor_speed_control_worked_example.csv", index=False)

    report = pd.DataFrame([{
        "max_speed_rpm": focused["true_speed_rpm"].max(),
        "final_speed_rpm": focused["true_speed_rpm"].iloc[-1],
        "mean_abs_error_rpm": focused["control_error"].abs().mean(),
        "saturation_rate": focused["saturated"].mean(),
        "minimum_deadline_slack_ms": focused["deadline_slack_ms"].min(),
        "safety_filter_events": int((focused["safety_filter_reason"] != "allowed").sum()),
    }]).round(4)

    report.to_csv(output_dir / "python_dc_motor_speed_control_summary.csv", index=False)
    print(report.to_string(index=False))


if __name__ == "__main__":
    run()
