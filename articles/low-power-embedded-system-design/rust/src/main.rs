use serde_json::Value;
use std::fs;

fn main() {
    let raw = fs::read_to_string("../config/power_manifest.json").expect("unable to read power manifest");
    let manifest: Value = serde_json::from_str(&raw).expect("power manifest is not valid json");

    let states = manifest["power_states"].as_array().expect("power_states must be an array");
    assert!(!states.is_empty(), "at least one power state is required");

    for state in states {
        assert!(state["state"].is_string(), "state name is required");
        assert!(state["retention"].is_array(), "retention array is required");
        assert!(state["peripherals_enabled"].is_array(), "peripherals_enabled array is required");
        assert!(state["wake_sources"].is_array(), "wake_sources array is required");
    }

    let brownout = &manifest["brownout_policy"];
    assert!(brownout["storage_write_inhibit_voltage"].is_number(), "storage write threshold required");
    assert!(brownout["brownout_voltage_threshold"].is_number(), "brownout threshold required");

    println!("validated {} power states", states.len());
}
