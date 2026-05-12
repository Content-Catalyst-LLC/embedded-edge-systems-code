#include <stdio.h>

typedef struct {
    float tracking_error_abs;
    float loop_jitter_ms;
    float actuator_current_a;
    float saturation_flag;
} RoboticsFeatures;

float mock_fault_score(RoboticsFeatures x) {
    float score = 0.0f;
    score += 2.0f * x.tracking_error_abs;
    score += 0.10f * x.loop_jitter_ms;
    score += 0.12f * x.actuator_current_a;
    score += 0.35f * x.saturation_flag;

    if (score > 1.0f) return 1.0f;
    if (score < 0.0f) return 0.0f;
    return score;
}

const char* classify_fault(float score) {
    if (score >= 0.75f) return "fault";
    if (score >= 0.45f) return "warning";
    return "normal";
}

int main(void) {
    RoboticsFeatures features = {0.06f, 2.1f, 3.2f, 1.0f};
    float score = mock_fault_score(features);

    printf("Local TinyML robotics fault score: %.2f\n", score);
    printf("Fault band: %s\n", classify_fault(score));

    return 0;
}
