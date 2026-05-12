struct TelemetryRecord {
    event_id: String,
    device_id: String,
    event_time_present: bool,
    processing_time_present: bool,
    idempotency_key: String,
    quality_state: String,
    trust_state: String,
    firmware_compliant: bool,
    configuration_compliant: bool,
    schema_compliant: bool,
    duplicate_detected: bool,
}

fn validate(record: &TelemetryRecord) -> Vec<String> {
    let mut issues = Vec::new();

    if record.event_id.is_empty() { issues.push("missing event id".to_string()); }
    if record.device_id.is_empty() { issues.push("missing device id".to_string()); }
    if !record.event_time_present { issues.push("missing event time".to_string()); }
    if !record.processing_time_present { issues.push("missing processing time".to_string()); }
    if record.idempotency_key.is_empty() { issues.push("missing idempotency key".to_string()); }
    if record.quality_state != "valid" { issues.push("quality state not valid".to_string()); }
    if record.trust_state != "verified" { issues.push("unverified trust state".to_string()); }
    if !record.firmware_compliant { issues.push("firmware skew".to_string()); }
    if !record.configuration_compliant { issues.push("configuration skew".to_string()); }
    if !record.schema_compliant { issues.push("schema skew".to_string()); }
    if record.duplicate_detected { issues.push("duplicate replay".to_string()); }

    issues
}

fn main() {
    let record = TelemetryRecord {
        event_id: "evt-005".to_string(),
        device_id: "dev-vib-002".to_string(),
        event_time_present: true,
        processing_time_present: true,
        idempotency_key: "dev-vib-002-505".to_string(),
        quality_state: "valid".to_string(),
        trust_state: "unverified".to_string(),
        firmware_compliant: false,
        configuration_compliant: true,
        schema_compliant: false,
        duplicate_detected: false,
    };

    let issues = validate(&record);
    println!("Telemetry record accepted: {}", issues.is_empty());
    for issue in issues {
        println!("- {}", issue);
    }
}
