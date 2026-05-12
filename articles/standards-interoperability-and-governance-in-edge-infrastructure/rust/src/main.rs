// Rust Example: Lifecycle Policy Validator
//
// This example models lifecycle support state as a safety-oriented governance
// constraint. End-of-support devices require decommissioning or formal exception.

#[derive(Debug)]
enum SupportState {
    Supported,
    LimitedSupport,
    EndOfSupport,
}

#[derive(Debug)]
struct DevicePolicy {
    device_id: String,
    support_state: SupportState,
    firmware_current: bool,
    security_baseline_met: bool,
}

fn validate_policy(device: &DevicePolicy) -> Result<(), String> {
    match device.support_state {
        SupportState::EndOfSupport => {
            Err(format!("{} requires decommissioning or approved exception", device.device_id))
        }
        SupportState::LimitedSupport if !device.security_baseline_met => {
            Err(format!("{} has limited support and fails security baseline", device.device_id))
        }
        _ if !device.firmware_current => {
            Err(format!("{} requires firmware update review", device.device_id))
        }
        _ => Ok(()),
    }
}

fn main() {
    let devices = vec![
        DevicePolicy {
            device_id: "gw-chi-001".to_string(),
            support_state: SupportState::Supported,
            firmware_current: true,
            security_baseline_met: true,
        },
        DevicePolicy {
            device_id: "plc-det-007".to_string(),
            support_state: SupportState::LimitedSupport,
            firmware_current: true,
            security_baseline_met: false,
        },
        DevicePolicy {
            device_id: "cam-stl-021".to_string(),
            support_state: SupportState::EndOfSupport,
            firmware_current: false,
            security_baseline_met: false,
        },
    ];

    for device in devices {
        match validate_policy(&device) {
            Ok(_) => println!("{}: PASS", device.device_id),
            Err(message) => println!("{}: REVIEW - {}", device.device_id, message),
        }
    }
}
