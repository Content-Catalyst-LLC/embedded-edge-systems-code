#include <iostream>

enum class PowerState {
    Active,
    Sensing,
    Communication,
    Sleep,
    DeepSleep,
    Wake,
    LowEnergyDegraded,
    BrownoutProtection,
    Recovery
};

struct PowerContext {
    bool event_pending;
    bool communication_pending;
    bool battery_low;
    bool brownout_risk;
    bool wake_source_valid;
    bool retained_state_valid;
};

PowerState next_state(PowerState state, const PowerContext& ctx) {
    if (ctx.brownout_risk) return PowerState::BrownoutProtection;
    if (ctx.battery_low) return PowerState::LowEnergyDegraded;
    if (state == PowerState::Wake && !ctx.retained_state_valid) return PowerState::Recovery;
    if (ctx.communication_pending) return PowerState::Communication;
    if (ctx.event_pending && ctx.wake_source_valid) return PowerState::Sensing;
    return PowerState::DeepSleep;
}

int main() {
    PowerContext ctx{false, false, false, false, true, true};
    auto state = next_state(PowerState::Active, ctx);
    std::cout << "next_state=" << static_cast<int>(state) << "\n";
    return 0;
}
