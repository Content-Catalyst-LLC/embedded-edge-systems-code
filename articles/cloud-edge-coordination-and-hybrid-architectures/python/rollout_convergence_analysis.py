"""
Python Workflow: Rollout Ring and Version-Convergence Analysis

This script distinguishes approved, target, deployed, active, and decision-used
versions across a hybrid edge fleet.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    nodes = pd.read_csv(article_root / "data" / "rollout_nodes.csv")

    with (article_root / "config" / "rollout_policy.yml").open("r", encoding="utf-8") as handle:
        rollout_policy = yaml.safe_load(handle)["rollout_policy"]

    eligible = nodes[nodes["eligible"] == True].copy()
    eligible["deployed_converged"] = eligible["deployed_version"] == eligible["target_version"]
    eligible["active_converged"] = eligible["active_version"] == eligible["target_version"]
    eligible["decision_used_converged"] = eligible["decision_used_version"] == eligible["target_version"]

    ring_summary = (
        eligible.groupby("rollout_ring")
        .agg(
            eligible_nodes=("node_id", "count"),
            deployed_convergence_rate=("deployed_converged", "mean"),
            active_convergence_rate=("active_converged", "mean"),
            decision_used_convergence_rate=("decision_used_converged", "mean"),
            unhealthy_nodes=("health_status", lambda s: int((s != "healthy").sum())),
            unreachable_nodes=("cloud_reachable", lambda s: int((~s).sum())),
        )
        .reset_index()
    )

    fleet_summary = pd.DataFrame([{
        "eligible_nodes": len(eligible),
        "deployed_convergence_rate": eligible["deployed_converged"].mean(),
        "active_convergence_rate": eligible["active_converged"].mean(),
        "decision_used_convergence_rate": eligible["decision_used_converged"].mean(),
        "min_required_convergence_rate": 0.95,
        "halt_conditions_defined": len(rollout_policy.get("halt_conditions", {})),
    }]).round(4)

    ring_summary.to_csv(output_dir / "python_rollout_ring_summary.csv", index=False)
    fleet_summary.to_csv(output_dir / "python_rollout_fleet_summary.csv", index=False)

    print(fleet_summary.to_string(index=False))


if __name__ == "__main__":
    run()
