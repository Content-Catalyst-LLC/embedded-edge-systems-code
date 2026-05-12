#include <iostream>
#include <string>

std::string filter_action(std::string candidate, float confidence, float latency_ms, float latency_budget_ms) {
    if (latency_ms > latency_budget_ms) {
        return "safe_stop";
    }
    if (confidence < 0.65f) {
        return "safe_stop";
    }
    if (confidence < 0.75f) {
        return "pause_and_request_review";
    }
    return candidate;
}

int main() {
    std::string candidate = "reroute";
    float confidence = 0.82f;
    float latency_ms = 56.0f;
    float latency_budget_ms = 80.0f;

    std::cout << "Candidate action: " << candidate << std::endl;
    std::cout << "Filtered action: " << filter_action(candidate, confidence, latency_ms, latency_budget_ms) << std::endl;

    return 0;
}
