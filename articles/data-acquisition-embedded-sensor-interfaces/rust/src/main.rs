use serde_json::Value;
use std::fs;

fn main() {
    let manifest_path = "../config/sensor_interface_manifest.json";
    let raw = fs::read_to_string(manifest_path).expect("unable to read manifest");
    let parsed: Value = serde_json::from_str(&raw).expect("manifest is not valid json");

    let interfaces = parsed["interfaces"].as_array().expect("interfaces must be an array");
    assert!(!interfaces.is_empty(), "at least one interface is required");

    for interface in interfaces {
        assert!(interface["name"].is_string(), "interface requires name");
        assert!(interface["type"].is_string(), "interface requires type");
        assert!(interface["channels"].is_array(), "interface requires channels array");
    }

    println!("validated {} acquisition interfaces", interfaces.len());
}
