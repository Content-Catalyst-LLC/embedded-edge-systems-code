"""
Python Workflow: Hybrid SLO and Authority-Window Checks

This script checks hybrid event records against SLOs for state age, sync lag,
buffer backlog, policy drift, model skew, degraded-mode rate, and reconciliation
conflict rate.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    with (article_root / "config" / "hybrid_slo.yml").open("r", encoding="utf-8") as handle:
        slo = yaml.safe_load(handle)["hybrid_slo"]

    events_path = output_dir / "python_cloud_edge_hybrid_events.csv"
    events = pd.read_csv(events_path) if events_path.exists() else pd.read_csv(article_root / "data" / "sample_hybrid_events.csv")

    events["state_age_violation"] = events["state_age_s"] > slo["max_state_age_s"]
    events["sync_lag_violation"] = events["sync_lag_s"] > slo["max_sync_lag_s"]
    events["buffer_backlog_violation"] = events["buffer_backlog"] > slo["max_buffer_backlog_events"]
    events["policy_drift"] = events["edge_policy_version"] != events["cloud_policy_version"]
    events["model_skew"] = events["edge_model_version"] != events["approved_model_version"]
    events["rollout_gap"] = events["active_version"] != events["target_version"]
    events["conflict"] = events["reconciliation_status"].isin(["conflict", "hold_for_review", "rollback_required"])

    checks = pd.DataFrame([{
        "state_age_violation_rate": events["state_age_violation"].mean(),
        "sync_lag_violation_rate": events["sync_lag_violation"].mean(),
        "buffer_backlog_violation_rate": events["buffer_backlog_violation"].mean(),
        "policy_drift_rate": events["policy_drift"].mean(),
        "model_skew_rate": events["model_skew"].mean(),
        "degraded_mode_rate": events["degraded_mode"].mean(),
        "reconciliation_conflict_rate": events["conflict"].mean(),
        "rollout_gap_rate": events["rollout_gap"].mean(),
        "authority_violation_rate": (~events["authority_valid"]).mean(),
    }]).round(4)

    checks["policy_drift_within_slo"] = checks["policy_drift_rate"] <= slo["max_policy_drift_rate"]
    checks["model_skew_within_slo"] = checks["model_skew_rate"] <= slo["max_model_skew_rate"]
    checks["degraded_mode_within_slo"] = checks["degraded_mode_rate"] <= slo["max_degraded_mode_rate"]
    checks["conflict_rate_within_slo"] = checks["reconciliation_conflict_rate"] <= slo["max_reconciliation_conflict_rate"]

    checks.to_csv(output_dir / "python_hybrid_slo_authority_checks.csv", index=False)
    print(checks.to_string(index=False))


if __name__ == "__main__":
    run()
