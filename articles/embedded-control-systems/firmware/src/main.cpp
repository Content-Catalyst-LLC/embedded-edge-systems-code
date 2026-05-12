#include <iostream>
#include <algorithm>

float safety_filter(float candidate, float temperature_c, bool deadline_missed) {
    if (deadline_missed) {
        return 0.0f;
    }

    if (temperature_c >= 80.0f) {
        return 0.0f;
    }

    if (temperature_c >= 70.0f) {
        return std::min(std::max(candidate, 0.0f), 0.75f);
    }

    return std::min(std::max(candidate, 0.0f), 1.0f);
}

int main() {
    float setpoint = 1200.0f;
    float estimate = 1080.0f;
    float kp = 0.0025f;

    float candidate = kp * (setpoint - estimate);
    float filtered = safety_filter(candidate, 55.0f, false);

    std::cout << "Candidate command: " << candidate << std::endl;
    std::cout << "Filtered command: " << filtered << std::endl;

    return 0;
}
