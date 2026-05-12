// Rust Example: Lifecycle Policy Validator for Support State and Rollback Readiness

#[derive(Debug)]
enum SupportState {
    Supported,
    LimitedSupport,
    EndOfSupport,
}

#[derive(Debug)]
struct DeviceLifecycleState {
    device_id: String,
    support_state: SupportState,
    rollback_ready: bool,
    identity_verified: bool,
    compatibility_verified: bool,
}

fn approve_update(device: &DeviceLifecycleState) -> Result<(), String> {
    match device.support_state {
        SupportState::EndOfSupport => Err(format!("{} is end-of-support and must not be updated", device.device_id)),
        SupportState::LimitedSupport if !device.rollback_ready => Err(format!("{} requires rollback review", device.device_id)),
        _ if !device.identity_verified => Err(format!("{} identity is not verified", device.device_id)),
        _ if !device.compatibility_verified => Err(format!("{} compatibility is not verified", device.device_id)),
        _ => Ok(()),
    }
}

fn main() {
    let fleet = vec![
        DeviceLifecycleState {
            device_id: "edge-gw-001".to_string(),
            support_state: SupportState::Supported,
            rollback_ready: true,
            identity_verified: true,
            compatibility_verified: true,
        },
        DeviceLifecycleState {
            device_id: "camera-021".to_string(),
            support_state: SupportState::EndOfSupport,
            rollback_ready: false,
            identity_verified: false,
            compatibility_verified: false,
        },
    ];

    for device in fleet {
        match approve_update(&device) {
            Ok(_) => println!("{}: OTA APPROVED", device.device_id),
            Err(reason) => println!("{}: OTA BLOCKED - {}", device.device_id, reason),
        }
    }
}
