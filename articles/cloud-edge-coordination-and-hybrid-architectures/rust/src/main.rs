// Rust Example: Authority-Window, Sync-Contract, Version-Skew, and Rollout Validator

#[derive(Debug)]
struct HybridEvent {
    state_age_s: f64,
    sync_lag_s: f64,
    offline_duration_s: f64,
    authority_window_s: f64,
    edge_policy_version: String,
    cloud_policy_version: String,
    edge_model_version: String,
    approved_model_version: String,
    active_version: String,
    target_version: String,
    buffer_backlog: i64,
}

fn validate(event: &HybridEvent) -> Vec<String> {
    let mut issues = Vec::new();

    if event.state_age_s > 120.0 {
        issues.push("state age SLO violation".to_string());
    }

    if event.sync_lag_s > 60.0 {
        issues.push("sync lag SLO violation".to_string());
    }

    if event.offline_duration_s > event.authority_window_s {
        issues.push("offline authority window expired".to_string());
    }

    if event.edge_policy_version != event.cloud_policy_version {
        issues.push("policy drift detected".to_string());
    }

    if event.edge_model_version != event.approved_model_version {
        issues.push("model version skew detected".to_string());
    }

    if event.active_version != event.target_version {
        issues.push("rollout active version gap detected".to_string());
    }

    if event.buffer_backlog > 200 {
        issues.push("buffer backlog SLO violation".to_string());
    }

    issues
}

fn main() {
    let event = HybridEvent {
        state_age_s: 525.0,
        sync_lag_s: 520.0,
        offline_duration_s: 520.0,
        authority_window_s: 300.0,
        edge_policy_version: "policy-1.0".to_string(),
        cloud_policy_version: "policy-1.1".to_string(),
        edge_model_version: "model-2.0".to_string(),
        approved_model_version: "model-2.1".to_string(),
        active_version: "model-2.0".to_string(),
        target_version: "model-2.1".to_string(),
        buffer_backlog: 300,
    };

    let issues = validate(&event);
    println!("Hybrid event accepted: {}", issues.is_empty());

    for issue in issues {
        println!("- {}", issue);
    }
}
