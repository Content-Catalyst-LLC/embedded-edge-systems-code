"""
Python Workflow: Gateway Buffering, Aggregation, and Selective Uplink Simulation

This script simulates a gateway with heterogeneous child devices, protocol
normalization, buffering, aggregation, selective uplink, and site-state quality.
"""

from __future__ import annotations

from pathlib import Path
import random
import uuid

import pandas as pd
import yaml


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def site_quality_score(missing_rate: float, stale_rate: float, protocol_error_rate: float, lineage_gap_rate: float, weights: dict) -> float:
    penalty = (
        weights["missing_devices"] * missing_rate
        + weights["stale_inputs"] * stale_rate
        + weights["protocol_errors"] * protocol_error_rate
        + weights["lineage_gaps"] * lineage_gap_rate
    )
    return max(0.0, min(1.0, 1.0 - penalty))


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(42)
    registry = pd.read_csv(article_root / "data" / "child_device_registry.csv")
    aggregation_contract = load_yaml(article_root / "config" / "aggregation_contract.yml")["aggregation_contract"]
    buffer_policy = load_yaml(article_root / "config" / "buffer_policy.yml")["buffer_policy"]
    forwarding_policy = load_yaml(article_root / "config" / "selective_forwarding_policy.yml")["selective_forwarding_policy"]

    rows = []
    site_rows = []
    buffer_backlog = {"gw-001": 0, "gw-002": 0, "gw-003": 0}

    for minute in range(120):
        for _, device in registry.iterrows():
            gateway_id = device["gateway_id"]
            cloud_reachable = rng.random() > 0.08
            arrival_rate = rng.randint(1, 5)
            service_rate = rng.randint(0, 6) if cloud_reachable else 0
            buffer_backlog[gateway_id] = min(
                buffer_policy["max_buffer_events"],
                max(0, buffer_backlog[gateway_id] + arrival_rate - service_rate),
            )

            expected_heartbeat = float(device["expected_heartbeat_s"])
            freshness = rng.uniform(0, expected_heartbeat * 1.5)
            if not cloud_reachable and rng.random() < 0.20:
                freshness += rng.uniform(120, 600)

            criticality = str(device["criticality"])
            threshold_key = f"{criticality}_criticality"
            freshness_threshold = float(aggregation_contract["freshness_thresholds_s"].get(threshold_key, 60))

            child_status = "active" if freshness <= freshness_threshold else "missing"
            protocol_error = rng.random() < {"i2c": 0.08, "spi": 0.04, "modbus": 0.06, "can": 0.05}.get(device["protocol_family"], 0.05)
            quality = "valid"
            if child_status == "missing":
                quality = "stale"
            if protocol_error:
                quality = "invalid"

            lineage_complete = not protocol_error and rng.random() > 0.01
            priority = "routine"
            if quality != "valid" or criticality == "high":
                priority = "incident" if quality == "invalid" else "diagnostic"

            forwarded = cloud_reachable and (
                priority in {"incident", "diagnostic"}
                or minute % int(forwarding_policy["defaults"]["routine_forwarding_interval_s"] / 60) == 0
            )

            event_time = f"2026-03-28T12:{minute:02d}:00Z"
            replay_lag = freshness if forwarded else freshness + buffer_backlog[gateway_id] * 0.5

            rows.append({
                "event_id": f"evt-{uuid.uuid4().hex[:10]}",
                "timestamp": event_time,
                "site_id": device["site_id"],
                "gateway_id": gateway_id,
                "device_id": device["device_id"],
                "protocol_family": device["protocol_family"],
                "local_acquisition_time": event_time,
                "gateway_receipt_time": event_time,
                "aggregation_time": event_time,
                "upload_time": event_time if forwarded else "",
                "upstream_ingest_time": event_time if forwarded else "",
                "measurement": round(rng.uniform(0, 100), 3),
                "unit": device["physical_unit"],
                "quality_flag": quality,
                "device_freshness_s": round(freshness, 3),
                "child_device_status": child_status,
                "protocol_error": protocol_error,
                "buffer_backlog": buffer_backlog[gateway_id],
                "replay_lag_s": round(replay_lag, 3),
                "forwarded_upstream": forwarded,
                "lineage_complete": lineage_complete,
                "selective_forwarding_reason": priority,
                "policy_version": "policy-1.0",
            })

    events = pd.DataFrame(rows)

    for (site_id, gateway_id), group in events.groupby(["site_id", "gateway_id"]):
        expected_devices = registry[(registry["site_id"] == site_id) & (registry["gateway_id"] == gateway_id)]["device_id"].nunique()
        contributing_devices = group[group["child_device_status"] == "active"]["device_id"].nunique()
        missing_child_count = max(0, expected_devices - contributing_devices)
        stale_device_count = int((group["quality_flag"] == "stale").sum())
        protocol_error_count = int(group["protocol_error"].sum())
        lineage_gap_count = int((~group["lineage_complete"]).sum())

        n = max(1, len(group))
        score = site_quality_score(
            missing_rate=missing_child_count / max(1, expected_devices),
            stale_rate=stale_device_count / n,
            protocol_error_rate=protocol_error_count / n,
            lineage_gap_rate=lineage_gap_count / n,
            weights=aggregation_contract["quality_score_weights"],
        )

        site_rows.append({
            "site_state_id": f"state-{site_id}-{gateway_id}",
            "timestamp": "2026-03-28T14:00:00Z",
            "site_id": site_id,
            "gateway_id": gateway_id,
            "aggregation_window_s": aggregation_contract["aggregation_window_s"],
            "contributing_devices": contributing_devices,
            "expected_devices": expected_devices,
            "missing_child_count": missing_child_count,
            "stale_device_count": stale_device_count,
            "protocol_error_count": protocol_error_count,
            "lineage_gap_count": lineage_gap_count,
            "site_quality_score": round(score, 4),
            "aggregation_confidence": round(score, 4),
            "forwarded_upstream": True,
        })

    site_state = pd.DataFrame(site_rows)

    events.to_csv(output_dir / "python_gateway_events.csv", index=False)
    site_state.to_csv(output_dir / "python_site_state_events.csv", index=False)

    summary = pd.DataFrame([{
        "events": len(events),
        "gateways": events["gateway_id"].nunique(),
        "child_devices": events["device_id"].nunique(),
        "protocol_error_rate": events["protocol_error"].mean(),
        "stale_or_missing_rate": (events["child_device_status"] == "missing").mean(),
        "mean_buffer_backlog": events["buffer_backlog"].mean(),
        "max_buffer_backlog": events["buffer_backlog"].max(),
        "mean_replay_lag_s": events["replay_lag_s"].mean(),
        "lineage_completeness_rate": events["lineage_complete"].mean(),
        "selective_uplink_rate": events["forwarded_upstream"].mean(),
        "mean_site_quality_score": site_state["site_quality_score"].mean(),
    }]).round(4)

    summary.to_csv(output_dir / "python_gateway_buffering_aggregation_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
