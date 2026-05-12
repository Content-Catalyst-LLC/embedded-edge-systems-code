"""
Python Workflow: Gateway SLO and Capacity-Budget Checks

This script checks gateway event and site-state data against gateway SLOs for
freshness, buffer backlog, replay lag, protocol errors, lineage completeness,
site quality, missing children, stale devices, and duplicate replay.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    slo = yaml.safe_load((article_root / "config" / "gateway_slo.yml").read_text(encoding="utf-8"))["gateway_slo"]

    events_path = output_dir / "python_gateway_events.csv"
    site_state_path = output_dir / "python_site_state_events.csv"

    events = pd.read_csv(events_path) if events_path.exists() else pd.read_csv(article_root / "data" / "sample_gateway_events.csv")
    site_state = pd.read_csv(site_state_path) if site_state_path.exists() else pd.read_csv(article_root / "data" / "site_state_events.csv")
    replay = pd.read_csv(article_root / "data" / "replay_events.csv")

    checks = pd.DataFrame([{
        "child_device_freshness_rate": (events["child_device_status"] == "active").mean(),
        "max_buffer_backlog": events["buffer_backlog"].max(),
        "max_replay_lag_s": events["replay_lag_s"].max(),
        "protocol_error_rate": events["protocol_error"].mean(),
        "lineage_completeness_rate": events["lineage_complete"].mean(),
        "mean_site_quality_score": site_state["site_quality_score"].mean(),
        "duplicate_replay_rate": replay["duplicate_detected"].mean(),
        "missing_child_rate": (events["child_device_status"] == "missing").mean(),
        "stale_device_rate": (events["quality_flag"] == "stale").mean(),
    }]).round(4)

    checks["freshness_within_slo"] = checks["child_device_freshness_rate"] >= slo["child_device_freshness_target"]
    checks["buffer_backlog_within_slo"] = checks["max_buffer_backlog"] <= slo["max_buffer_backlog_events"]
    checks["replay_lag_within_slo"] = checks["max_replay_lag_s"] <= slo["max_replay_lag_s"]
    checks["protocol_error_within_slo"] = checks["protocol_error_rate"] <= slo["max_protocol_error_rate"]
    checks["lineage_within_slo"] = checks["lineage_completeness_rate"] >= slo["min_lineage_completeness_rate"]
    checks["site_quality_within_slo"] = checks["mean_site_quality_score"] >= slo["min_site_quality_score"]
    checks["duplicate_replay_within_slo"] = checks["duplicate_replay_rate"] <= slo["max_duplicate_replay_rate"]
    checks["missing_child_within_slo"] = checks["missing_child_rate"] <= slo["max_missing_child_rate"]
    checks["stale_device_within_slo"] = checks["stale_device_rate"] <= slo["max_stale_device_rate"]

    checks.to_csv(output_dir / "python_gateway_slo_checks.csv", index=False)
    print(checks.to_string(index=False))


if __name__ == "__main__":
    run()
