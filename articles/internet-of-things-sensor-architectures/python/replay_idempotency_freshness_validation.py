from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    policy = yaml.safe_load((root / "config/buffering_replay_policy.yml").read_text())["buffering_replay_policy"]
    telemetry = pd.read_csv(root / "data/telemetry_records.csv", parse_dates=["event_time", "upload_time", "ingestion_time", "processing_time"])

    telemetry["freshness_seconds"] = (telemetry["processing_time"] - telemetry["event_time"]).dt.total_seconds()
    telemetry["fresh"] = telemetry["freshness_seconds"] <= policy["freshness_threshold_seconds"]
    telemetry["has_idempotency_key"] = telemetry["idempotency_key"].notna() & (telemetry["idempotency_key"].astype(str).str.len() > 0)
    telemetry["has_sequence_number"] = telemetry["sequence_number"].notna()
    telemetry["is_backfill"] = telemetry["replay_batch_id"].notna()
    telemetry["backfill_has_replay_batch"] = (~telemetry["is_backfill"]) | telemetry["replay_batch_id"].notna()
    telemetry["replay_safe"] = telemetry["has_idempotency_key"] & telemetry["has_sequence_number"] & telemetry["backfill_has_replay_batch"]

    duplicates = telemetry.groupby("idempotency_key").size().reset_index(name="count")
    duplicates["idempotency_collision"] = duplicates["count"] > 1
    telemetry = telemetry.merge(duplicates[["idempotency_key", "idempotency_collision"]], on="idempotency_key", how="left")

    telemetry.to_csv(out / "python_replay_idempotency_freshness_validation.csv", index=False)

    summary = pd.DataFrame([{
        "records": len(telemetry),
        "fresh_rate": telemetry["fresh"].mean(),
        "backfill_rate": telemetry["is_backfill"].mean(),
        "duplicate_detected_rate": telemetry["duplicate_detected"].mean(),
        "idempotency_collision_rate": telemetry["idempotency_collision"].mean(),
        "replay_safe_rate": telemetry["replay_safe"].mean(),
        "mean_freshness_seconds": telemetry["freshness_seconds"].mean()
    }]).round(4)
    summary.to_csv(out / "python_replay_idempotency_freshness_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
