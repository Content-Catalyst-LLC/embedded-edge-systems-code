"""
Python Workflow: Synchronization and Conflict-Reconciliation Validation

This script validates whether state-lineage records preserve acquisition,
decision, synchronization, cloud ingestion, interpretation time, and version
context.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    lineage = pd.read_csv(article_root / "data" / "state_lineage_events.csv")
    conflict_policy = yaml.safe_load((article_root / "config" / "conflict_resolution_policy.yml").read_text(encoding="utf-8"))["conflict_resolution_policy"]

    time_columns = [
        "local_acquisition_time",
        "local_decision_time",
        "edge_persist_time",
        "sync_time",
        "cloud_ingest_time",
        "cloud_interpret_time",
    ]

    for col in time_columns:
        lineage[col] = pd.to_datetime(lineage[col], utc=True)

    lineage["state_age_s"] = (lineage["cloud_ingest_time"] - lineage["local_acquisition_time"]).dt.total_seconds()
    lineage["sync_lag_s"] = (lineage["cloud_ingest_time"] - lineage["edge_persist_time"]).dt.total_seconds()
    lineage["policy_drift"] = lineage["edge_policy_version"] != lineage["cloud_policy_version"]
    lineage["model_skew"] = lineage["edge_model_version"] != lineage["approved_model_version"]
    lineage["requires_reconciliation"] = lineage["policy_drift"] | lineage["model_skew"] | (lineage["state_age_s"] > 120)

    lineage.to_csv(output_dir / "python_state_lineage_validation.csv", index=False)

    summary = pd.DataFrame([{
        "events": len(lineage),
        "mean_state_age_s": lineage["state_age_s"].mean(),
        "max_sync_lag_s": lineage["sync_lag_s"].max(),
        "policy_drift_rate": lineage["policy_drift"].mean(),
        "model_skew_rate": lineage["model_skew"].mean(),
        "reconciliation_required_rate": lineage["requires_reconciliation"].mean(),
        "conflict_resolution_rule_count": len(conflict_policy.get("rules", {})),
    }]).round(4)

    summary.to_csv(output_dir / "python_sync_reconciliation_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
