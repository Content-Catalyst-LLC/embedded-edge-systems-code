"""
Python Workflow: Analytics SLO and Capacity-Budget Checks

This script checks local analytics events against freshness, latency, feature
completeness, lineage, buffer backlog, replay lag, drop transparency, missing
sample, and duplicate replay objectives.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    slo = yaml.safe_load((article_root / "config" / "analytics_slo.yml").read_text(encoding="utf-8"))["analytics_slo"]

    events_path = output_dir / "python_edge_analytics_events.csv"
    events = pd.read_csv(events_path) if events_path.exists() else pd.read_csv(article_root / "data" / "sample_analytics_events.csv")
    replay = pd.read_csv(article_root / "data" / "replay_records.csv")

    checks = pd.DataFrame([{
        "p95_local_latency_ms": events["local_latency_ms"].quantile(0.95),
        "stale_output_rate": (events["freshness_s"] > events["freshness_threshold_s"]).mean(),
        "feature_completeness_rate": events["feature_complete"].mean(),
        "lineage_completeness_rate": events["lineage_complete"].mean(),
        "max_buffer_backlog": events["buffer_backlog"].max(),
        "p95_replay_lag_s": events["replay_lag_s"].quantile(0.95),
        "drop_transparency_rate": ((events["drop_reason"] != "") & events["drop_reason"].notna()).mean(),
        "high_missing_sample_rate": (events["missing_sample_rate"] > slo["max_missing_sample_rate"]).mean(),
        "duplicate_replay_rate": replay["duplicate_detected"].mean(),
    }]).round(4)

    checks["latency_within_slo"] = checks["p95_local_latency_ms"] <= slo["p95_local_latency_ms"]
    checks["freshness_within_slo"] = checks["stale_output_rate"] <= slo["max_stale_output_rate"]
    checks["feature_completeness_within_slo"] = checks["feature_completeness_rate"] >= slo["min_feature_completeness_rate"]
    checks["lineage_within_slo"] = checks["lineage_completeness_rate"] >= slo["min_lineage_completeness_rate"]
    checks["buffer_backlog_within_slo"] = checks["max_buffer_backlog"] <= slo["max_buffer_backlog_records"]
    checks["replay_lag_within_slo"] = checks["p95_replay_lag_s"] <= slo["max_replay_lag_s"]
    checks["drop_transparency_within_slo"] = checks["drop_transparency_rate"] >= slo["min_drop_transparency_rate"]
    checks["missing_sample_within_slo"] = checks["high_missing_sample_rate"] <= slo["max_missing_sample_rate"]
    checks["duplicate_replay_within_slo"] = checks["duplicate_replay_rate"] <= slo["max_duplicate_replay_rate"]

    checks.to_csv(output_dir / "python_analytics_slo_checks.csv", index=False)
    print(checks.to_string(index=False))


if __name__ == "__main__":
    run()
