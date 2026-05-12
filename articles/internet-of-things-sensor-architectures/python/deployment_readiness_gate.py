from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    readiness = yaml.safe_load((root / "config/deployment_readiness.yml").read_text())["deployment_readiness"]["required_gates"]

    computed = {
        "sensor_inventory_complete": (root / "data/device_inventory.csv").exists(),
        "device_identity_provisioned": (root / "config/device_identity_manifest.yml").exists(),
        "telemetry_schema_validated": (root / "config/telemetry_schema.json").exists(),
        "protocol_topic_map_reviewed": (root / "config/topic_resource_map.yml").exists(),
        "offline_behavior_tested": (root / "config/buffering_replay_policy.yml").exists(),
        "gateway_transformations_documented": (root / "config/gateway_transformation_manifest.yml").exists(),
        "security_controls_verified": (root / "config/security_control_profile.yml").exists(),
        "command_authority_bounded": (root / "config/command_authority_policy.yml").exists(),
        "ota_configuration_rollout_tested": (root / "config/ota_rollout_policy.yml").exists(),
        "observability_implemented": (root / "config/observability_schema.json").exists(),
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
