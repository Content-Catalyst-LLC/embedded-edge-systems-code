from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    readiness = yaml.safe_load((root / "config/deployment_readiness.yml").read_text())["deployment_readiness"]["required_gates"]

    computed = {
        "monitoring_objective_defined": (root / "config/monitoring_objective.yml").exists(),
        "topology_reviewed": (root / "config/topology_policy.yml").exists() and (root / "data/topology_zones.csv").exists(),
        "inference_boundaries_documented": (root / "docs/inference_boundaries.md").exists(),
        "node_inventory_complete": (root / "data/node_inventory.csv").exists(),
        "timing_policy_validated": (root / "config/timing_policy.yml").exists(),
        "transport_path_tested": (root / "config/transport_policy.yml").exists(),
        "buffering_and_replay_tested": (root / "config/buffering_replay_policy.yml").exists(),
        "quality_policy_implemented": (root / "config/quality_policy.yml").exists(),
        "fault_containment_implemented": (root / "config/fault_containment_policy.yml").exists(),
        "gateway_behavior_documented": (root / "config/gateway_manifest.yml").exists(),
        "aggregation_lineage_preserved": (root / "config/aggregation_manifest.yml").exists(),
        "monitoring_observability_implemented": (root / "config/monitoring_health_schema.json").exists(),
        "incident_reconstruction_ready": (root / "config/incident_reconstruction_policy.yml").exists()
    }

    results = pd.DataFrame([{"check_name": k, "required": bool(v), "passed": bool(computed.get(k, False))} for k, v in readiness.items()])
    results["gate_passed"] = (~results["required"]) | results["passed"]
    results.to_csv(out / "python_deployment_readiness_gate.csv", index=False)

    summary = pd.DataFrame([{
        "checks": len(results),
        "passed_checks": int(results["gate_passed"].sum()),
        "readiness_pass_rate": results["gate_passed"].mean(),
        "deployment_ready": bool(results["gate_passed"].all())
    }]).round(4)
    summary.to_csv(out / "python_deployment_readiness_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
