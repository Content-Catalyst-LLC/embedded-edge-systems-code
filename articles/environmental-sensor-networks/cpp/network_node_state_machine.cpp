#include <iostream>

enum class NodeState {
    BaselineSampling,
    EventSampling,
    Degraded,
    OfflineBuffering,
    Recovery
};

struct NodeContext {
    bool event_detected;
    bool link_available;
    bool battery_low;
    bool quality_ok;
    bool replay_pending;
};

NodeState next_state(NodeState state, const NodeContext& ctx) {
    if (ctx.battery_low || !ctx.quality_ok) {
        return NodeState::Degraded;
    }
    if (!ctx.link_available) {
        return NodeState::OfflineBuffering;
    }
    if (ctx.replay_pending) {
        return NodeState::Recovery;
    }
    if (ctx.event_detected) {
        return NodeState::EventSampling;
    }
    return NodeState::BaselineSampling;
}

int main() {
    NodeContext ctx{true, true, false, true, false};
    auto state = next_state(NodeState::BaselineSampling, ctx);
    std::cout << "next_state=" << static_cast<int>(state) << "\n";
    return 0;
}
