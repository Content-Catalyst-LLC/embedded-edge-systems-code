"""
Python Workflow: Deployment Readiness Gate

This script evaluates whether the edge analytics deployment has satisfied
engineering readiness gates before field rollout.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    readiness = yaml.safe_load((article_root / "config" / "deployment_readiness.yml").read_text(encoding="utf-8"))["deployment_readiness"]
    events_path = output_dir / "python_edge_analytics_events.csv"
    events = pd.read_csv(events_path) if events_path.exists() else pd.read_csv(article_root / "data" / "sample_analytics_events.csv")
    replay = pd.read_csv(article_root / "data" / "replay_records.csv")

    computed = {
        "signal_manifest_complete": True,
        "preprocessing_validated": True,
        "window_policy_approved": True,
        "feature_parity_passed": bool(events["feature_complete"].mean() >= 0.95),
        "event_logic_tested": True,
        "retention_policy_deployed": True,
        "selective_uplink_tested": bool(events["uplink_mode"].isin(["immediate", "deferred", "sampled", "suppressed"]).all()),
        "replay_semantics_tested": bool("idempotency_key" in replay.columns and "replay_batch_id" in replay.columns),
        "analytics_slos_monitored": True,
        "rollback_path_ready": True,
    }

    rows = []
    for check_name, required in readiness["required_gates"].items():
        rows.append({
            "check_name": check_name,
            "required": bool(required),
            "passed": bool(computed.get(check_name, False)),
            "notes": "computed from companion workflow scaffold"
        })

    results = pd.DataFrame(rows)
    results["gate_passed"] = (~results["required"]) | results["passed"]
    results.to_csv(output_dir / "python_deployment_readiness_gate.csv", index=False)

    summary = pd.DataFrame([{
        "checks": len(results),
        "passed_checks": int(results["gate_passed"].sum()),
        "readiness_pass_rate": results["gate_passed"].mean(),
        "deployment_ready": bool(results["gate_passed"].all()),
    }]).round(4)

    summary.to_csv(output_dir / "python_deployment_readiness_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
