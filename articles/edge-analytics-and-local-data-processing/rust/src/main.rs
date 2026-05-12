// Rust Example: Feature Schema, Event Contract, Replay Policy, and Uplink Policy Validator

#[derive(Debug)]
struct AnalyticsEvent {
    event_id: String,
    window_id: String,
    signal_id: String,
    feature_version: String,
    rule_version: String,
    idempotency_key: String,
    uplink_mode: String,
    freshness_s: f64,
    freshness_threshold_s: f64,
    missing_sample_rate: f64,
    feature_complete: bool,
    replay_lag_s: f64,
    lineage_complete: bool,
    drop_reason: String,
}

fn validate(event: &AnalyticsEvent) -> Vec<String> {
    let mut issues = Vec::new();

    if event.event_id.is_empty() {
        issues.push("missing event identity".to_string());
    }

    if event.window_id.is_empty() {
        issues.push("missing window identity".to_string());
    }

    if event.signal_id.is_empty() {
        issues.push("missing signal identity".to_string());
    }

    if event.feature_version.is_empty() {
        issues.push("missing feature version".to_string());
    }

    if event.rule_version.is_empty() {
        issues.push("missing rule version".to_string());
    }

    if event.idempotency_key.is_empty() {
        issues.push("missing idempotency key".to_string());
    }

    if event.freshness_s > event.freshness_threshold_s {
        issues.push("stale local output".to_string());
    }

    if event.missing_sample_rate > 0.05 || !event.feature_complete {
        issues.push("feature completeness violation".to_string());
    }

    if event.replay_lag_s > 300.0 {
        issues.push("replay lag violation".to_string());
    }

    if !event.lineage_complete {
        issues.push("lineage incomplete".to_string());
    }

    if event.uplink_mode == "suppressed" && event.drop_reason == "none" {
        issues.push("suppressed record missing drop reason".to_string());
    }

    issues
}

fn main() {
    let event = AnalyticsEvent {
        event_id: "evt-004".to_string(),
        window_id: "win-004".to_string(),
        signal_id: "current-main".to_string(),
        feature_version: "features-1.1".to_string(),
        rule_version: "rules-1.1".to_string(),
        idempotency_key: "evt-004-key".to_string(),
        uplink_mode: "suppressed".to_string(),
        freshness_s: 330.0,
        freshness_threshold_s: 60.0,
        missing_sample_rate: 0.12,
        feature_complete: false,
        replay_lag_s: 330.0,
        lineage_complete: false,
        drop_reason: "missing_feature_context".to_string(),
    };

    let issues = validate(&event);
    println!("Analytics event accepted: {}", issues.is_empty());

    for issue in issues {
        println!("- {}", issue);
    }
}
