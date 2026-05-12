from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    cfg = yaml.safe_load((root / "config/drift_monitoring_policy.yml").read_text())["drift_monitoring_policy"]
    measurements = pd.read_csv(root / "data/sample_measurement_records.csv")
    measurements["raw_value"] = measurements["adc_counts"] * measurements["reference_voltage"] / (2 ** measurements["adc_bits"])
    measurements["calibrated_value"] = measurements["gain_coefficient"] * measurements["raw_value"] + measurements["offset_coefficient"]
    measurements["drift"] = measurements["calibrated_value"] - measurements["reference_value"]
    measurements["drift_warning"] = measurements["drift"].abs() > cfg["drift_threshold_absolute"]
    measurements["recalibration_required"] = measurements["drift_warning"] | measurements["calibration_expired"] | measurements["coefficient_mismatch"]

    measurements.to_csv(out / "python_drift_recalibration_monitoring.csv", index=False)

    summary = pd.DataFrame([{
        "measurements": len(measurements),
        "drift_warning_rate": measurements["drift_warning"].mean(),
        "recalibration_required_rate": measurements["recalibration_required"].mean(),
        "mean_absolute_drift": measurements["drift"].abs().mean()
    }]).round(4)
    summary.to_csv(out / "python_drift_recalibration_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
