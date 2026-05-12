"""
Python Workflow: Uncertainty Budget Analysis

This script checks whether the total uncertainty budget remains inside the
decision tolerance for the cyber-physical system.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    with (article_root / "config" / "uncertainty_budget.yml").open("r", encoding="utf-8") as handle:
        budget = yaml.safe_load(handle)["uncertainty_budget"]

    events_path = output_dir / "python_cps_timing_sensing_actuation_events.csv"
    if events_path.exists():
        events = pd.read_csv(events_path)
    else:
        events = pd.read_csv(article_root / "data" / "sample_cps_events.csv")

    events = events.copy()
    events["uncertainty_fraction"] = events["total_uncertainty"] / events["uncertainty_budget"]
    events["uncertainty_band"] = pd.cut(
        events["uncertainty_fraction"],
        bins=[-float("inf"), budget["warning_fraction"], budget["fault_fraction"], float("inf")],
        labels=["normal", "warning", "fault"],
    )

    events.to_csv(output_dir / "python_uncertainty_budget_records.csv", index=False)

    summary = (
        events.groupby("uncertainty_band", observed=False)
        .size()
        .reset_index(name="events")
    )
    summary.to_csv(output_dir / "python_uncertainty_budget_summary.csv", index=False)

    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
