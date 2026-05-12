"""
Python Workflow: Interoperability Risk Scoring Across Edge Device Fleets

This script scores edge devices using a governance-capacity model:

G_edge = wp*P + ws*S + wl*L + wt*T + wo*O - wd*D

Where:
P = protocol conformance
S = semantic alignment
L = lifecycle control
T = trust/security baseline maturity
O = operational accountability
D = unmanaged divergence
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd


@dataclass(frozen=True)
class GovernanceWeights:
    protocol_conformance: float = 0.20
    semantic_alignment: float = 0.20
    lifecycle_control: float = 0.20
    security_baseline: float = 0.20
    operational_accountability: float = 0.15
    unmanaged_divergence: float = 0.15


def classify_risk(score: float, support_state: str) -> str:
    """Convert score and support state into an operational risk band."""
    if support_state == "end-of-support":
        return "critical"
    if score < 0.55:
        return "critical"
    if score < 0.70:
        return "high"
    if score < 0.82:
        return "moderate"
    return "low"


def calculate_governance_score(row: pd.Series, weights: GovernanceWeights) -> float:
    """Calculate governance capacity score for one edge asset."""
    positive = (
        weights.protocol_conformance * row["protocol_conformance"]
        + weights.semantic_alignment * row["semantic_alignment"]
        + weights.lifecycle_control * row["lifecycle_control"]
        + weights.security_baseline * row["security_baseline"]
        + weights.operational_accountability * row["operational_accountability"]
    )
    penalty = weights.unmanaged_divergence * row["unmanaged_divergence"]
    return round(max(0.0, min(1.0, positive - penalty)), 3)


def summarize_by_site(scored: pd.DataFrame) -> pd.DataFrame:
    """Create site-level interoperability governance summary."""
    return (
        scored.groupby("site", as_index=False)
        .agg(
            devices=("device_id", "count"),
            mean_governance_score=("governance_score", "mean"),
            critical_devices=("risk_band", lambda s: int((s == "critical").sum())),
            high_risk_devices=("risk_band", lambda s: int((s == "high").sum())),
            end_of_support_devices=("support_state", lambda s: int((s == "end-of-support").sum())),
        )
        .round({"mean_governance_score": 3})
        .sort_values(["critical_devices", "high_risk_devices", "mean_governance_score"], ascending=[False, False, True])
    )


def run_workflow(data_path: Path, output_dir: Path) -> Dict[str, Path]:
    """Run the complete scoring and reporting workflow."""
    output_dir.mkdir(parents=True, exist_ok=True)

    assets = pd.read_csv(data_path)
    weights = GovernanceWeights()

    scored = assets.copy()
    scored["governance_score"] = scored.apply(calculate_governance_score, axis=1, weights=weights)
    scored["risk_band"] = scored.apply(
        lambda row: classify_risk(row["governance_score"], row["support_state"]),
        axis=1,
    )

    site_summary = summarize_by_site(scored)

    scored_path = output_dir / "edge_governance_scores.csv"
    summary_path = output_dir / "site_governance_summary.csv"

    scored.to_csv(scored_path, index=False)
    site_summary.to_csv(summary_path, index=False)

    return {
        "scored_devices": scored_path,
        "site_summary": summary_path,
    }


if __name__ == "__main__":
    article_root = Path(__file__).resolve().parents[1]
    outputs = run_workflow(
        data_path=article_root / "data" / "sample_edge_assets.csv",
        output_dir=article_root / "outputs",
    )

    print("Generated governance outputs:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")
