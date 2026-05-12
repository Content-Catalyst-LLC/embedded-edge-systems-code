"""
Python Workflow: Protocol Mediation and Aggregation Quality Analysis

This script summarizes protocol error rates, unit coverage, lineage completeness,
and site-state quality across gateways and protocol families.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    events_path = output_dir / "python_gateway_events.csv"
    events = pd.read_csv(events_path) if events_path.exists() else pd.read_csv(article_root / "data" / "sample_gateway_events.csv")

    protocol_map = yaml.safe_load((article_root / "config" / "protocol_map.yml").read_text(encoding="utf-8"))["protocol_map"]
    mapped_protocols = {entry["protocol_family"] for entry in protocol_map["mappings"].values()}

    events["protocol_mapped"] = events["protocol_family"].isin(mapped_protocols)
    events["unit_present"] = events["unit"].notna() & (events["unit"].astype(str).str.len() > 0)

    protocol_summary = (
        events.groupby(["gateway_id", "protocol_family"])
        .agg(
            events=("event_id", "count"),
            protocol_error_rate=("protocol_error", "mean"),
            lineage_completeness_rate=("lineage_complete", "mean"),
            unit_coverage=("unit_present", "mean"),
            mapped_coverage=("protocol_mapped", "mean"),
            mean_freshness_s=("device_freshness_s", "mean"),
            mean_replay_lag_s=("replay_lag_s", "mean"),
        )
        .reset_index()
        .round(4)
    )

    protocol_summary.to_csv(output_dir / "python_protocol_aggregation_quality_summary.csv", index=False)

    overall = pd.DataFrame([{
        "protocol_families": events["protocol_family"].nunique(),
        "mapped_protocol_coverage": events["protocol_mapped"].mean(),
        "unit_coverage": events["unit_present"].mean(),
        "lineage_completeness_rate": events["lineage_complete"].mean(),
        "protocol_error_rate": events["protocol_error"].mean(),
    }]).round(4)

    overall.to_csv(output_dir / "python_protocol_quality_overall.csv", index=False)
    print(overall.to_string(index=False))


if __name__ == "__main__":
    run()
