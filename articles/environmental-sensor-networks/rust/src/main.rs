use serde_json::Value;
use std::fs;

fn main() {
    let raw = fs::read_to_string("../config/node_manifest.json").expect("unable to read node manifest");
    let manifest: Value = serde_json::from_str(&raw).expect("node manifest is not valid json");

    let nodes = manifest["nodes"].as_array().expect("nodes must be an array");
    assert!(!nodes.is_empty(), "at least one node is required");

    for node in nodes {
        assert!(node["node_id"].is_string(), "node_id is required");
        assert!(node["site_id"].is_string(), "site_id is required");
        assert!(node["parameters"].is_array(), "parameters array is required");
        assert!(node["radio"].is_string(), "radio is required");
        assert!(node["power"].is_string(), "power profile is required");
        assert!(node["quality_checks"].is_array(), "quality_checks array is required");
    }

    println!("validated {} environmental node manifests", nodes.len());
}
