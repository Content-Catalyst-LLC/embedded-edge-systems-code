"""
Python Workflow: Edge Stream Analytics, Windowing, and Selective Uplink Simulation

This script simulates local stream windows, feature extraction, event logic,
buffering, freshness, compression, and selective uplink behavior.
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


def classify_event(signal_family: str, rms: float, peak: float, missing_rate: float, feature_complete: bool) -> str:
    if not feature_complete or missing_rate > 0.05:
        return "degraded"
    if signal_family == "vibration" and rms > 0.65 and peak > 0.80:
        return "fault"
    if signal_family == "vibration" and (rms > 0.45 or peak > 0.75):
        return "warning"
    if signal_family == "environmental" and peak > 5.0:
        return "warning"
    return "normal"


def route_event(state: str, connected: bool, buffer_backlog: int) -> str:
    if state in {"fault", "warning", "degraded"} and connected:
        return "immediate"
    if state in {"fault", "warning", "degraded"} and not connected:
        return "deferred"
    if buffer_backlog > 250:
        return "suppressed"
    return "sampled"


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(42)
    window_policy = load_yaml(article_root / "config" / "window_policy.yml")["window_policy"]
    slo = load_yaml(article_root / "config" / "analytics_slo.yml")["analytics_slo"]

    signal_families = ["vibration", "temperature", "power", "environmental"]
    rows = []
    buffer_backlog_by_gateway = {"gw-001": 0, "gw-002": 0, "gw-003": 0}

    for minute in range(180):
        site_id = rng.choice(["site-a", "site-b", "site-c"])
        gateway_id = {"site-a": "gw-001", "site-b": "gw-002", "site-c": "gw-003"}[site_id]
        signal_family = rng.choice(signal_families)
        signal_id = f"{signal_family}-main"
        sensor_id = f"{signal_family[:4]}-{rng.randint(1, 3):03d}"
        window_id = f"win-{minute:04d}"

        connected = rng.random() > 0.10
        arrivals = rng.randint(1, 5)
        service = rng.randint(0, 6) if connected else 0
        buffer_backlog_by_gateway[gateway_id] = max(0, min(500, buffer_backlog_by_gateway[gateway_id] + arrivals - service))
        buffer_backlog = buffer_backlog_by_gateway[gateway_id]

        expected_samples = 512 if signal_family == "vibration" else 60
        missing_sample_rate = max(0.0, min(0.25, abs(rng.gauss(0.02, 0.04))))
        feature_complete = missing_sample_rate <= 0.05
        rms = abs(rng.gauss(0.35, 0.25)) if signal_family == "vibration" else 0.0
        peak = abs(rng.gauss(0.70, 0.30)) if signal_family == "vibration" else abs(rng.gauss(4.0, 1.0))
        event_state = classify_event(signal_family, rms, peak, missing_sample_rate, feature_complete)
        event_detected = event_state != "normal"

        uplink_mode = route_event(event_state, connected, buffer_backlog)
        raw_bytes = expected_samples * 8
        uplink_bytes = 512 if event_detected else 128
        if uplink_mode == "suppressed":
            uplink_bytes = 0

        local_latency_ms = abs(rng.gauss(35, 25))
        if not connected:
            local_latency_ms += rng.uniform(5, 30)

        freshness_s = rng.uniform(1, 90)
        if uplink_mode in {"deferred", "suppressed"}:
            freshness_s += rng.uniform(60, 400)

        replay_lag_s = freshness_s if uplink_mode in {"deferred", "suppressed"} else rng.uniform(1, 10)
        lineage_complete = feature_complete and rng.random() > 0.02
        drop_reason = "none"
        if uplink_mode == "suppressed":
            drop_reason = "buffer_pressure_or_policy_suppression"
        quality_flag = "valid" if feature_complete and freshness_s <= slo["max_replay_lag_s"] else "stale_or_incomplete"

        rows.append({
            "event_id": f"evt-{uuid.uuid4().hex[:10]}",
            "timestamp": f"2026-03-28T12:{minute % 60:02d}:00Z",
            "site_id": site_id,
            "gateway_id": gateway_id,
            "signal_id": signal_id,
            "sensor_id": sensor_id,
            "signal_family": signal_family,
            "feature_version": "features-1.0",
            "rule_version": "rules-1.0",
            "window_id": window_id,
            "window_start": f"2026-03-28T12:{minute % 60:02d}:00Z",
            "window_end": f"2026-03-28T12:{minute % 60:02d}:02Z",
            "acquisition_time": f"2026-03-28T12:{minute % 60:02d}:00Z",
            "processing_time": f"2026-03-28T12:{minute % 60:02d}:01Z",
            "buffer_entry_time": f"2026-03-28T12:{minute % 60:02d}:01Z",
            "upload_time": f"2026-03-28T12:{minute % 60:02d}:02Z" if uplink_mode in {"immediate", "sampled"} else "",
            "upstream_ingest_time": f"2026-03-28T12:{minute % 60:02d}:03Z" if uplink_mode in {"immediate", "sampled"} else "",
            "raw_bytes": raw_bytes,
            "uplink_bytes": uplink_bytes,
            "local_latency_ms": round(local_latency_ms, 3),
            "freshness_s": round(freshness_s, 3),
            "freshness_threshold_s": 60 if signal_family != "environmental" else 120,
            "missing_sample_rate": round(missing_sample_rate, 4),
            "feature_complete": feature_complete,
            "event_detected": event_detected,
            "event_state": event_state,
            "uplink_mode": uplink_mode,
            "buffer_backlog": buffer_backlog,
            "replay_lag_s": round(replay_lag_s, 3),
            "lineage_complete": lineage_complete,
            "drop_reason": drop_reason,
            "quality_flag": quality_flag,
            "idempotency_key": f"{gateway_id}-{window_id}-{event_state}",
            "replay_batch_id": f"batch-{minute // 20:03d}",
        })

    events = pd.DataFrame(rows)
    events.to_csv(output_dir / "python_edge_analytics_events.csv", index=False)

    summary = pd.DataFrame([{
        "events": len(events),
        "sites": events["site_id"].nunique(),
        "gateways": events["gateway_id"].nunique(),
        "event_rate": events["event_detected"].mean(),
        "immediate_uplink_rate": (events["uplink_mode"] == "immediate").mean(),
        "deferred_uplink_rate": (events["uplink_mode"] == "deferred").mean(),
        "suppressed_rate": (events["uplink_mode"] == "suppressed").mean(),
        "mean_local_latency_ms": events["local_latency_ms"].mean(),
        "p95_local_latency_ms": events["local_latency_ms"].quantile(0.95),
        "stale_output_rate": (events["freshness_s"] > events["freshness_threshold_s"]).mean(),
        "feature_completeness_rate": events["feature_complete"].mean(),
        "lineage_completeness_rate": events["lineage_complete"].mean(),
        "mean_compression_ratio": (1 - events["uplink_bytes"].sum() / events["raw_bytes"].sum()),
        "max_buffer_backlog": events["buffer_backlog"].max(),
        "p95_replay_lag_s": events["replay_lag_s"].quantile(0.95),
    }]).round(4)

    summary.to_csv(output_dir / "python_edge_stream_analytics_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
