#include <iostream>
#include <string>

enum class MeasurementState {
    Valid,
    Stale,
    LowSNR,
    CalibrationExpired,
    CoefficientMismatch,
    Saturated,
    DriftWarning,
    LineageIncomplete
};

std::string allowed_use(MeasurementState state) {
    switch (state) {
        case MeasurementState::Valid: return "control, analytics, alarms, reporting";
        case MeasurementState::Stale: return "historical display only";
        case MeasurementState::LowSNR: return "low-confidence trend context";
        case MeasurementState::CalibrationExpired: return "provisional trend analysis";
        case MeasurementState::CoefficientMismatch: return "diagnostic logging only";
        case MeasurementState::Saturated: return "range-exceeded alarm only";
        case MeasurementState::DriftWarning: return "diagnostic review and recalibration planning";
        case MeasurementState::LineageIncomplete: return "diagnostic review only";
    }
    return "unknown";
}

int main() {
    MeasurementState state = MeasurementState::CoefficientMismatch;
    std::cout << "Allowed use: " << allowed_use(state) << "\n";
    return 0;
}
