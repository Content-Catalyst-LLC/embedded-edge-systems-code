#include <iostream>
#include <string>

enum class AcquisitionState {
    Configure,
    Sample,
    Validate,
    Degraded,
    Publish
};

struct AcquisitionContext {
    bool config_ok;
    bool sample_fresh;
    bool quality_ok;
    bool bus_ok;
};

AcquisitionState next_state(AcquisitionState state, const AcquisitionContext& ctx) {
    switch (state) {
        case AcquisitionState::Configure:
            return ctx.config_ok ? AcquisitionState::Sample : AcquisitionState::Degraded;
        case AcquisitionState::Sample:
            return (ctx.sample_fresh && ctx.bus_ok) ? AcquisitionState::Validate : AcquisitionState::Degraded;
        case AcquisitionState::Validate:
            return ctx.quality_ok ? AcquisitionState::Publish : AcquisitionState::Degraded;
        case AcquisitionState::Degraded:
            return AcquisitionState::Configure;
        case AcquisitionState::Publish:
            return AcquisitionState::Sample;
    }
    return AcquisitionState::Degraded;
}

int main() {
    AcquisitionContext ctx{true, true, false, true};
    auto state = next_state(AcquisitionState::Validate, ctx);
    std::cout << "next_state=" << static_cast<int>(state) << "\n";
    return 0;
}
