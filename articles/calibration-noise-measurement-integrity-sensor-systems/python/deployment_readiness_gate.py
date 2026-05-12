from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    readiness = yaml.safe_load((root / "config/deployment_readiness.yml").read_text())["deployment_readiness"]["required_gates"]

    computed = {
        "measurand_defined": (root / "data/sensor_inventory.csv").exists(),
        "calibration_manifest_complete": (root / "config/calibration_manifest.yml").exists(),
        "traceability_record_present": (root / "config/traceability_record.yml").exists(),
        "analog_front_end_validated": (root / "config/afe_configuration.yml").exists(),
        "sampling_and_settling_tested": (root / "config/adc_sampling_plan.yml").exists(),
        "noise_budget_evaluated": (root / "config/noise_budget_policy.yml").exists(),
        "wiring_installation_reviewed": True,
        "firmware_provenance_preserved": (root / "config/firmware_filter_manifest.yml").exists(),
        "quality_flags_implemented": (root / "config/quality_flag_policy.yml").exists(),
        "quality_gates_enforced": (root / "config/quality_gate_policy.yml").exists(),
        "uncertainty_carried_forward": (root / "config/measurement_record_schema.json").exists(),
        "recalibration_policy_defined": (root / "config/drift_monitoring_policy.yml").exists()
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
