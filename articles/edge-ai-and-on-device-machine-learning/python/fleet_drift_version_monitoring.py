"""
Python Workflow: Fleet Drift, Version-Skew, and Monitoring Analysis

This script summarizes drift proxies, confidence distributions, fallback rates,
latency behavior, backend deltas, and model-version skew across device classes.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    events_path = output_dir / "python_edge_ai_inference_events.csv"
    events = pd.read_csv(events_path) if events_path.exists() else pd.read_csv(article_root / "data" / "sample_inference_events.csv")
    inventory = pd.read_csv(article_root / "data" / "model_inventory.csv")
    monitoring = yaml.safe_load((article_root / "config" / "fleet_monitoring_plan.yml").read_text(encoding="utf-8"))["fleet_monitoring_plan"]

    summary = (
        events.groupby(["device_class", "runtime_backend"])
        .agg(
            events=("device_id", "count"),
            mean_latency_ms=("latency_ms", "mean"),
            p95_latency_ms=("latency_ms", lambda s: s.quantile(0.95)),
            mean_confidence=("confidence", "mean"),
            low_confidence_rate=("confidence", lambda s: (s < events.loc[s.index, "confidence_threshold"]).mean()),
            fallback_rate=("fallback_used", "mean"),
            model_skew_rate=("model_version", lambda s: (s != events.loc[s.index, "approved_model_version"]).mean()),
            mean_drift_proxy=("drift_proxy", "mean"),
            backend_delta_p95=("backend_output_delta", lambda s: s.quantile(0.95)),
            latency_violation_rate=("latency_ok", lambda s: (~s).mean()),
            memory_violation_rate=("memory_ok", lambda s: (~s).mean()),
        )
        .reset_index()
        .round(4)
    )

    version_summary = pd.DataFrame([{
        "fleet_devices": len(inventory),
        "deployed_version_skew_rate": (inventory["deployed_model_version"] != inventory["approved_model_version"]).mean(),
        "active_version_skew_rate": (inventory["active_model_version"] != inventory["approved_model_version"]).mean(),
        "decision_used_version_skew_rate": (inventory["decision_used_model_version"] != inventory["approved_model_version"]).mean(),
        "rollback_ready_rate": inventory["rollback_ready"].mean(),
        "fallback_alert_threshold": monitoring["alert_thresholds"]["fallback_rate"],
        "backend_delta_p95_threshold": monitoring["alert_thresholds"]["backend_delta_p95"],
    }]).round(4)

    summary.to_csv(output_dir / "python_fleet_drift_monitoring_summary.csv", index=False)
    version_summary.to_csv(output_dir / "python_model_version_skew_summary.csv", index=False)

    print(summary.to_string(index=False))
    print(version_summary.to_string(index=False))


if __name__ == "__main__":
    run()
