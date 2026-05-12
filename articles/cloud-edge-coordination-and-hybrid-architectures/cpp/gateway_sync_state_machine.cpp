/*
 * C++ Example: Gateway Sync State Machine and Buffer Management
 */

#include <iostream>
#include <string>

enum class GatewayState {
    Connected,
    Buffering,
    Degraded,
    Reconnecting,
    Reconciling,
    HoldForReview,
    Recovered
};

struct GatewaySignals {
    bool cloud_reachable;
    int offline_duration_s;
    int authority_window_s;
    int buffer_backlog;
    bool policy_drift;
    bool model_skew;
    bool conflict_detected;
};

GatewayState next_state(GatewayState state, const GatewaySignals& s) {
    if (!s.cloud_reachable && s.offline_duration_s <= s.authority_window_s) {
        return GatewayState::Buffering;
    }

    if (!s.cloud_reachable && s.offline_duration_s > s.authority_window_s) {
        return GatewayState::Degraded;
    }

    if (state == GatewayState::Degraded && s.cloud_reachable) {
        return GatewayState::Reconnecting;
    }

    if (s.cloud_reachable && s.buffer_backlog > 0) {
        return GatewayState::Reconciling;
    }

    if (s.conflict_detected || s.policy_drift || s.model_skew) {
        return GatewayState::HoldForReview;
    }

    return GatewayState::Recovered;
}

std::string state_name(GatewayState state) {
    switch (state) {
        case GatewayState::Connected: return "Connected";
        case GatewayState::Buffering: return "Buffering";
        case GatewayState::Degraded: return "Degraded";
        case GatewayState::Reconnecting: return "Reconnecting";
        case GatewayState::Reconciling: return "Reconciling";
        case GatewayState::HoldForReview: return "HoldForReview";
        case GatewayState::Recovered: return "Recovered";
    }
    return "Unknown";
}

int main() {
    GatewaySignals signals{
        false,
        520,
        300,
        300,
        true,
        true,
        true
    };

    GatewayState state = GatewayState::Connected;
    GatewayState next = next_state(state, signals);

    std::cout << "Current gateway state: " << state_name(state) << "\n";
    std::cout << "Next gateway state: " << state_name(next) << "\n";

    return 0;
}
