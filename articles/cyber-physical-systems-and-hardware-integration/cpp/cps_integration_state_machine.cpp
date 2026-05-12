/*
 * C++ Example: CPS Integration State Machine and Hardware-Interface Abstraction
 */

#include <iostream>
#include <string>
#include <cmath>

enum class CpsState {
    Startup,
    InterfaceCheck,
    Calibration,
    Nominal,
    Warning,
    Degraded,
    SafeStop,
    FaultLatch,
    Recovery
};

struct CpsSignals {
    bool interface_contract_valid;
    bool calibration_valid;
    bool clock_sync_valid;
    double sensor_age_ms;
    double deadline_slack_ms;
    double total_uncertainty;
    double uncertainty_budget;
    bool actuator_saturated;
    bool authorized_reset;
};

CpsState next_state(CpsState state, const CpsSignals& s) {
    switch (state) {
        case CpsState::Startup:
            return CpsState::InterfaceCheck;
        case CpsState::InterfaceCheck:
            return s.interface_contract_valid ? CpsState::Calibration : CpsState::FaultLatch;
        case CpsState::Calibration:
            return s.calibration_valid ? CpsState::Nominal : CpsState::FaultLatch;
        case CpsState::Nominal:
            if (!s.clock_sync_valid || s.sensor_age_ms > 3.0 || s.deadline_slack_ms < 0.0) {
                return CpsState::SafeStop;
            }
            if (s.total_uncertainty > s.uncertainty_budget || s.actuator_saturated) {
                return CpsState::Warning;
            }
            return CpsState::Nominal;
        case CpsState::Warning:
            if (s.deadline_slack_ms < 0.0 || s.sensor_age_ms > 3.0) {
                return CpsState::SafeStop;
            }
            return CpsState::Degraded;
        case CpsState::Degraded:
            if (s.deadline_slack_ms < 0.0 || !s.clock_sync_valid) {
                return CpsState::SafeStop;
            }
            return CpsState::Degraded;
        case CpsState::SafeStop:
            return CpsState::FaultLatch;
        case CpsState::FaultLatch:
            return s.authorized_reset ? CpsState::Recovery : CpsState::FaultLatch;
        case CpsState::Recovery:
            return CpsState::InterfaceCheck;
    }
    return CpsState::FaultLatch;
}

std::string state_name(CpsState state) {
    switch (state) {
        case CpsState::Startup: return "Startup";
        case CpsState::InterfaceCheck: return "InterfaceCheck";
        case CpsState::Calibration: return "Calibration";
        case CpsState::Nominal: return "Nominal";
        case CpsState::Warning: return "Warning";
        case CpsState::Degraded: return "Degraded";
        case CpsState::SafeStop: return "SafeStop";
        case CpsState::FaultLatch: return "FaultLatch";
        case CpsState::Recovery: return "Recovery";
    }
    return "Unknown";
}

int main() {
    CpsSignals signals{
        true,
        true,
        true,
        1.2,
        0.62,
        24.0,
        35.0,
        true,
        false
    };

    CpsState state = CpsState::Nominal;
    CpsState next = next_state(state, signals);

    std::cout << "Current CPS state: " << state_name(state) << "\n";
    std::cout << "Next CPS state: " << state_name(next) << "\n";

    return 0;
}
