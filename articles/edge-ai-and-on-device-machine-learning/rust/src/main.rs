// Rust Example: Model Budget, Inference Event, Runtime, and Deployment Readiness Validator

#[derive(Debug)]
struct InferenceEvent {
    model_size_kb: f64,
    flash_budget_kb: f64,
    tensor_arena_kb: f64,
    ram_budget_kb: f64,
    latency_ms: f64,
    latency_budget_ms: f64,
    confidence: f64,
    confidence_threshold: f64,
    backend_output_delta: f64,
    backend_delta_tolerance: f64,
    model_version: String,
    approved_model_version: String,
    sensor_health: String,
}

fn validate(event: &InferenceEvent) -> Vec<String> {
    let mut issues = Vec::new();

    if event.model_size_kb > event.flash_budget_kb {
        issues.push("model size exceeds flash budget".to_string());
    }

    if event.tensor_arena_kb > event.ram_budget_kb {
        issues.push("tensor arena exceeds RAM budget".to_string());
    }

    if event.latency_ms > event.latency_budget_ms {
        issues.push("latency budget violation".to_string());
    }

    if event.confidence < event.confidence_threshold {
        issues.push("low confidence fallback required".to_string());
    }

    if event.backend_output_delta > event.backend_delta_tolerance {
        issues.push("backend parity violation".to_string());
    }

    if event.model_version != event.approved_model_version {
        issues.push("model version skew detected".to_string());
    }

    if event.sensor_health != "healthy" {
        issues.push("sensor health degraded".to_string());
    }

    issues
}

fn main() {
    let event = InferenceEvent {
        model_size_kb: 1536.0,
        flash_budget_kb: 4096.0,
        tensor_arena_kb: 384.0,
        ram_budget_kb: 2048.0,
        latency_ms: 7.8,
        latency_budget_ms: 20.0,
        confidence: 0.89,
        confidence_threshold: 0.80,
        backend_output_delta: 0.031,
        backend_delta_tolerance: 0.025,
        model_version: "model-1.2".to_string(),
        approved_model_version: "model-1.2".to_string(),
        sensor_health: "healthy".to_string(),
    };

    let issues = validate(&event);
    println!("Deployment event accepted: {}", issues.is_empty());

    for issue in issues {
        println!("- {}", issue);
    }
}
