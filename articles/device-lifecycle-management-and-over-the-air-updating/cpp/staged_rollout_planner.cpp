/*
 * C++ Example: Staged Rollout Planner for Edge Device Groups
 *
 * This example creates a simple staged rollout plan that avoids blocked devices
 * and prioritizes canary groups before wider deployment rings.
 */

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Device {
    std::string id;
    std::string ring;
    std::string support_state;
    double readiness_score;
};

bool eligible(const Device& device) {
    return device.support_state != "end-of-support" && device.readiness_score >= 0.70;
}

int ring_order(const std::string& ring) {
    if (ring == "canary") return 0;
    if (ring == "ring-1") return 1;
    if (ring == "ring-2") return 2;
    return 3;
}

int main() {
    std::vector<Device> devices = {
        {"edge-gw-001", "canary", "supported", 0.88},
        {"sensor-014", "ring-1", "supported", 0.75},
        {"plc-007", "ring-2", "limited-support", 0.68},
        {"camera-021", "blocked", "end-of-support", 0.32},
        {"gw-nyc-009", "ring-1", "supported", 0.87}
    };

    std::sort(devices.begin(), devices.end(), [](const Device& a, const Device& b) {
        return ring_order(a.ring) < ring_order(b.ring);
    });

    std::cout << "Staged rollout candidates:\n";
    for (const auto& device : devices) {
        if (eligible(device)) {
            std::cout << "- " << device.id << " (" << device.ring << ")\n";
        }
    }

    return 0;
}
