/*
 * C++ Example: Gateway Runtime State Machine and Aggregation-Health Abstraction
 */

#include <iostream>
#include <string>

enum class GatewayState {
    Healthy,
    Buffering,
    Backpressure,
    ProtocolDegraded,
    AggregationDegraded,
    Replaying,
    Recovering,
    Fault
};

struct GatewaySignals {
    bool upstream_reachable;
    int buffer_backlog;
    int high_watermark;
    double protocol_error_rate;
    double lineage_completeness_rate;
    double site_quality_score;
    bool replay_in_progress;
};

GatewayState next_state(const GatewaySignals& s) {
    if (s.protocol_error_rate > 0.10) {
        return GatewayState::ProtocolDegraded;
    }

    if (s.lineage_completeness_rate < 0.95 || s.site_quality_score < 0.80) {
        return GatewayState::AggregationDegraded;
    }

    if (!s.upstream_reachable) {
        return GatewayState::Buffering;
    }

    if (s.buffer_backlog >= s.high_watermark) {
        return GatewayState::Backpressure;
    }

    if (s.replay_in_progress) {
        return GatewayState::Replaying;
    }

    return GatewayState::Healthy;
}

std::string state_name(GatewayState state) {
    switch (state) {
        case GatewayState::Healthy: return "Healthy";
        case GatewayState::Buffering: return "Buffering";
        case GatewayState::Backpressure: return "Backpressure";
        case GatewayState::ProtocolDegraded: return "ProtocolDegraded";
        case GatewayState::AggregationDegraded: return "AggregationDegraded";
        case GatewayState::Replaying: return "Replaying";
        case GatewayState::Recovering: return "Recovering";
        case GatewayState::Fault: return "Fault";
    }
    return "Unknown";
}

int main() {
    GatewaySignals signals{
        true,
        250,
        200,
        0.04,
        0.99,
        0.88,
        false
    };

    GatewayState state = next_state(signals);
    std::cout << "Gateway runtime state: " << state_name(state) << "\n";

    return 0;
}
