// Rust Example: Protocol-Map, Buffer-Policy, Replay-Policy, and Lineage Validator

#[derive(Debug)]
struct GatewayEvent {
    device_id: String,
    gateway_id: String,
    protocol_family: String,
    unit: String,
    acquisition_time_present: bool,
    idempotency_key_present: bool,
    buffer_backlog: i64,
    high_watermark: i64,
    replay_lag_s: f64,
    lineage_complete: bool,
}

fn validate(event: &GatewayEvent) -> Vec<String> {
    let mut issues = Vec::new();

    if event.device_id.is_empty() {
        issues.push("missing child device identity".to_string());
    }

    if event.gateway_id.is_empty() {
        issues.push("missing parent gateway identity".to_string());
    }

    if event.protocol_family.is_empty() {
        issues.push("missing protocol family".to_string());
    }

    if event.unit.is_empty() {
        issues.push("missing physical unit".to_string());
    }

    if !event.acquisition_time_present {
        issues.push("missing acquisition time".to_string());
    }

    if !event.idempotency_key_present {
        issues.push("missing replay idempotency key".to_string());
    }

    if event.buffer_backlog >= event.high_watermark {
        issues.push("buffer high watermark reached".to_string());
    }

    if event.replay_lag_s > 120.0 {
        issues.push("replay lag SLO violation".to_string());
    }

    if !event.lineage_complete {
        issues.push("lineage incomplete".to_string());
    }

    issues
}

fn main() {
    let event = GatewayEvent {
        device_id: "dev-vib-001".to_string(),
        gateway_id: "gw-001".to_string(),
        protocol_family: "spi".to_string(),
        unit: "g".to_string(),
        acquisition_time_present: true,
        idempotency_key_present: true,
        buffer_backlog: 250,
        high_watermark: 200,
        replay_lag_s: 30.0,
        lineage_complete: true,
    };

    let issues = validate(&event);
    println!("Gateway event accepted: {}", issues.is_empty());

    for issue in issues {
        println!("- {}", issue);
    }
}
