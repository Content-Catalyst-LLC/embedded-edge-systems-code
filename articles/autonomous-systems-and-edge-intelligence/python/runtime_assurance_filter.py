"""
Python Workflow: Runtime Assurance and Safety-Filtered Action Selection

This module evaluates candidate autonomous actions against confidence, latency,
drift, authority, and safety constraints.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd
import yaml


def filter_action(
    candidate_action: str,
    belief_state: str,
    confidence: float,
    latency_ms: float,
    input_drift_score: float,
    autonomy_level: str,
    safety_state: str,
    assurance: dict,
    allowed_actions: List[str],
) -> Dict[str, object]:
    thresholds = assurance["thresholds"]
    fallbacks = assurance["fallbacks"]

    if candidate_action not in allowed_actions:
        return {
            "allowed": False,
            "filtered_action": fallbacks["authority_violation"],
            "reason_code": "authority_violation",
        }

    if safety_state == "degraded":
        return {
            "allowed": False,
            "filtered_action": fallbacks["degraded_safety_state"],
            "reason_code": "degraded_safety_state",
        }

    if latency_ms > thresholds["latency_budget_ms"]:
        return {
            "allowed": False,
            "filtered_action": fallbacks["excessive_latency"],
            "reason_code": "excessive_latency",
        }

    if input_drift_score >= thresholds["input_drift_fault"]:
        return {
            "allowed": False,
            "filtered_action": fallbacks["drift_fault"],
            "reason_code": "input_drift_fault",
        }

    if confidence < thresholds["minimum_confidence_for_any_motion"]:
        return {
            "allowed": False,
            "filtered_action": fallbacks["low_confidence"],
            "reason_code": "confidence_below_motion_threshold",
        }

    if confidence < thresholds["minimum_confidence_for_nominal_action"]:
        return {
            "allowed": False,
            "filtered_action": fallbacks["low_confidence"],
            "reason_code": "confidence_below_nominal_threshold",
        }

    if input_drift_score >= thresholds["input_drift_warning"] and candidate_action == "continue":
        return {
            "allowed": False,
            "filtered_action": fallbacks["drift_warning"],
            "reason_code": "input_drift_warning",
        }

    return {
        "allowed": True,
        "filtered_action": candidate_action,
        "reason_code": "allowed",
    }


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    events = pd.read_csv(article_root / "data" / "sample_autonomy_events.csv")
    with (article_root / "config" / "runtime_assurance.yml").open("r", encoding="utf-8") as handle:
        assurance = yaml.safe_load(handle)["runtime_assurance"]
    with (article_root / "config" / "autonomy_profile.yml").open("r", encoding="utf-8") as handle:
        profile = yaml.safe_load(handle)["autonomy_profile"]

    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for _, row in events.iterrows():
        result = filter_action(
            candidate_action=row["candidate_action"],
            belief_state=row["belief_state"],
            confidence=float(row["decision_confidence"]),
            latency_ms=float(row["latency_ms"]),
            input_drift_score=float(row["input_drift_score"]),
            autonomy_level=row["autonomy_level"],
            safety_state=row["safety_state"],
            assurance=assurance,
            allowed_actions=profile["allowed_actions"],
        )

        records.append({
            "timestamp": row["timestamp"],
            "device_id": row["device_id"],
            "candidate_action": row["candidate_action"],
            "logged_filtered_action": row["filtered_action"],
            "recomputed_filtered_action": result["filtered_action"],
            "allowed": result["allowed"],
            "reason_code": result["reason_code"],
        })

    out = pd.DataFrame(records)
    out.to_csv(output_dir / "python_runtime_assurance_records.csv", index=False)

    summary = pd.DataFrame([{
        "events": len(out),
        "allowed_events": int(out["allowed"].sum()),
        "filtered_or_rejected_events": int((~out["allowed"]).sum()),
        "filter_rate": float((~out["allowed"]).mean()),
    }]).round(4)

    summary.to_csv(output_dir / "python_runtime_assurance_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
