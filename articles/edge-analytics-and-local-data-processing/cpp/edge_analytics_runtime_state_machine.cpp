/*
 * C++ Example: Edge Analytics Runtime State Machine and Event-Qualification Abstraction
 */

#include <iostream>
#include <string>

enum class AnalyticsState {
    Healthy,
    MissingSamples,
    FeatureIncomplete,
    StaleOutput,
    BufferPressure,
    ReplayDelayed,
    LineageGap,
    Degraded
};

struct AnalyticsSignals {
    double missing_sample_rate;
    bool feature_complete;
    double freshness_s;
    double freshness_threshold_s;
    int buffer_backlog;
    int buffer_high_watermark;
    double replay_lag_s;
    double replay_lag_threshold_s;
    bool lineage_complete;
};

AnalyticsState evaluate(const AnalyticsSignals& s) {
    if (s.missing_sample_rate > 0.05) return AnalyticsState::MissingSamples;
    if (!s.feature_complete) return AnalyticsState::FeatureIncomplete;
    if (s.freshness_s > s.freshness_threshold_s) return AnalyticsState::StaleOutput;
    if (s.buffer_backlog >= s.buffer_high_watermark) return AnalyticsState::BufferPressure;
    if (s.replay_lag_s > s.replay_lag_threshold_s) return AnalyticsState::ReplayDelayed;
    if (!s.lineage_complete) return AnalyticsState::LineageGap;
    return AnalyticsState::Healthy;
}

std::string state_name(AnalyticsState state) {
    switch (state) {
        case AnalyticsState::Healthy: return "Healthy";
        case AnalyticsState::MissingSamples: return "MissingSamples";
        case AnalyticsState::FeatureIncomplete: return "FeatureIncomplete";
        case AnalyticsState::StaleOutput: return "StaleOutput";
        case AnalyticsState::BufferPressure: return "BufferPressure";
        case AnalyticsState::ReplayDelayed: return "ReplayDelayed";
        case AnalyticsState::LineageGap: return "LineageGap";
        case AnalyticsState::Degraded: return "Degraded";
    }
    return "Unknown";
}

int main() {
    AnalyticsSignals signals{
        0.12,
        false,
        330.0,
        60.0,
        250,
        200,
        330.0,
        300.0,
        false
    };

    AnalyticsState state = evaluate(signals);
    std::cout << "Edge analytics runtime state: " << state_name(state) << "\n";

    return 0;
}
