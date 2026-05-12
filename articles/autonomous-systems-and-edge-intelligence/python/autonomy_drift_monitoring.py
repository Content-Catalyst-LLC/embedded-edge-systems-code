"""
Python Workflow: Autonomy Drift Monitoring and Mission Reliability Analysis

This script summarizes input drift, confidence drift, fallback behavior,
intervention rate, latency violations, and safety events.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def summarize_drift(events: pd.DataFrame) -> pd.DataFrame:
    return (
        events.groupby(["device_id", "mission_type", "autonomy_level"], as_index=False)
        .agg(
            decisions=("device_id", "count"),
            mean_confidence=("decision_confidence", "mean"),
            fallback_rate=("action_type", lambda s: float((s == "fallback").mean())),
            intervention_rate=("human_intervention_required", "mean"),
            latency_violation_rate=("latency_ms", lambda s: float((s > events.loc[s.index, "latency_budget_ms"]).mean())),
            safety_events=("safety_state", lambda s: int((s != "normal").sum())),
            mean_input_drift=("input_drift_score", "mean"),
            max_input_drift=("input_drift_score", "max"),
            mean_confidence_drift=("confidence_drift_score", "mean"),
        )
        .round(4)
        .sort_values(["fallback_rate", "intervention_rate", "mean_input_drift"], ascending=[False, False, False])
    )


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    events = pd.read_csv(article_root / "data" / "sample_autonomy_events.csv")
    summary = summarize_drift(events)
    summary.to_csv(output_dir / "python_autonomy_drift_summary.csv", index=False)

    warnings = events[
        (events["input_drift_score"] >= 0.25)
        | (events["confidence_drift_score"] >= 0.20)
        | (events["latency_ms"] > events["latency_budget_ms"])
        | (events["safety_state"] != "normal")
    ].copy()

    warnings.to_csv(output_dir / "python_autonomy_drift_warnings.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
