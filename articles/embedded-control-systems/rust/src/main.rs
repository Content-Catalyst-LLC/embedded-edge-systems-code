// Rust Example: Timing-Budget and Safety-Envelope Validator

#[derive(Debug)]
struct ControlEvent {
    candidate_command: f64,
    filtered_command: f64,
    loop_jitter_ms: f64,
    deadline_slack_ms: f64,
    control_error: f64,
    temperature_c: f64,
}

fn validate_event(event: &ControlEvent) -> Result<(), String> {
    if event.deadline_slack_ms < 0.0 {
        return Err("deadline missed".to_string());
    }

    if event.loop_jitter_ms.abs() > 0.35 {
        return Err("jitter outside timing budget".to_string());
    }

    if event.candidate_command < 0.0 || event.candidate_command > 1.0 {
        if (event.filtered_command < 0.0) || (event.filtered_command > 1.0) {
            return Err("filtered command still outside actuator bounds".to_string());
        }
    }

    if event.control_error.abs() >= 160.0 {
        return Err("control error exceeds fault threshold".to_string());
    }

    if event.temperature_c >= 80.0 {
        return Err("thermal fault threshold exceeded".to_string());
    }

    Ok(())
}

fn main() {
    let event = ControlEvent {
        candidate_command: 1.18,
        filtered_command: 1.0,
        loop_jitter_ms: 0.30,
        deadline_slack_ms: 0.62,
        control_error: 81.0,
        temperature_c: 55.0,
    };

    match validate_event(&event) {
        Ok(_) => println!("Control event accepted"),
        Err(message) => println!("Control event rejected: {}", message),
    }
}
