/*
 * C++ Example: Autonomy State Machine and Behavior Selection
 */

#include <iostream>
#include <string>
#include <cmath>

enum class AutonomyState {
    Nominal,
    ReducedAutonomy,
    DegradedMode,
    HumanHandoff,
    SafeStop,
    Quarantined
};

struct DecisionContext {
    double confidence;
    double latency_ms;
    double latency_budget_ms;
    double input_drift_score;
    bool security_trust_valid;
    bool human_override_requested;
};

AutonomyState select_state(const DecisionContext& context) {
    if (!context.security_trust_valid) {
        return AutonomyState::Quarantined;
    }

    if (context.human_override_requested) {
        return AutonomyState::HumanHandoff;
    }

    if (context.latency_ms > context.latency_budget_ms || context.confidence < 0.65) {
        return AutonomyState::SafeStop;
    }

    if (context.input_drift_score >= 0.40) {
        return AutonomyState::DegradedMode;
    }

    if (context.confidence < 0.75 || context.input_drift_score >= 0.25) {
        return AutonomyState::ReducedAutonomy;
    }

    return AutonomyState::Nominal;
}

std::string state_name(AutonomyState state) {
    switch (state) {
        case AutonomyState::Nominal: return "Nominal";
        case AutonomyState::ReducedAutonomy: return "ReducedAutonomy";
        case AutonomyState::DegradedMode: return "DegradedMode";
        case AutonomyState::HumanHandoff: return "HumanHandoff";
        case AutonomyState::SafeStop: return "SafeStop";
        case AutonomyState::Quarantined: return "Quarantined";
    }
    return "Unknown";
}

int main() {
    DecisionContext context{
        0.72,
        61.0,
        80.0,
        0.16,
        true,
        false
    };

    AutonomyState state = select_state(context);
    std::cout << "Selected autonomy state: " << state_name(state) << "\n";

    return 0;
}
