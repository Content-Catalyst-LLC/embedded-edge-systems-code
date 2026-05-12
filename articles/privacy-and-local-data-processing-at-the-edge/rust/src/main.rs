// Rust Example: Retention and Disclosure Policy Validator

#[derive(Debug)]
struct DataFlow {
    data_class: String,
    retention_hours: u32,
    upstream_transfer: bool,
    person_revealing: bool,
}

fn validate_privacy_policy(flow: &DataFlow) -> Result<(), String> {
    if flow.person_revealing && flow.upstream_transfer && flow.data_class.starts_with("raw_") {
        return Err(format!("{} cannot be transferred upstream as raw person-revealing data", flow.data_class));
    }

    if flow.person_revealing && flow.retention_hours > 24 {
        return Err(format!("{} exceeds retention threshold for person-revealing data", flow.data_class));
    }

    Ok(())
}

fn main() {
    let flows = vec![
        DataFlow {
            data_class: "raw_video".to_string(),
            retention_hours: 0,
            upstream_transfer: false,
            person_revealing: true,
        },
        DataFlow {
            data_class: "derived_event".to_string(),
            retention_hours: 24,
            upstream_transfer: true,
            person_revealing: false,
        },
    ];

    for flow in flows {
        match validate_privacy_policy(&flow) {
            Ok(_) => println!("{}: PASS", flow.data_class),
            Err(message) => println!("{}: REVIEW - {}", flow.data_class, message),
        }
    }
}
