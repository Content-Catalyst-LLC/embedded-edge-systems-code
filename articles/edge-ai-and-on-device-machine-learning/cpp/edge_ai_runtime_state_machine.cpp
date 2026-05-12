/*
 * C++ Example: Inference Runtime State Machine and Decision-Policy Abstraction
 */

#include <iostream>
#include <string>

enum class RuntimeState {
    Ready,
    MemoryViolation,
    LatencyViolation,
    BackendMismatch,
    LowConfidence,
    SensorDegraded,
    ModelSkew,
    Fallback,
    ActionAllowed
};

struct InferenceSignals {
    bool memory_ok;
    bool latency_ok;
    double backend_delta;
    double backend_tolerance;
    double confidence;
    double confidence_threshold;
    bool sensor_healthy;
    bool approved_model_active;
};

RuntimeState evaluate(const InferenceSignals& s) {
    if (!s.memory_ok) return RuntimeState::MemoryViolation;
    if (!s.latency_ok) return RuntimeState::LatencyViolation;
    if (s.backend_delta > s.backend_tolerance) return RuntimeState::BackendMismatch;
    if (s.confidence < s.confidence_threshold) return RuntimeState::LowConfidence;
    if (!s.sensor_healthy) return RuntimeState::SensorDegraded;
    if (!s.approved_model_active) return RuntimeState::ModelSkew;
    return RuntimeState::ActionAllowed;
}

std::string state_name(RuntimeState state) {
    switch (state) {
        case RuntimeState::Ready: return "Ready";
        case RuntimeState::MemoryViolation: return "MemoryViolation";
        case RuntimeState::LatencyViolation: return "LatencyViolation";
        case RuntimeState::BackendMismatch: return "BackendMismatch";
        case RuntimeState::LowConfidence: return "LowConfidence";
        case RuntimeState::SensorDegraded: return "SensorDegraded";
        case RuntimeState::ModelSkew: return "ModelSkew";
        case RuntimeState::Fallback: return "Fallback";
        case RuntimeState::ActionAllowed: return "ActionAllowed";
    }
    return "Unknown";
}

int main() {
    InferenceSignals signals{
        true,
        true,
        0.031,
        0.025,
        0.89,
        0.80,
        true,
        true
    };

    RuntimeState state = evaluate(signals);
    std::cout << "Inference runtime state: " << state_name(state) << "\n";

    return 0;
}
