from pathlib import Path
import math
import pandas as pd
import yaml

def snr_db(signal_rms, noise_rms):
    if noise_rms <= 0:
        return float("inf")
    return 20 * math.log10(signal_rms / noise_rms)

def quality_flags(row, cfg):
    flags = []
    minimum_snr_db = cfg["noise_budget_policy"]["minimum_snr_db"]
    drift_threshold = cfg["drift_monitoring_policy"]["drift_threshold_absolute"]

    if row["calibration_expired"]:
        flags.append("calibration_expired")
    if row["coefficient_mismatch"]:
        flags.append("coefficient_mismatch")
    if row["stale"]:
        flags.append("stale")
    if row["saturated"]:
        flags.append("saturated")
    if row["clipped"]:
        flags.append("clipped")
    if row["snr_db"] < minimum_snr_db:
        flags.append("low_snr")
    if abs(row["calibrated_value"] - row["reference_value"]) > drift_threshold:
        flags.append("drift_warning")
    if row["calibrated_value"] < row["valid_min"] or row["calibrated_value"] > row["valid_max"]:
        flags.append("out_of_range")
    if not row["lineage_complete"]:
        flags.append("lineage_incomplete")
    if not row["traceability_complete"]:
        flags.append("traceability_incomplete")

    return flags or ["valid"]

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    noise_cfg = yaml.safe_load((root / "config/noise_budget_policy.yml").read_text())
    drift_cfg = yaml.safe_load((root / "config/drift_monitoring_policy.yml").read_text())
    cfg = {**noise_cfg, **drift_cfg}

    measurements = pd.read_csv(root / "data/sample_measurement_records.csv")
    inventory = pd.read_csv(root / "data/sensor_inventory.csv")
    df = measurements.merge(inventory[["sensor_id", "valid_min", "valid_max", "unit", "filter_version"]], on="sensor_id", how="left")

    df["raw_value"] = df["adc_counts"] * df["reference_voltage"] / (2 ** df["adc_bits"])
    df["calibrated_value"] = df["gain_coefficient"] * df["raw_value"] + df["offset_coefficient"]
    uncertainty_cols = [
        "sensor_uncertainty", "reference_uncertainty", "afe_uncertainty",
        "adc_uncertainty", "calibration_uncertainty", "environmental_uncertainty"
    ]
    df["combined_uncertainty"] = (df[uncertainty_cols] ** 2).sum(axis=1) ** 0.5
    df["expanded_uncertainty"] = 2.0 * df["combined_uncertainty"]
    df["snr_db"] = df.apply(lambda r: snr_db(r["signal_rms"], r["noise_rms"]), axis=1)
    df["quality_flags"] = df.apply(lambda r: quality_flags(r, cfg), axis=1)
    df["primary_quality_state"] = df["quality_flags"].apply(lambda flags: flags[0])
    df["measurement_confidence"] = (
        (~df["calibration_expired"]).astype(float) * 0.20
        + (df["snr_db"].clip(0, 40) / 40.0) * 0.20
        + (~df["stale"]).astype(float) * 0.15
        + (~df["saturated"]).astype(float) * 0.15
        + df["lineage_complete"].astype(float) * 0.15
        + df["traceability_complete"].astype(float) * 0.15
    ).round(4)

    df.to_csv(out / "python_measurement_integrity_analysis.csv", index=False)

    summary = pd.DataFrame([{
        "measurements": len(df),
        "valid_rate": (df["primary_quality_state"] == "valid").mean(),
        "low_snr_rate": df["quality_flags"].apply(lambda flags: "low_snr" in flags).mean(),
        "drift_warning_rate": df["quality_flags"].apply(lambda flags: "drift_warning" in flags).mean(),
        "calibration_expired_rate": df["quality_flags"].apply(lambda flags: "calibration_expired" in flags).mean(),
        "coefficient_mismatch_rate": df["quality_flags"].apply(lambda flags: "coefficient_mismatch" in flags).mean(),
        "lineage_completeness_rate": df["lineage_complete"].mean(),
        "traceability_completeness_rate": df["traceability_complete"].mean(),
        "mean_expanded_uncertainty": df["expanded_uncertainty"].mean(),
        "mean_measurement_confidence": df["measurement_confidence"].mean()
    }]).round(4)

    summary.to_csv(out / "python_measurement_integrity_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
