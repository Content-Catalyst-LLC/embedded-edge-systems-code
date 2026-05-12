/*
 * C++ Example: Privacy-Aware Gateway Transformation Policy
 *
 * This example models a gateway that transforms raw inputs into derived events
 * before allowing upstream disclosure.
 */

#include <iostream>
#include <string>

struct EdgeObservation {
    std::string signal_type;
    double value;
    bool person_revealing;
    int retention_hours;
};

std::string transform_observation(const EdgeObservation& obs) {
    if (obs.signal_type == "video") {
        return obs.value > 0.5 ? "zone_occupied" : "zone_clear";
    }
    if (obs.signal_type == "audio") {
        return obs.value > 0.7 ? "wake_word_detected" : "no_command";
    }
    return "aggregate_metric";
}

bool allow_upstream(const EdgeObservation& obs) {
    if (obs.person_revealing && obs.retention_hours > 24) {
        return false;
    }
    return true;
}

int main() {
    EdgeObservation obs{"video", 0.76, true, 0};
    std::string transformed = transform_observation(obs);

    std::cout << "Transformed output: " << transformed << "\n";
    std::cout << "Upstream transfer allowed: " << (allow_upstream(obs) ? "yes" : "no") << "\n";

    return 0;
}
