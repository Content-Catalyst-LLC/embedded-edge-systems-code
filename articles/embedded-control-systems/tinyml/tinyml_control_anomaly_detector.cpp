#include <stdio.h>

typedef struct {
    float abs_control_error;
    float saturation_flag;
    float loop_jitter_ms;
    float deadline_slack_ms;
    float temperature_c;
} ControlFeatures;

float mock_anomaly_score(ControlFeatures x) {
    float score = 0.0f;
    score += 0.003f * x.abs_control_error;
    score += 0.25f * x.saturation_flag;
    score += 0.20f * x.loop_jitter_ms;
    score += x.deadline_slack_ms < 0.2f ? 0.30f : 0.0f;
    score += x.temperature_c >= 70.0f ? 0.35f : 0.0f;

    if (score > 1.0f) return 1.0f;
    if (score < 0.0f) return 0.0f;
    return score;
}

const char* classify_anomaly(float score) {
    if (score >= 0.75f) return "fault";
    if (score >= 0.45f) return "warning";
    return "normal";
}

int main(void) {
    ControlFeatures features = {81.0f, 1.0f, 0.30f, 0.62f, 55.0f};
    float score = mock_anomaly_score(features);

    printf("Embedded control anomaly score: %.2f\n", score);
    printf("Anomaly band: %s\n", classify_anomaly(score));

    return 0;
}
