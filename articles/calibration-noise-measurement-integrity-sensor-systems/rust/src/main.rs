struct MeasurementRecord {
    sensor_id: String,
    calibrated_value: f64,
    valid_min: f64,
    valid_max: f64,
    calibration_version: String,
    firmware_version: String,
    expanded_uncertainty: f64,
    snr_db: f64,
    lineage_complete: bool,
    traceability_complete: bool,
}

fn validate(record: &MeasurementRecord) -> Vec<String> {
    let mut issues = Vec::new();

    if record.sensor_id.is_empty() {
        issues.push("missing sensor id".to_string());
    }
    if record.calibration_version.is_empty() {
        issues.push("missing calibration version".to_string());
    }
    if record.firmware_version.is_empty() {
        issues.push("missing firmware version".to_string());
    }
    if record.calibrated_value < record.valid_min || record.calibrated_value > record.valid_max {
        issues.push("out of range".to_string());
    }
    if record.expanded_uncertainty > 1.5 {
        issues.push("high uncertainty".to_string());
    }
    if record.snr_db < 20.0 {
        issues.push("low snr".to_string());
    }
    if !record.lineage_complete {
        issues.push("lineage incomplete".to_string());
    }
    if !record.traceability_complete {
        issues.push("traceability incomplete".to_string());
    }

    issues
}

fn main() {
    let record = MeasurementRecord {
        sensor_id: "temp-003".to_string(),
        calibrated_value: 110.0,
        valid_min: 0.0,
        valid_max: 120.0,
        calibration_version: "cal-2024-06".to_string(),
        firmware_version: "fw-0.9".to_string(),
        expanded_uncertainty: 1.8,
        snr_db: 12.0,
        lineage_complete: false,
        traceability_complete: false,
    };

    let issues = validate(&record);
    println!("Measurement record accepted: {}", issues.is_empty());
    for issue in issues {
        println!("- {}", issue);
    }
}
