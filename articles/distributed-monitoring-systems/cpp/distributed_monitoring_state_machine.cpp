#include <iostream>
#include <string>

enum class MonitoringState {
    ObservedValid,
    ObservedLowConfidence,
    ObservedStale,
    CoverageDegraded,
    GatewayDegraded,
    SyncDegraded,
    BackfillReplay,
    VisibilityLost
};

std::string allowed_use(MonitoringState state) {
    switch (state) {
        case MonitoringState::ObservedValid: return "normal monitoring, aggregation, alerts";
        case MonitoringState::ObservedLowConfidence: return "diagnostic review, qualified trends";
        case MonitoringState::ObservedStale: return "historical reconstruction only";
        case MonitoringState::CoverageDegraded: return "local claims only; no unqualified system claim";
        case MonitoringState::GatewayDegraded: return "qualified cluster visibility only";
        case MonitoringState::SyncDegraded: return "not for time-sensitive fusion";
        case MonitoringState::BackfillReplay: return "historical recovery only";
        case MonitoringState::VisibilityLost: return "no current-state claim";
    }
    return "unknown";
}

int main() {
    MonitoringState state = MonitoringState::CoverageDegraded;
    std::cout << "Allowed use: " << allowed_use(state) << "\n";
    return 0;
}
