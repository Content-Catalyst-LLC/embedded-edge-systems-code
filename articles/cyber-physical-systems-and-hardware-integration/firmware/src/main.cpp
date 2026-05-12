#include <iostream>
#include <algorithm>

float runtime_assurance(float candidate, float sensor_age_ms, float deadline_slack_ms, float uncertainty, float uncertainty_budget) {
    if (sensor_age_ms > 3.0f) {
        return 0.0f;
    }

    if (deadline_slack_ms < 0.0f) {
        return 0.0f;
    }

    if (uncertainty > uncertainty_budget) {
        return std::min(std::max(candidate, 0.0f), 0.5f);
    }

    return std::min(std::max(candidate, 0.0f), 1.0f);
}

int main() {
    float estimate = 1080.0f;
    float reference = 1200.0f;
    float candidate = 0.0025f * (reference - estimate);

    float filtered = runtime_assurance(candidate, 1.2f, 0.62f, 24.0f, 35.0f);

    std::cout << "Candidate command: " << candidate << std::endl;
    std::cout << "Filtered command: " << filtered << std::endl;

    return 0;
}
