use serde_json::Value;
use std::fs;

fn main() {
    let raw = fs::read_to_string("../config/fault_model.json").expect("unable to read fault model");
    let manifest: Value = serde_json::from_str(&raw).expect("fault model is not valid json");

    let classes = manifest["fault_classes"].as_array().expect("fault_classes must be an array");
    assert!(!classes.is_empty(), "at least one fault class is required");

    for class in classes {
        assert!(class["class"].is_string(), "fault class name is required");
        assert!(class["examples"].is_array(), "fault examples are required");
        assert!(class["preferred_response"].is_array(), "preferred response is required");
    }

    let evidence = manifest["required_evidence"].as_array().expect("required_evidence must be an array");
    assert!(evidence.len() >= 3, "required evidence should include diagnostic fields");

    println!("validated {} fault classes", classes.len());
}
