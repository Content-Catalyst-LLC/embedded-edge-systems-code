#include <iostream>

enum class DeviceState {
    Reset,
    Init,
    Configured,
    Active,
    Suspended,
    Fault,
    Recovery,
    Update,
    Rollback,
    Disabled
};

struct DeviceContext {
    bool init_ok;
    bool fault_detected;
    bool suspend_requested;
    bool resume_requested;
    bool update_requested;
    bool update_failed;
    bool recovery_ok;
};

DeviceState next_state(DeviceState state, const DeviceContext& ctx) {
    if (ctx.update_failed) return DeviceState::Rollback;
    if (ctx.update_requested) return DeviceState::Update;
    if (ctx.fault_detected) return DeviceState::Fault;
    if (state == DeviceState::Fault && ctx.recovery_ok) return DeviceState::Recovery;
    if (state == DeviceState::Reset && ctx.init_ok) return DeviceState::Init;
    if (state == DeviceState::Init && ctx.init_ok) return DeviceState::Configured;
    if (ctx.suspend_requested) return DeviceState::Suspended;
    if (state == DeviceState::Suspended && ctx.resume_requested) return DeviceState::Active;
    return DeviceState::Active;
}

int main() {
    DeviceContext ctx{true, false, false, false, false, false, false};
    auto state = next_state(DeviceState::Reset, ctx);
    std::cout << "next_state=" << static_cast<int>(state) << "\n";
    return 0;
}
