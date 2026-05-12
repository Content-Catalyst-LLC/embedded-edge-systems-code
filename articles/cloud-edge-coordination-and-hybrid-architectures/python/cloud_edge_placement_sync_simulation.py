"""
Python Workflow: Cloud-Edge Placement, Synchronization, and Degraded-Mode Simulation

This script simulates a small hybrid edge/cloud fleet with workload-placement scores,
cloud reachability, offline authority windows, buffered telemetry, state age, sync lag,
policy drift, model skew, and degraded-mode behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
import pandas as pd
import yaml


@dataclass(frozen=True)
class PlacementWeights:
    alpha_latency: float = 0.35
    beta_bandwidth: float = 0.20
    gamma_privacy: float = 0.20
    delta_compute: float = 0.10
    eta_governance: float = 0.15


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def placement_score(latency_ms: float, bandwidth_mb: float, privacy_risk: float, compute_cost: float, governance_burden: float, weights: PlacementWeights) -> float:
    return (
        weights.alpha_latency * latency_ms
        + weights.beta_bandwidth * bandwidth_mb
        + weights.gamma_privacy * privacy_risk
        + weights.delta_compute * compute_cost
        + weights.eta_governance * governance_burden
    )


def simulate(seed: int = 42) -> pd.DataFrame:
    rng = random.Random(seed)
    article_root = Path(__file__).resolve().parents[1]
    authority = load_yaml(article_root / "config" / "authority_policy.yml")["authority_policy"]
    default_authority_window_s = float(authority["default_authority_window_s"])

    sites = ["site-a", "site-b", "site-c", "site-d"]
    rows = []
    weights = PlacementWeights()

    for minute in range(180):
        for idx, site_id in enumerate(sites):
            gateway_id = f"gw-{idx + 1:03d}"
            device_id = f"dev-{idx + 1:03d}"

            cloud_reachable = rng.random() > (0.03 + 0.04 * idx)
            offline_duration_s = 0 if cloud_reachable else rng.choice([60, 120, 240, 520, 900])
            authority_valid = cloud_reachable or offline_duration_s <= default_authority_window_s

            state_age_s = rng.uniform(2, 12) if cloud_reachable else offline_duration_s + rng.uniform(2, 20)
            sync_lag_s = rng.uniform(1, 15) if cloud_reachable else offline_duration_s
            buffer_backlog = int(rng.uniform(0, 30)) if cloud_reachable else int(rng.uniform(80, 450))

            cloud_policy_version = "policy-1.1" if minute > 60 else "policy-1.0"
            edge_policy_version = cloud_policy_version
            if not cloud_reachable and minute > 60:
                edge_policy_version = "policy-1.0"

            approved_model_version = "model-2.1"
            edge_model_version = approved_model_version if rng.random() > 0.15 else "model-2.0"
            target_version = approved_model_version
            active_version = edge_model_version if rng.random() > 0.08 else "model-2.0"

            reconciliation_status = "none"
            if edge_policy_version != cloud_policy_version or edge_model_version != approved_model_version:
                reconciliation_status = rng.choice(["conflict", "merged", "hold_for_review"])

            degraded_mode = (not cloud_reachable and offline_duration_s > 120) or not authority_valid
            operating_mode = "degraded" if degraded_mode else "nominal"

            local_decision_count = 0 if cloud_reachable else int(offline_duration_s / 30)
            selective_uplink_rate = max(0.03, min(0.30, rng.uniform(0.05, 0.22)))

            placement_edge = placement_score(
                latency_ms=5,
                bandwidth_mb=2,
                privacy_risk=0.2,
                compute_cost=0.4,
                governance_burden=0.5,
                weights=weights,
            )
            placement_cloud = placement_score(
                latency_ms=90,
                bandwidth_mb=80,
                privacy_risk=0.7,
                compute_cost=0.2,
                governance_burden=0.2,
                weights=weights,
            )

            rows.append({
                "timestamp": f"2026-03-28T12:{minute:02d}:00Z",
                "site_id": site_id,
                "gateway_id": gateway_id,
                "device_id": device_id,
                "operating_mode": operating_mode,
                "cloud_reachable": cloud_reachable,
                "offline_duration_s": offline_duration_s,
                "state_age_s": state_age_s,
                "sync_lag_s": sync_lag_s,
                "buffer_backlog": buffer_backlog,
                "edge_policy_version": edge_policy_version,
                "cloud_policy_version": cloud_policy_version,
                "edge_model_version": edge_model_version,
                "approved_model_version": approved_model_version,
                "target_version": target_version,
                "active_version": active_version,
                "local_decision_count": local_decision_count,
                "reconciliation_status": reconciliation_status,
                "degraded_mode": degraded_mode,
                "authority_valid": authority_valid,
                "selective_uplink_rate": selective_uplink_rate,
                "rollout_ring": rng.choice(["canary", "pilot", "regional", "fleet"]),
                "edge_placement_score": placement_edge,
                "cloud_placement_score": placement_cloud,
                "recommended_placement": "edge" if placement_edge < cloud_placement else "cloud",
            })

    return pd.DataFrame(rows)


def summarize(events: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([{
        "events": len(events),
        "cloud_unreachable_rate": (~events["cloud_reachable"]).mean(),
        "degraded_mode_rate": events["degraded_mode"].mean(),
        "authority_violation_rate": (~events["authority_valid"]).mean(),
        "policy_drift_rate": (events["edge_policy_version"] != events["cloud_policy_version"]).mean(),
        "model_skew_rate": (events["edge_model_version"] != events["approved_model_version"]).mean(),
        "rollout_active_version_gap_rate": (events["active_version"] != events["target_version"]).mean(),
        "mean_state_age_s": events["state_age_s"].mean(),
        "max_sync_lag_s": events["sync_lag_s"].max(),
        "max_buffer_backlog": events["buffer_backlog"].max(),
        "reconciliation_conflict_rate": events["reconciliation_status"].isin(["conflict", "hold_for_review", "rollback_required"]).mean(),
    }]).round(4)


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    events = simulate()
    summary = summarize(events)

    events.to_csv(output_dir / "python_cloud_edge_hybrid_events.csv", index=False)
    summary.to_csv(output_dir / "python_cloud_edge_hybrid_summary.csv", index=False)

    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
