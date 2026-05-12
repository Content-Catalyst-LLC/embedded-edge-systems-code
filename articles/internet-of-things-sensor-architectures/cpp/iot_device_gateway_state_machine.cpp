#include <iostream>
#include <string>

enum class Connectivity { Online, Degraded, Offline };
enum class TrustState { Verified, Unverified };
enum class LifecycleState { Provisioning, Active, Updating, Quarantined, Retired };
enum class RuntimeState { Normal, Degraded, Quarantined, Retired };

struct DeviceGatewayState {
    Connectivity connectivity;
    TrustState trust;
    LifecycleState lifecycle;
    double buffer_pressure;
    bool firmware_compliant;
    bool config_compliant;
    bool schema_compliant;
    bool command_authority_bounded;
};

RuntimeState evaluate(const DeviceGatewayState& s) {
    if (s.lifecycle == LifecycleState::Retired) return RuntimeState::Retired;
    if (s.trust == TrustState::Unverified || s.lifecycle == LifecycleState::Quarantined) return RuntimeState::Quarantined;
    if (s.connectivity != Connectivity::Online || s.buffer_pressure > 0.6 ||
        !s.firmware_compliant || !s.config_compliant || !s.schema_compliant ||
        !s.command_authority_bounded) return RuntimeState::Degraded;
    return RuntimeState::Normal;
}

std::string name(RuntimeState state) {
    switch(state) {
        case RuntimeState::Normal: return "normal";
        case RuntimeState::Degraded: return "degraded";
        case RuntimeState::Quarantined: return "quarantined";
        case RuntimeState::Retired: return "retired";
    }
    return "unknown";
}

int main() {
    DeviceGatewayState s{Connectivity::Degraded, TrustState::Verified, LifecycleState::Active, 0.65, false, false, true, true};
    std::cout << "Runtime state: " << name(evaluate(s)) << "\n";
    return 0;
}
