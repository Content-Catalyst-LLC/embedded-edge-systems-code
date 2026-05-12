from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)
    controls = yaml.safe_load((root / "config/trust_boundary_manifest.yml").read_text())["trust_boundary_manifest"]["required_controls"]
    controls_df = pd.DataFrame([{"control": k, "declared": bool(v)} for k, v in controls.items()])
    controls_df.to_csv(out / "python_trust_boundary_controls.csv", index=False)
    fleet = pd.read_csv(root / "data/sample_edge_fleet_inventory.csv")
    fleet["trust_problem"] = fleet["trust_state"] != "verified"
    fleet["authority_should_be_restricted"] = fleet["trust_state"].isin(["unknown", "unverified"])
    summary = pd.DataFrame([{
        "control_declaration_rate": controls_df["declared"].mean(),
        "trust_verified_rate": (fleet["trust_state"] == "verified").mean(),
        "trust_problem_rate": fleet["trust_problem"].mean(),
        "authority_restriction_rate": fleet["authority_should_be_restricted"].mean()
    }]).round(4)
    summary.to_csv(out / "python_trust_boundary_security_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
