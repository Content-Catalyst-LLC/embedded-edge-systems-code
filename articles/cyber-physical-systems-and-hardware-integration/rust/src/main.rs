// Rust Example: Interface-Contract, Command-Bound, Uncertainty-Budget, and Timing-Budget Validator

#[derive(Debug)]
struct CpsEvent {
    signal_name: String,
    physical_unit: String,
    sensor_age_ms: f64,
    maximum_age_ms: f64,
    candidate_command: f64,
    filtered_command: f64,
    deadline_slack_ms: f64,
    total_uncertainty: f64,
    uncertainty_budget: f64,
}

fn validate(event: &CpsEvent) -> Result<(), String> {
    if event.signal_name.is_empty() {
        return Err("missing signal name".to_string());
    }

    if event.physical_unit.is_empty() {
        return Err("missing physical unit".to_string());
    }

    if event.sensor_age_ms > event.maximum_age_ms {
        return Err("sensor freshness contract violated".to_string());
    }

    if event.deadline_slack_ms < 0.0 {
        return Err("timing contract violated".to_string());
    }

    if event.total_uncertainty > event.uncertainty_budget {
        return Err("uncertainty budget violated".to_string());
    }

    if event.filtered_command < 0.0 || event.filtered_command > 1.0 {
        return Err("filtered command outside actuator bounds".to_string());
    }

    if event.candidate_command != event.filtered_command {
        println!("Runtime assurance modified the command.");
    }

    Ok(())
}

fn main() {
    let event = CpsEvent {
        signal_name: "pwm_duty_cycle".to_string(),
        physical_unit: "ratio".to_string(),
        sensor_age_ms: 1.2,
        maximum_age_ms: 3.0,
        candidate_command: 1.18,
        filtered_command: 1.0,
        deadline_slack_ms: 0.62,
        total_uncertainty: 24.0,
        uncertainty_budget: 35.0,
    };

    match validate(&event) {
        Ok(_) => println!("CPS event accepted"),
        Err(message) => println!("CPS event rejected: {}", message),
    }
}
