"""
Python Workflow: Lineage, Freshness, and Feature-Completeness Analysis

This script summarizes feature completeness, missing samples, freshness,
compression, uplink mode, and lineage quality across sites, gateways, and signal
families.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    events_path = output_dir / "python_edge_analytics_events.csv"
    events = pd.read_csv(events_path) if events_path.exists() else pd.read_csv(article_root / "data" / "sample_analytics_events.csv")

    events["compression_ratio"] = 1 - (events["uplink_bytes"] / events["raw_bytes"]).clip(upper=1)
    events["stale_output"] = events["freshness_s"] > events["freshness_threshold_s"]

    summary = (
        events.groupby(["site_id", "gateway_id", "signal_family", "feature_version"])
        .agg(
            events=("event_id", "count"),
            feature_completeness_rate=("feature_complete", "mean"),
            mean_missing_sample_rate=("missing_sample_rate", "mean"),
            stale_output_rate=("stale_output", "mean"),
            lineage_completeness_rate=("lineage_complete", "mean"),
            mean_compression_ratio=("compression_ratio", "mean"),
            immediate_uplink_rate=("uplink_mode", lambda s: (s == "immediate").mean()),
            deferred_uplink_rate=("uplink_mode", lambda s: (s == "deferred").mean()),
            suppressed_rate=("uplink_mode", lambda s: (s == "suppressed").mean()),
            mean_buffer_backlog=("buffer_backlog", "mean"),
            mean_replay_lag_s=("replay_lag_s", "mean"),
        )
        .reset_index()
        .round(4)
    )

    summary.to_csv(output_dir / "python_lineage_freshness_feature_quality_summary.csv", index=False)

    overall = pd.DataFrame([{
        "events": len(events),
        "feature_completeness_rate": events["feature_complete"].mean(),
        "lineage_completeness_rate": events["lineage_complete"].mean(),
        "stale_output_rate": events["stale_output"].mean(),
        "mean_compression_ratio": events["compression_ratio"].mean(),
        "mean_buffer_backlog": events["buffer_backlog"].mean(),
        "mean_replay_lag_s": events["replay_lag_s"].mean(),
    }]).round(4)

    overall.to_csv(output_dir / "python_lineage_freshness_overall.csv", index=False)
    print(overall.to_string(index=False))


if __name__ == "__main__":
    run()
