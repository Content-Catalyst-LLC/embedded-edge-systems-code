#include <iostream>
#include <string>

enum class Connectivity { Online, Degraded, Offline };
enum class TrustState { Verified, Degraded, Unknown, Unverified };
enum class RuntimeMode { Normal, Degraded, FailSafe, FailOperational };

struct RuntimeSignals {
    Connectivity connectivity;
    TrustState trust_state;
    double cpu_utilization;
    double memory_utilization;
    double storage_utilization;
    double clock_drift_ms;
    int watchdog_resets;
    int buffer_backlog;
    bool rollback_ready;
};

RuntimeMode evaluate(const RuntimeSignals& s) {
    if (s.trust_state == TrustState::Unknown || s.trust_state == TrustState::Unverified) return RuntimeMode::FailSafe;
    if (s.connectivity == Connectivity::Offline && s.rollback_ready) return RuntimeMode::FailOperational;
    if (s.cpu_utilization > 0.85 || s.memory_utilization > 0.85 || s.storage_utilization > 0.90 ||
        s.clock_drift_ms > 50.0 || s.watchdog_resets > 1 || s.buffer_backlog > 250) return RuntimeMode::Degraded;
    return RuntimeMode::Normal;
}

std::string mode_name(RuntimeMode mode) {
    switch (mode) {
        case RuntimeMode::Normal: return "Normal";
        case RuntimeMode::Degraded: return "Degraded";
        case RuntimeMode::FailSafe: return "FailSafe";
        case RuntimeMode::FailOperational: return "FailOperational";
    }
    return "Unknown";
}

int main() {
    RuntimeSignals s{Connectivity::Offline, TrustState::Verified, 0.62, 0.70, 0.55, 12.0, 0, 160, true};
    std::cout << "Runtime mode: " << mode_name(evaluate(s)) << "\n";
    return 0;
}
