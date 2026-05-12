from pathlib import Path
import ast
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    policy = yaml.safe_load((root / "config/fault_containment_policy.yml").read_text())["fault_containment_policy"]
    telemetry_path = out / "python_telemetry_scored.csv"
    coverage_path = out / "python_coverage_scored.csv"
    if not telemetry_path.exists() or not coverage_path.exists():
        raise SystemExit("Run distributed_monitoring_health_coverage_analysis.py first.")

    telemetry = pd.read_csv(telemetry_path)
    coverage = pd.read_csv(coverage_path)

    def monitoring_state(row):
        if bool(row["usable"]):
            return "valid_fresh_synchronized"
        if not bool(row["fresh"]):
            return "stale"
        if not bool(row["synchronized"]):
            return "sync_degraded"
        if bool(row["duplicate_detected"]):
            return "gateway_replay"
        if row["quality_state"] == "low_confidence":
            return "low_confidence"
        if row["calibration_state"] == "drift_warning":
            return "node_drift_warning"
        return "low_confidence"

    telemetry["monitoring_state"] = telemetry.apply(monitoring_state, axis=1)
    telemetry["allowed_uses"] = telemetry["monitoring_state"].apply(
        lambda state: ",".join(policy["allowed_uses"].get(state, []))
    )
    telemetry["blocked_uses"] = telemetry["monitoring_state"].apply(
        lambda state: ",".join(policy["blocked_uses"].get(state, []))
    )
    telemetry["normal_monitoring_allowed"] = telemetry["allowed_uses"].str.contains("normal_monitoring", na=False)
    telemetry["historical_only"] = telemetry["allowed_uses"].str.contains("historical", na=False)

    coverage["system_claim_allowed"] = coverage["coverage_status"] == "observed_valid"
    coverage["inference_boundary"] = coverage["system_claim_allowed"].apply(
        lambda ok: "normal_zone_claim" if ok else "zone_claim_qualified"
    )

    telemetry.to_csv(out / "python_fault_containment_telemetry_evaluation.csv", index=False)
    coverage.to_csv(out / "python_inference_boundary_coverage_evaluation.csv", index=False)

    summary = pd.DataFrame([{
        "records": len(telemetry),
        "normal_monitoring_allowed_rate": telemetry["normal_monitoring_allowed"].mean(),
        "historical_only_rate": telemetry["historical_only"].mean(),
        "system_claim_allowed_zone_rate": coverage["system_claim_allowed"].mean(),
        "qualified_zone_claim_rate": (~coverage["system_claim_allowed"]).mean()
    }]).round(4)
    summary.to_csv(out / "python_fault_containment_inference_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
