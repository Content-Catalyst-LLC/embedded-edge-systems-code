"""
Python Workflow: Timing Budget and Deadline-Slack Analysis

This script validates whether observed control events fit within the configured
timing budget and summarizes deadline slack.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def load_timing_budget(article_root: Path) -> dict:
    with (article_root / "config" / "timing_budget.yml").open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)["timing_budget"]


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    timing = load_timing_budget(article_root)
    events_path = output_dir / "python_embedded_control_simulation.csv"

    if not events_path.exists():
        from embedded_control_simulation import simulate
        events = simulate()
    else:
        events = pd.read_csv(events_path)

    events = events.copy()
    events["deadline_valid"] = events["deadline_slack_ms"] >= 0
    events["jitter_valid"] = events["loop_jitter_ms"].abs() <= timing["jitter"]["max_allowed_jitter_ms"]
    events["timing_valid"] = events["deadline_valid"] & events["jitter_valid"]

    events.to_csv(output_dir / "python_timing_budget_validation.csv", index=False)

    summary = pd.DataFrame([{
        "events": len(events),
        "deadline_miss_rate": float((~events["deadline_valid"]).mean()),
        "jitter_violation_rate": float((~events["jitter_valid"]).mean()),
        "timing_violation_rate": float((~events["timing_valid"]).mean()),
        "minimum_deadline_slack_ms": float(events["deadline_slack_ms"].min()),
        "maximum_abs_jitter_ms": float(events["loop_jitter_ms"].abs().max()),
    }]).round(4)

    summary.to_csv(output_dir / "python_timing_budget_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
