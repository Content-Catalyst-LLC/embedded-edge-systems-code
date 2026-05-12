// Rust Example: Authority-Bound and Safety-Envelope Action Validator

#[derive(Debug)]
struct Decision {
    candidate_action: String,
    confidence: f64,
    latency_ms: f64,
    latency_budget_ms: f64,
    autonomy_level: String,
    safety_state: String,
}

fn allowed_actions(autonomy_level: &str) -> Vec<&'static str> {
    match autonomy_level {
        "bounded_local" => vec![
            "continue",
            "slow_down",
            "reroute",
            "slow_reroute",
            "pause_and_request_review",
            "safe_stop",
        ],
        "supervised" => vec![
            "continue",
            "slow_down",
            "reroute",
            "slow_reroute",
            "pause_and_request_review",
            "safe_stop",
            "proceed_slow",
        ],
        _ => vec!["safe_stop", "pause_and_request_review"],
    }
}

fn validate(decision: &Decision) -> Result<(), String> {
    let allowed = allowed_actions(&decision.autonomy_level);

    if !allowed.contains(&decision.candidate_action.as_str()) {
        return Err("candidate action violates authority boundary".to_string());
    }

    if decision.safety_state == "degraded" {
        return Err("safety state requires safe stop".to_string());
    }

    if decision.latency_ms > decision.latency_budget_ms {
        return Err("latency budget violation".to_string());
    }

    if decision.confidence < 0.65 {
        return Err("confidence below motion threshold".to_string());
    }

    if decision.confidence < 0.75 && decision.candidate_action != "pause_and_request_review" {
        return Err("confidence below nominal-action threshold".to_string());
    }

    Ok(())
}

fn main() {
    let decision = Decision {
        candidate_action: "reroute".to_string(),
        confidence: 0.82,
        latency_ms: 56.0,
        latency_budget_ms: 80.0,
        autonomy_level: "bounded_local".to_string(),
        safety_state: "normal".to_string(),
    };

    match validate(&decision) {
        Ok(_) => println!("Decision accepted"),
        Err(message) => println!("Decision rejected: {}", message),
    }
}
