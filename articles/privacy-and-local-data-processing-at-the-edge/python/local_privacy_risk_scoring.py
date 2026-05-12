"""
Python Workflow: Local Data Minimisation and Privacy Risk Scoring

This workflow calculates a privacy-risk score for edge events and shows how
local minimisation, transformation, and ephemeral processing can reduce risk.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd


@dataclass(frozen=True)
class PrivacyWeights:
    raw_collection: float = 0.18
    identifiability: float = 0.22
    retention_hours: float = 0.12
    linkability: float = 0.18
    sharing_scope: float = 0.18
    minimisation: float = 0.16
    local_transformation: float = 0.18
    ephemeral_processing: float = 0.14


def normalize_retention(hours: float, cap: float = 168.0) -> float:
    """Normalize retention into a 0-1 risk range."""
    return max(0.0, min(1.0, hours / cap))


def classify_privacy_risk(score: float) -> str:
    """Convert a numeric privacy-risk score into a review band."""
    if score >= 0.70:
        return "high"
    if score >= 0.50:
        return "moderate"
    if score >= 0.30:
        return "managed"
    return "low"


def calculate_privacy_risk(row: pd.Series, weights: PrivacyWeights) -> float:
    """Calculate residual privacy risk after local controls."""
    exposure = (
        weights.raw_collection * row["raw_collection"]
        + weights.identifiability * row["identifiability"]
        + weights.retention_hours * normalize_retention(row["retention_hours"])
        + weights.linkability * row["linkability"]
        + weights.sharing_scope * row["sharing_scope"]
    )

    controls = (
        weights.minimisation * row["minimisation"]
        + weights.local_transformation * row["local_transformation"]
        + weights.ephemeral_processing * row["ephemeral_processing"]
    )

    return round(max(0.0, min(1.0, exposure - controls)), 3)


def recommend_action(row: pd.Series) -> str:
    """Recommend a governance action based on privacy risk and signal type."""
    if row["privacy_risk_band"] == "high":
        return "block upstream transfer and require privacy review"
    if row["signal_type"] in {"audio", "video", "physiological"} and row["retention_hours"] > 24:
        return "reduce retention and document purpose limitation"
    if row["privacy_risk_band"] == "moderate":
        return "strengthen minimisation or transformation"
    return "approved with monitoring"


def run_workflow(data_path: Path, output_dir: Path) -> Dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    events = pd.read_csv(data_path)
    weights = PrivacyWeights()

    scored = events.copy()
    scored["privacy_risk_score"] = scored.apply(calculate_privacy_risk, axis=1, weights=weights)
    scored["privacy_risk_band"] = scored["privacy_risk_score"].apply(classify_privacy_risk)
    scored["recommended_action"] = scored.apply(recommend_action, axis=1)

    summary = (
        scored.groupby(["site", "signal_type", "privacy_risk_band"], as_index=False)
        .agg(
            events=("event_id", "count"),
            mean_privacy_risk=("privacy_risk_score", "mean"),
            max_retention_hours=("retention_hours", "max"),
        )
        .round({"mean_privacy_risk": 3})
    )

    scored_path = output_dir / "edge_privacy_risk_scores.csv"
    summary_path = output_dir / "edge_privacy_summary.csv"

    scored.to_csv(scored_path, index=False)
    summary.to_csv(summary_path, index=False)

    return {"scored_events": scored_path, "summary": summary_path}


if __name__ == "__main__":
    article_root = Path(__file__).resolve().parents[1]
    outputs = run_workflow(
        data_path=article_root / "data" / "sample_edge_privacy_events.csv",
        output_dir=article_root / "outputs",
    )

    print("Generated privacy outputs:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")
