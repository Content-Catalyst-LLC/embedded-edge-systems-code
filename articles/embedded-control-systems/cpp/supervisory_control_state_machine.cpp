/*
 * C++ Example: Supervisory Control State Machine and Command Validation
 */

#include <iostream>
#include <string>
#include <cmath>

enum class ControlState {
    Startup,
    Calibration,
    OpenLoopTest,
    ClosedLoopNominal,
    Warning,
    DegradedControl,
    SafeStop,
    FaultLatch,
    Recovery
};

struct ControlSignals {
    double control_error;
    double loop_jitter_ms;
    double deadline_slack_ms;
    bool saturated;
    double temperature_c;
    bool authorized_reset;
};

ControlState next_state(ControlState state, const ControlSignals& signals) {
    switch (state) {
        case ControlState::Startup:
            return ControlState::Calibration;
        case ControlState::Calibration:
            return ControlState::OpenLoopTest;
        case ControlState::OpenLoopTest:
            return ControlState::ClosedLoopNominal;
        case ControlState::ClosedLoopNominal:
            if (signals.deadline_slack_ms < 0.0 || std::abs(signals.control_error) >= 160.0 || signals.temperature_c >= 80.0) {
                return ControlState::SafeStop;
            }
            if (signals.saturated || std::abs(signals.control_error) >= 80.0 || signals.loop_jitter_ms >= 0.35) {
                return ControlState::Warning;
            }
            return ControlState::ClosedLoopNominal;
        case ControlState::Warning:
            if (signals.deadline_slack_ms < 0.0 || signals.temperature_c >= 80.0) {
                return ControlState::SafeStop;
            }
            return ControlState::DegradedControl;
        case ControlState::DegradedControl:
            if (signals.deadline_slack_ms < 0.0 || std::abs(signals.control_error) >= 160.0) {
                return ControlState::SafeStop;
            }
            return ControlState::DegradedControl;
        case ControlState::SafeStop:
            return ControlState::FaultLatch;
        case ControlState::FaultLatch:
            return signals.authorized_reset ? ControlState::Recovery : ControlState::FaultLatch;
        case ControlState::Recovery:
            return ControlState::Calibration;
    }
    return ControlState::FaultLatch;
}

std::string state_name(ControlState state) {
    switch (state) {
        case ControlState::Startup: return "Startup";
        case ControlState::Calibration: return "Calibration";
        case ControlState::OpenLoopTest: return "OpenLoopTest";
        case ControlState::ClosedLoopNominal: return "ClosedLoopNominal";
        case ControlState::Warning: return "Warning";
        case ControlState::DegradedControl: return "DegradedControl";
        case ControlState::SafeStop: return "SafeStop";
        case ControlState::FaultLatch: return "FaultLatch";
        case ControlState::Recovery: return "Recovery";
    }
    return "Unknown";
}

int main() {
    ControlSignals signals{
        95.0,
        0.42,
        0.35,
        true,
        68.0,
        false
    };

    ControlState state = ControlState::ClosedLoopNominal;
    ControlState next = next_state(state, signals);

    std::cout << "Current state: " << state_name(state) << "\n";
    std::cout << "Next state: " << state_name(next) << "\n";

    return 0;
}
