from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)
    readiness = yaml.safe_load((root / "config/deployment_readiness.yml").read_text())["deployment_readiness"]["required_gates"]
    fleet = pd.read_csv(root / "data/sample_edge_fleet_inventory.csv")
    placement = pd.read_csv(root / "data/workload_placement_matrix.csv")
    computed = {
        "topology_manifest_complete": (root / "config/edge_topology_manifest.yml").exists(),
        "workload_placement_justified": placement["preferred_layer"].notna().all(),
        "latency_budget_passed": (fleet["latency_ms"] <= fleet["latency_budget_ms"]).mean() >= 0.70,
        "offline_mode_tested": (root / "config/offline_mode_policy.yml").exists(),
        "runtime_assurance_tested": (root / "config/runtime_assurance_policy.yml").exists(),
        "selective_uplink_tested": (root / "config/data_locality_policy.yml").exists(),
        "security_posture_verified": (fleet["trust_state"] == "verified").mean() >= 0.70,
        "fleet_inventory_deployed": len(fleet) > 0,
        "rollback_path_ready": fleet["rollback_ready"].mean() >= 0.70,
        "observability_schema_deployed": (root / "config/edge_telemetry_schema.json").exists(),
        "incident_reconstruction_ready": (root / "config/incident_reconstruction_policy.yml").exists()
    }
    results = pd.DataFrame([{"check_name": k, "required": bool(v), "passed": bool(computed.get(k, False))} for k, v in readiness.items()])
    results["gate_passed"] = (~results["required"]) | results["passed"]
    results.to_csv(out / "python_deployment_readiness_gate.csv", index=False)
    summary = pd.DataFrame([{"checks": len(results), "passed_checks": int(results["gate_passed"].sum()), "readiness_pass_rate": results["gate_passed"].mean(), "deployment_ready": bool(results["gate_passed"].all())}]).round(4)
    summary.to_csv(out / "python_deployment_readiness_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
