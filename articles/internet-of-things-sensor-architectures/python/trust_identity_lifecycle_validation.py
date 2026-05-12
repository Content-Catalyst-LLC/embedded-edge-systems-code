from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    identity_cfg = yaml.safe_load((root / "config/device_identity_manifest.yml").read_text())["device_identity_manifest"]
    fleet = pd.read_csv(root / "data/device_inventory.csv")
    gateways = pd.read_csv(root / "data/gateway_state.csv")

    required_fields = identity_cfg["required_identity_fields"]
    field_presence = {field: field in fleet.columns and fleet[field].notna().all() for field in required_fields}

    fleet["identity_complete"] = fleet[required_fields].notna().all(axis=1)
    fleet["trust_lifecycle_ok"] = (
        (fleet["trust_state"] == "verified")
        & (fleet["credential_state"] == "valid")
        & (fleet["lifecycle_state"] == "active")
    )
    fleet["version_state_ok"] = (
        (fleet["active_firmware"] == fleet["approved_firmware"])
        & (fleet["active_config"] == fleet["approved_config"])
        & (fleet["active_schema"] == fleet["approved_schema"])
    )
    gateways["gateway_trust_ok"] = gateways["trust_state"] == "verified"

    fleet.to_csv(out / "python_trust_identity_lifecycle_validation.csv", index=False)

    summary = pd.DataFrame([{
        "devices": len(fleet),
        "identity_complete_rate": fleet["identity_complete"].mean(),
        "trust_lifecycle_ok_rate": fleet["trust_lifecycle_ok"].mean(),
        "version_state_ok_rate": fleet["version_state_ok"].mean(),
        "gateway_trust_ok_rate": gateways["gateway_trust_ok"].mean(),
        "required_identity_fields_present": all(field_presence.values())
    }]).round(4)
    summary.to_csv(out / "python_trust_identity_lifecycle_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
