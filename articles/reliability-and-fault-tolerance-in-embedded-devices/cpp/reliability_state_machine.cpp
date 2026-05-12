#include <iostream>

enum class ReliabilityState {
    NormalService,
    SuspectedFault,
    DegradedService,
    Recovery,
    RepeatedFailure,
    SafeShutdown
};

struct ReliabilityContext {
    bool fault_detected;
    bool recovery_success;
    bool repeated_resets;
    bool safety_boundary_violated;
    bool degraded_allowed;
};

ReliabilityState next_state(ReliabilityState state, const ReliabilityContext& ctx) {
    if (ctx.safety_boundary_violated) return ReliabilityState::SafeShutdown;
    if (ctx.repeated_resets) return ReliabilityState::RepeatedFailure;
    if (ctx.fault_detected && ctx.degraded_allowed) return ReliabilityState::DegradedService;
    if (ctx.fault_detected) return ReliabilityState::Recovery;
    if (state == ReliabilityState::Recovery && ctx.recovery_success) return ReliabilityState::NormalService;
    return ReliabilityState::NormalService;
}

int main() {
    ReliabilityContext ctx{true, false, false, false, true};
    auto state = next_state(ReliabilityState::NormalService, ctx);
    std::cout << "next_state=" << static_cast<int>(state) << "\n";
    return 0;
}
