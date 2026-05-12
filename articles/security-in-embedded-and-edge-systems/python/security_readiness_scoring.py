"""
Python Workflow: Embedded Security Readiness and Risk Scoring

This workflow calculates an embedded/edge security-readiness score:

S_edge = wh*H + wb*B + wi*I + wu*U + wr*R + wm*M - we*E - wd*D
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd


@dataclass(frozen=True)
class SecurityWeights:
    hardware_trust: float = 0.16
    boot_integrity: float = 0.16
    identity_strength: float = 0.15
    update_readiness: float = 0.14
    runtime_isolation: float = 0.14
    monitoring_maturity: float = 0.13
    exposure: float = 0.16
    lifecycle_drift: float = 0.14


def calculate_score(row: pd.Series, weights: SecurityWeights) -> float:
    positive = (
        weights.hardware_trust * row["hardware_trust"]
        + weights.boot_integrity * row["boot_integrity"]
        + weights.identity_strength * row["identity_strength"]
        + weights.update_readiness * row["update_readiness"]
        + weights.runtime_isolation * row["runtime_isolation"]
        + weights.monitoring_maturity * row["monitoring_maturity"]
    )

    penalty = (
        weights.exposure * row["exposure"]
        + weights.lifecycle_drift * row["lifecycle_drift"]
    )

    return round(max(0.0, min(1.0, positive - penalty)), 3)


def classify_risk(score: float, support_state: str, secure_boot: bool) -> str:
    if support_state == "end-of-support":
        return "critical"
    if not secure_boot:
        return "critical"
    if score < 0.45:
        return "critical"
    if score < 0.60:
        return "high"
    if score < 0.75:
        return "moderate"
    return "managed"


def recommend_action(row: pd.Series) -> str:
    if row["risk_band"] == "critical":
        return "quarantine or retire device; require security review"
    if row["support_state"] == "limited-support":
        return "plan replacement or add compensating controls"
    if not row["rollback_ready"]:
        return "remediate rollback and recovery readiness before broad rollout"
    if row["risk_band"] == "high":
        return "reduce exposure and improve monitoring"
    return "approved with continuous monitoring"


def summarize_by_site(scored: pd.DataFrame) -> pd.DataFrame:
    return (
        scored.groupby(["site", "device_class", "support_state"], as_index=False)
        .agg(
            devices=("device_id", "count"),
            mean_security_readiness=("security_readiness_score", "mean"),
            critical_devices=("risk_band", lambda s: int((s == "critical").sum())),
            high_risk_devices=("risk_band", lambda s: int((s == "high").sum())),
            exposed_devices=("exposure", lambda s: int((s >= 0.70).sum())),
        )
        .round({"mean_security_readiness": 3})
        .sort_values(["critical_devices", "high_risk_devices", "mean_security_readiness"], ascending=[False, False, True])
    )


def run_workflow(data_path: Path, output_dir: Path) -> Dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    assets = pd.read_csv(data_path)
    weights = SecurityWeights()

    scored = assets.copy()
    scored["security_readiness_score"] = scored.apply(calculate_score, axis=1, weights=weights)
    scored["risk_band"] = scored.apply(
        lambda row: classify_risk(row["security_readiness_score"], row["support_state"], bool(row["secure_boot"])),
        axis=1,
    )
    scored["recommended_action"] = scored.apply(recommend_action, axis=1)

    summary = summarize_by_site(scored)

    scored_path = output_dir / "security_readiness_scores.csv"
    summary_path = output_dir / "security_posture_summary.csv"

    scored.to_csv(scored_path, index=False)
    summary.to_csv(summary_path, index=False)

    return {"scored_assets": scored_path, "summary": summary_path}


if __name__ == "__main__":
    article_root = Path(__file__).resolve().parents[1]
    outputs = run_workflow(
        data_path=article_root / "data" / "sample_security_assets.csv",
        output_dir=article_root / "outputs",
    )

    print("Generated security outputs:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")
