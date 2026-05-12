"""
Python Workflow: Confidence, Fallback, and Local Decision Simulation

This script evaluates local action eligibility using confidence thresholds,
sensor health, approved model version, memory/latency status, and backend parity.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def decide(row: pd.Series) -> str:
    if row["confidence"] < row["confidence_threshold"]:
        return "fallback_more_samples"
    if row["sensor_health"] != "healthy":
        return "suppress_local_action_and_uplink"
    if row["model_version"] != row["approved_model_version"]:
        return "restrict_action_and_flag_version_skew"
    if row["backend_output_delta"] > row["backend_delta_tolerance"]:
        return "restrict_action_and_request_backend_review"
    if not bool(row["memory_ok"]):
        return "restrict_action_memory_budget_violation"
    if not bool(row["latency_ok"]):
        return "restrict_action_latency_budget_violation"
    if row["predicted_class"] == "fault":
        return "local_alarm"
    if row["predicted_class"] == "warning":
        return "uplink_for_review"
    return "no_action"


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    events_path = output_dir / "python_edge_ai_inference_events.csv"
    events = pd.read_csv(events_path) if events_path.exists() else pd.read_csv(article_root / "data" / "sample_inference_events.csv")

    events["computed_action"] = events.apply(decide, axis=1)
    events["action_matches_policy"] = events["computed_action"] == events["local_action"]
    events["computed_fallback_used"] = events["computed_action"].str.startswith(("fallback", "restrict", "suppress"))

    events.to_csv(output_dir / "python_confidence_fallback_decisions.csv", index=False)

    summary = pd.DataFrame([{
        "events": len(events),
        "computed_fallback_rate": events["computed_fallback_used"].mean(),
        "action_policy_match_rate": events["action_matches_policy"].mean(),
        "low_confidence_rate": (events["confidence"] < events["confidence_threshold"]).mean(),
        "unhealthy_sensor_rate": (events["sensor_health"] != "healthy").mean(),
        "backend_review_rate": (events["backend_output_delta"] > events["backend_delta_tolerance"]).mean(),
    }]).round(4)

    summary.to_csv(output_dir / "python_confidence_fallback_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
