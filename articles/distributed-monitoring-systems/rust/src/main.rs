struct MonitoringRecord {
    event_id: String,
    node_id: String,
    coverage_zone: String,
    event_time_present: bool,
    processing_time_present: bool,
    quality_state: String,
    calibration_state: String,
    clock_skew_ms: i32,
    idempotency_key: String,
    duplicate_detected: bool,
}

fn validate(record: &MonitoringRecord) -> Vec<String> {
    let mut issues = Vec::new();

    if record.event_id.is_empty() { issues.push("missing event id".to_string()); }
    if record.node_id.is_empty() { issues.push("missing node id".to_string()); }
    if record.coverage_zone.is_empty() { issues.push("missing coverage zone".to_string()); }
    if !record.event_time_present { issues.push("missing event time".to_string()); }
    if !record.processing_time_present { issues.push("missing processing time".to_string()); }
    if record.quality_state != "valid" { issues.push("quality state not valid".to_string()); }
    if record.calibration_state != "valid" { issues.push("calibration not valid".to_string()); }
    if record.clock_skew_ms.abs() > 1000 { issues.push("clock skew violation".to_string()); }
    if record.idempotency_key.is_empty() { issues.push("missing idempotency key".to_string()); }
    if record.duplicate_detected { issues.push("duplicate replay".to_string()); }

    issues
}

fn main() {
    let record = MonitoringRecord {
        event_id: "evt-water-003".to_string(),
        node_id: "node-water-downstream-001".to_string(),
        coverage_zone: "zone-downstream".to_string(),
        event_time_present: true,
        processing_time_present: true,
        quality_state: "valid".to_string(),
        calibration_state: "valid".to_string(),
        clock_skew_ms: 1800,
        idempotency_key: "node-water-downstream-001-301".to_string(),
        duplicate_detected: false,
    };

    let issues = validate(&record);
    println!("Monitoring record accepted: {}", issues.is_empty());
    for issue in issues {
        println!("- {}", issue);
    }
}
