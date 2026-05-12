#include <stdio.h>

typedef struct {
    float sensor_age_ms;
    float deadline_slack_ms;
    float loop_jitter_ms;
    float actuator_saturated;
    float interface_error;
    float uncertainty_fraction;
} CpsFeatures;

float mock_anomaly_score(CpsFeatures x) {
    float score = 0.0f;
    score += x.sensor_age_ms > 3.0f ? 0.35f : 0.0f;
    score += x.deadline_slack_ms < 0.0f ? 0.45f : 0.0f;
    score += x.loop_jitter_ms > 0.35f ? 0.25f : 0.0f;
    score += 0.20f * x.actuator_saturated;
    score += 0.30f * x.interface_error;
    score += x.uncertainty_fraction > 1.0f ? 0.35f : 0.15f * x.uncertainty_fraction;

    if (score > 1.0f) return 1.0f;
    if (score < 0.0f) return 0.0f;
    return score;
}

const char* classify(float score) {
    if (score >= 0.75f) return "fault";
    if (score >= 0.45f) return "warning";
    return "normal";
}

int main(void) {
    CpsFeatures features = {1.4f, 0.62f, 0.30f, 1.0f, 0.0f, 0.71f};
    float score = mock_anomaly_score(features);

    printf("CPS anomaly score: %.2f\n", score);
    printf("CPS anomaly band: %s\n", classify(score));

    return 0;
}
