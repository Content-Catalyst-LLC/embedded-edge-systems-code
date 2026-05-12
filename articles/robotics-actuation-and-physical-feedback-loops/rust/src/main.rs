// Rust Example: Safety Envelope and Command-Bound Validator

#[derive(Debug)]
struct SafetyEnvelope {
    position_min: f64,
    position_max: f64,
    velocity_max_abs: f64,
    command_max_abs: f64,
    tracking_error_fault: f64,
}

#[derive(Debug)]
struct RobotCommand {
    position: f64,
    velocity: f64,
    command: f64,
    tracking_error: f64,
}

fn validate_command(cmd: &RobotCommand, env: &SafetyEnvelope) -> Result<(), String> {
    if cmd.position < env.position_min || cmd.position > env.position_max {
        return Err("position outside workspace envelope".to_string());
    }
    if cmd.velocity.abs() > env.velocity_max_abs {
        return Err("velocity outside safety envelope".to_string());
    }
    if cmd.command.abs() > env.command_max_abs {
        return Err("command exceeds actuator bound".to_string());
    }
    if cmd.tracking_error.abs() > env.tracking_error_fault {
        return Err("tracking error exceeds fault threshold".to_string());
    }
    Ok(())
}

fn main() {
    let env = SafetyEnvelope {
        position_min: -1.0,
        position_max: 1.0,
        velocity_max_abs: 1.5,
        command_max_abs: 1.0,
        tracking_error_fault: 0.15,
    };

    let cmd = RobotCommand {
        position: 0.42,
        velocity: 0.35,
        command: 0.80,
        tracking_error: 0.04,
    };

    match validate_command(&cmd, &env) {
        Ok(_) => println!("Command accepted"),
        Err(message) => println!("Command rejected: {}", message),
    }
}
