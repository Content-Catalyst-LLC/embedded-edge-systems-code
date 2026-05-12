use serde_json::Value;
use std::fs;

fn main() {
    let raw = fs::read_to_string("../config/platform_manifest.json").expect("unable to read platform manifest");
    let manifest: Value = serde_json::from_str(&raw).expect("platform manifest is not valid json");

    let dimensions = manifest["platform_selection_dimensions"]
        .as_array()
        .expect("platform_selection_dimensions must be an array");
    assert!(!dimensions.is_empty(), "at least one platform selection dimension required");

    let requirements = &manifest["candidate_requirements"];
    for required_group in ["compute", "memory", "i_o", "power", "security", "lifecycle"] {
        assert!(requirements[required_group].is_array(), "missing candidate requirement group");
    }

    println!("validated platform manifest with {} dimensions", dimensions.len());
}
