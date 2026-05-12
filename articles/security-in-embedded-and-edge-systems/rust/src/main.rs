// Rust Example: Lifecycle and Credential Policy Validator

#[derive(Debug)]
struct SecurityPolicy {
    device_id: String,
    support_state: String,
    credential_current: bool,
    secure_boot: bool,
    rollback_ready: bool,
    exposure: f32,
}

fn validate(policy: &SecurityPolicy) -> Result<(), String> {
    if policy.support_state == "end-of-support" {
        return Err(format!("{} is end-of-support and must be retired or isolated", policy.device_id));
    }
    if !policy.credential_current {
        return Err(format!("{} has stale credentials", policy.device_id));
    }
    if !policy.secure_boot {
        return Err(format!("{} does not report secure boot", policy.device_id));
    }
    if !policy.rollback_ready {
        return Err(format!("{} lacks rollback readiness", policy.device_id));
    }
    if policy.exposure >= 0.70 {
        return Err(format!("{} has high exposure and requires segmentation review", policy.device_id));
    }
    Ok(())
}

fn main() {
    let device = SecurityPolicy {
        device_id: "gw-chi-001".to_string(),
        support_state: "supported".to_string(),
        credential_current: true,
        secure_boot: true,
        rollback_ready: true,
        exposure: 0.20,
    };

    match validate(&device) {
        Ok(_) => println!("{}: PASS", device.device_id),
        Err(message) => println!("{}: REVIEW - {}", device.device_id, message),
    }
}
