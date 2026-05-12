"""
Python Workflow: OTA Fleet Readiness and Rollout Risk Scoring

This script scores embedded and edge devices for OTA readiness:

S_OTA = wi*I + wc*C + wp*P + wv*V + wr*R + wo*O - wd*D

Where:
I = identity assurance
C = compatibility match
P = package integrity
V = validation status
R = rollback readiness
O = observability
D = lifecycle drift
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd


@dataclass(frozen=True)
class OTAWeights:
    identity_assurance: float = 0.16
    compatibility_match: float = 0.18
    package_integrity: float = 0.16
    validation_status: float = 0.16
    rollback_readiness: float = 0.16
    observability: float = 0.13
    lifecycle_drift: float = 0.15


def readiness_score(row: pd.Series, weights: OTAWeights) -> float:
    """Calculate OTA readiness score for one device."""
    positive = (
        weights.identity_assurance * row["identity_assurance"]
        + weights.compatibility_match * row["compatibility_match"]
        + weights.package_integrity * row["package_integrity"]
        + weights.validation_status * row["validation_status"]
        + weights.rollback_readiness * row["rollback_readiness"]
        + weights.observability * row["observability"]
    )
    penalty = weights.lifecycle_drift * row["lifecycle_drift"]
    return round(max(0.0, min(1.0, positive - penalty)), 3)


def rollout_decision(row: pd.Series) -> str:
    """Classify rollout decision using support state and OTA readiness."""
    if row["support_state"] == "end-of-support":
        return "block"
    if row["rollback_readiness"] < 0.50:
        return "hold-for-recovery-review"
    if row["ota_readiness_score"] >= 0.82:
        return "approve"
    if row["ota_readiness_score"] >= 0.70:
        return "canary-only"
    return "hold"


def summarize_by_ring(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize OTA readiness by rollout ring."""
    return (
        scored.groupby("rollout_ring", as_index=False)
        .agg(
            devices=("device_id", "count"),
            mean_ota_readiness=("ota_readiness_score", "mean"),
            blocked=("rollout_decision", lambda s: int((s == "block").sum())),
            held=("rollout_decision", lambda s: int(s.isin(["hold", "hold-for-recovery-review"]).sum())),
            approved=("rollout_decision", lambda s: int((s == "approve").sum())),
        )
        .round({"mean_ota_readiness": 3})
        .sort_values(["blocked", "held", "mean_ota_readiness"], ascending=[False, False, True])
    )


def run_workflow(data_path: Path, output_dir: Path) -> Dict[str, Path]:
    """Run OTA readiness scoring and reporting."""
    output_dir.mkdir(parents=True, exist_ok=True)

    devices = pd.read_csv(data_path)
    weights = OTAWeights()

    scored = devices.copy()
    scored["ota_readiness_score"] = scored.apply(readiness_score, axis=1, weights=weights)
    scored["rollout_decision"] = scored.apply(rollout_decision, axis=1)

    ring_summary = summarize_by_ring(scored)

    scored_path = output_dir / "ota_readiness_scores.csv"
    summary_path = output_dir / "rollout_ring_summary.csv"

    scored.to_csv(scored_path, index=False)
    ring_summary.to_csv(summary_path, index=False)

    return {
        "ota_readiness_scores": scored_path,
        "rollout_ring_summary": summary_path,
    }


if __name__ == "__main__":
    article_root = Path(__file__).resolve().parents[1]
    outputs = run_workflow(
        data_path=article_root / "data" / "sample_device_fleet.csv",
        output_dir=article_root / "outputs",
    )

    print("Generated OTA readiness outputs:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")
