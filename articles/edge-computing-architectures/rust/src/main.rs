struct EdgeAsset {
    layer: String,
    active_version: String,
    approved_version: String,
    trust_state: String,
    runtime_assurance_state: String,
    watchdog_resets: u32,
    cpu_utilization: f64,
    rollback_ready: bool,
}

fn validate(a: &EdgeAsset) -> Vec<String> {
    let mut issues = Vec::new();
    if !["device", "gateway", "local-edge", "regional-edge", "cloud"].contains(&a.layer.as_str()) {
        issues.push("invalid edge layer".to_string());
    }
    if a.active_version != a.approved_version { issues.push("version skew".to_string()); }
    if a.trust_state != "verified" { issues.push("trust state not verified".to_string()); }
    if a.runtime_assurance_state != "ready" { issues.push("runtime assurance not ready".to_string()); }
    if a.watchdog_resets > 1 { issues.push("watchdog threshold exceeded".to_string()); }
    if a.cpu_utilization > 0.85 { issues.push("cpu pressure".to_string()); }
    if !a.rollback_ready { issues.push("rollback path not ready".to_string()); }
    issues
}

fn main() {
    let asset = EdgeAsset {
        layer: "gateway".to_string(),
        active_version: "gw-2.0".to_string(),
        approved_version: "gw-2.1".to_string(),
        trust_state: "verified".to_string(),
        runtime_assurance_state: "degraded".to_string(),
        watchdog_resets: 2,
        cpu_utilization: 0.88,
        rollback_ready: true,
    };
    let issues = validate(&asset);
    println!("Edge asset accepted: {}", issues.is_empty());
    for issue in issues { println!("- {}", issue); }
}
