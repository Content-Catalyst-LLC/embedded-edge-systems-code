"""
Python Workflow: Late Data, Replay, Deduplication, and Backfill Integrity Validation

This script checks replay records for idempotency, duplicate handling, late-arrival
behavior, gap detection, correction records, and replay lag.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    replay = pd.read_csv(article_root / "data" / "replay_records.csv")
    policy = yaml.safe_load((article_root / "config" / "replay_policy.yml").read_text(encoding="utf-8"))["replay_policy"]

    missing = [field for field in policy["required_fields"] if field not in replay.columns]
    if missing:
        raise ValueError(f"Missing replay fields: {missing}")

    replay["event_time_dt"] = pd.to_datetime(replay["event_time"], utc=True)
    replay["upstream_ingest_time_dt"] = pd.to_datetime(replay["upstream_ingest_time"], utc=True)
    replay["computed_replay_lag_s"] = (replay["upstream_ingest_time_dt"] - replay["event_time_dt"]).dt.total_seconds()

    replay["idempotency_seen_count"] = replay.groupby("idempotency_key")["idempotency_key"].transform("count")
    replay["computed_duplicate"] = replay["idempotency_seen_count"] > 1
    replay["duplicate_flag_correct"] = replay["computed_duplicate"] == replay["duplicate_detected"]

    replay.to_csv(output_dir / "python_replay_backfill_integrity_validation.csv", index=False)

    summary = pd.DataFrame([{
        "replay_records": len(replay),
        "late_arrival_rate": replay["late_arrival"].mean(),
        "duplicate_rate": replay["duplicate_detected"].mean(),
        "duplicate_flag_accuracy": replay["duplicate_flag_correct"].mean(),
        "gap_rate": replay["gap_detected"].mean(),
        "correction_rate": replay["correction_record"].mean(),
        "max_replay_lag_s": replay["computed_replay_lag_s"].max(),
    }]).round(4)

    summary.to_csv(output_dir / "python_replay_backfill_integrity_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
