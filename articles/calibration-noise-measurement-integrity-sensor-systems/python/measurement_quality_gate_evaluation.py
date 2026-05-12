from pathlib import Path
import ast
import pandas as pd
import yaml

def normalize_flags(value):
    if isinstance(value, list):
        return value
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, list):
            return parsed
    except Exception:
        pass
    return [str(value)]

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    analysis_path = out / "python_measurement_integrity_analysis.csv"
    if not analysis_path.exists():
        raise SystemExit("Run sensor_calibration_noise_integrity_analysis.py first.")

    gate_policy = yaml.safe_load((root / "config/quality_gate_policy.yml").read_text())["quality_gate_policy"]["allowed_uses"]
    df = pd.read_csv(analysis_path)
    df["quality_flags_list"] = df["quality_flags"].apply(normalize_flags)

    def allowed_uses(flags):
        uses = set()
        for flag in flags:
            for use in gate_policy.get(flag, []):
                uses.add(use)
        return ",".join(sorted(uses))

    df["allowed_uses"] = df["quality_flags_list"].apply(allowed_uses)
    df["blocked_from_high_consequence_use"] = ~df["allowed_uses"].str.contains("control", na=False)
    df["restricted_from_model_features"] = df["quality_flags_list"].apply(
        lambda flags: any(flag in flags for flag in ["low_snr", "calibration_expired", "coefficient_mismatch", "lineage_incomplete", "traceability_incomplete"])
    )

    df.to_csv(out / "python_measurement_quality_gate_evaluation.csv", index=False)

    summary = pd.DataFrame([{
        "measurements": len(df),
        "blocked_from_high_consequence_use_rate": df["blocked_from_high_consequence_use"].mean(),
        "restricted_from_model_features_rate": df["restricted_from_model_features"].mean()
    }]).round(4)
    summary.to_csv(out / "python_measurement_quality_gate_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
