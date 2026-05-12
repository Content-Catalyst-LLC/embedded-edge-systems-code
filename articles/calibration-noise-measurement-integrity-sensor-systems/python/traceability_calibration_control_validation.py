from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    trace_cfg = yaml.safe_load((root / "config/traceability_record.yml").read_text())["traceability_record"]
    inventory = pd.read_csv(root / "data/sensor_inventory.csv")
    measurements = pd.read_csv(root / "data/sample_measurement_records.csv")

    inventory["traceability_record_present"] = inventory["traceability_record_id"].notna()
    inventory["calibration_version_present"] = inventory["calibration_version"].notna()
    measurements["traceability_ok"] = measurements["traceability_complete"] == True
    measurements["lineage_ok"] = measurements["lineage_complete"] == True

    summary = pd.DataFrame([{
        "sensors": len(inventory),
        "sensor_traceability_record_present_rate": inventory["traceability_record_present"].mean(),
        "sensor_calibration_version_present_rate": inventory["calibration_version_present"].mean(),
        "measurement_traceability_complete_rate": measurements["traceability_ok"].mean(),
        "measurement_lineage_complete_rate": measurements["lineage_ok"].mean(),
        "meets_minimum_traceability_rate": measurements["traceability_ok"].mean() >= trace_cfg["minimum_traceability_complete_rate"]
    }])
    summary.to_csv(out / "python_traceability_calibration_control_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
