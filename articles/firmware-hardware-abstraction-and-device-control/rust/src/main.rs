use serde_json::Value;
use std::fs;

fn main() {
    let raw = fs::read_to_string("../config/driver_manifest.json").expect("unable to read driver manifest");
    let manifest: Value = serde_json::from_str(&raw).expect("driver manifest is not valid json");

    let drivers = manifest["drivers"].as_array().expect("drivers must be an array");
    assert!(!drivers.is_empty(), "at least one driver is required");

    for driver in drivers {
        assert!(driver["driver_id"].is_string(), "driver_id required");
        assert!(driver["device_name"].is_string(), "device_name required");
        assert!(driver["bus"].is_string(), "bus required");
        assert!(driver["owner_layer"].is_string(), "owner_layer required");
        assert!(driver["interrupts"].is_array(), "interrupts array required");
        assert!(driver["power_states"].is_array(), "power_states array required");

        let contract = &driver["api_contract"];
        assert!(contract["blocking_behavior"].is_string(), "blocking behavior required");
        assert!(contract["isr_safe_functions"].is_array(), "ISR safety statement required");
        assert!(contract["timeout_ms"].is_number(), "timeout required");
        assert!(contract["error_semantics"].is_string(), "error semantics required");
    }

    println!("validated {} driver manifests", drivers.len());
}
