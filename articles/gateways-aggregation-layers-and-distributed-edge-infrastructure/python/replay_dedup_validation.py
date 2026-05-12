"""
Python Workflow: Replay, Deduplication, and Late-Arrival Validation

This script checks replay events for idempotency keys, duplicate detection,
late-arrival status, gap reporting, and reconciliation outcomes.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    replay = pd.read_csv(article_root / "data" / "replay_events.csv")
    replay_policy = yaml.safe_load((article_root / "config" / "replay_policy.yml").read_text(encoding="utf-8"))["replay_policy"]

    required = replay_policy["required_fields"]
    missing = [field for field in required if field not in replay.columns]
    if missing:
        raise ValueError(f"Missing replay fields: {missing}")

    replay["idempotency_seen_count"] = replay.groupby("idempotency_key")["idempotency_key"].transform("count")
    replay["computed_duplicate"] = replay["idempotency_seen_count"] > 1
    replay["duplicate_correctly_flagged"] = replay["computed_duplicate"] == replay["duplicate_detected"]

    replay["local_acquisition_time"] = pd.to_datetime(replay["local_acquisition_time"], utc=True)
    replay["upstream_ingest_time"] = pd.to_datetime(replay["upstream_ingest_time"], utc=True)
    replay["replay_lag_s"] = (replay["upstream_ingest_time"] - replay["local_acquisition_time"]).dt.total_seconds()

    replay.to_csv(output_dir / "python_replay_dedup_validation.csv", index=False)

    summary = pd.DataFrame([{
        "replay_records": len(replay),
        "duplicate_rate": replay["duplicate_detected"].mean(),
        "late_arrival_rate": replay["late_arrival"].mean(),
        "gap_rate": replay["gap_detected"].mean(),
        "duplicate_flag_accuracy": replay["duplicate_correctly_flagged"].mean(),
        "max_replay_lag_s": replay["replay_lag_s"].max(),
    }]).round(4)

    summary.to_csv(output_dir / "python_replay_dedup_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
