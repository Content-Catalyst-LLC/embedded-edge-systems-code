#include <stdio.h>

typedef struct {
    float sensor_feature_mean;
    float sensor_feature_std;
    float temperature_c;
    float offline_duration_s;
    float buffer_backlog;
} HybridFeatures;

float mock_anomaly_score(HybridFeatures x) {
    float score = 0.0f;
    score += x.sensor_feature_std > 10.0f ? 0.30f : 0.0f;
    score += x.temperature_c > 70.0f ? 0.30f : 0.0f;
    score += x.offline_duration_s > 300.0f ? 0.25f : 0.0f;
    score += x.buffer_backlog > 200.0f ? 0.20f : 0.0f;

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
    HybridFeatures features = {42.0f, 12.5f, 72.0f, 520.0f, 300.0f};
    float score = mock_anomaly_score(features);

    printf("Hybrid edge anomaly score: %.2f\n", score);
    printf("Anomaly band: %s\n", classify(score));
    printf("Model version: model-2.1\n");

    return 0;
}
