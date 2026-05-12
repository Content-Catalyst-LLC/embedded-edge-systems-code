#include <iostream>
#include <algorithm>

float clamp(float value, float low, float high) {
    return std::max(low, std::min(value, high));
}

int main() {
    float reference = 0.50f;
    float measured = 0.42f;
    float kp = 4.0f;
    float command = clamp(kp * (reference - measured), -1.0f, 1.0f);

    std::cout << "Robotics firmware scaffold command: " << command << std::endl;
    return 0;
}
