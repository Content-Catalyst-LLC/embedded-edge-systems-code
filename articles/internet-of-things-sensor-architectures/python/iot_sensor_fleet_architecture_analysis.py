from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    freshness_threshold = yaml.safe_load((root / "config/buffering_replay_policy.yml").read_text())["buffering_replay_policy"]["freshness_threshold_seconds"]

    fleet = pd.read_csv(root / "data/device_inventory.csv")
    gateways = pd.read_csv(root / "data/gateway_state.csv")
    telemetry = pd.read_csv(root / "data/telemetry_records.csv", parse_dates=["event_time", "upload_time", "ingestion_time", "processing_time"])

    fleet["firmware_compliant"] = fleet["active_firmware"] == fleet["approved_firmware"]
    fleet["configuration_compliant"] = fleet["active_config"] == fleet["approved_config"]
    fleet["schema_compliant"] = fleet["active_schema"] == fleet["approved_schema"]
    fleet["trusted"] = fleet["trust_state"] == "verified"
    fleet["online"] = fleet["connectivity_state"] == "online"
    fleet["lifecycle_active"] = fleet["lifecycle_state"] == "active"
    fleet["credential_valid"] = fleet["credential_state"] == "valid"

    gateways["rule_compliant"] = gateways["active_rule_version"] == gateways["approved_rule_version"]
    gateways["firmware_compliant"] = gateways["firmware_version"] == gateways["approved_firmware"]
    gateways["buffer_pressure"] = gateways["buffer_depth"] / gateways["buffer_capacity"]
    gateways["child_reporting_rate"] = gateways["child_devices_reporting"] / gateways["child_device_count"]

    telemetry["freshness_seconds"] = (telemetry["processing_time"] - telemetry["event_time"]).dt.total_seconds()
    telemetry["fresh"] = telemetry["freshness_seconds"] <= freshness_threshold
    telemetry["firmware_compliant"] = telemetry["active_firmware"] == telemetry["approved_firmware"]
    telemetry["configuration_compliant"] = telemetry["active_config"] == telemetry["approved_config"]
    telemetry["schema_compliant"] = telemetry["active_schema"] == telemetry["approved_schema"]
    telemetry["trusted"] = telemetry["trust_state"] == "verified"
    telemetry["usable"] = (
        telemetry["fresh"]
        & (telemetry["quality_state"] == "valid")
        & telemetry["trusted"]
        & (~telemetry["duplicate_detected"])
        & telemetry["firmware_compliant"]
        & telemetry["configuration_compliant"]
        & telemetry["schema_compliant"]
    )

    fleet.to_csv(out / "python_device_inventory_scored.csv", index=False)
    gateways.to_csv(out / "python_gateway_state_scored.csv", index=False)
    telemetry.to_csv(out / "python_telemetry_records_scored.csv", index=False)

    summary = pd.DataFrame([{
        "fleet_assets": len(fleet),
        "online_rate": fleet["online"].mean(),
        "trust_verified_rate": fleet["trusted"].mean(),
        "lifecycle_active_rate": fleet["lifecycle_active"].mean(),
        "credential_valid_rate": fleet["credential_valid"].mean(),
        "firmware_compliance_rate": fleet["firmware_compliant"].mean(),
        "configuration_compliance_rate": fleet["configuration_compliant"].mean(),
        "schema_compliance_rate": fleet["schema_compliant"].mean(),
        "mean_gateway_buffer_pressure": gateways["buffer_pressure"].mean(),
        "gateway_rule_compliance_rate": gateways["rule_compliant"].mean(),
        "usable_telemetry_rate": telemetry["usable"].mean(),
        "stale_telemetry_rate": (~telemetry["fresh"]).mean(),
        "duplicate_replay_rate": telemetry["duplicate_detected"].mean(),
        "mean_freshness_seconds": telemetry["freshness_seconds"].mean()
    }]).round(4)

    summary.to_csv(out / "python_iot_sensor_architecture_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
