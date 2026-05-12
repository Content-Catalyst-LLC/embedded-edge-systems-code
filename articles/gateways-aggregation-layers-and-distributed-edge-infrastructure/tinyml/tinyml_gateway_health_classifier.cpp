#include <stdio.h>

typedef struct {
    float device_freshness_s;
    float buffer_backlog;
    float protocol_error_rate;
    float replay_lag_s;
    float lineage_complete;
    float site_quality_score;
} GatewayFeatures;

float mock_gateway_anomaly_score(GatewayFeatures x) {
    float score = 0.0f;
    score += x.device_freshness_s > 60.0f ? 0.20f : 0.0f;
    score += x.buffer_backlog > 200.0f ? 0.25f : 0.0f;
    score += x.protocol_error_rate > 0.05f ? 0.20f : 0.0f;
    score += x.replay_lag_s > 120.0f ? 0.20f : 0.0f;
    score += x.lineage_complete < 1.0f ? 0.15f : 0.0f;
    score += x.site_quality_score < 0.80f ? 0.25f : 0.0f;

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
    GatewayFeatures features = {303.0f, 250.0f, 0.08f, 303.0f, 1.0f, 0.42f};
    float score = mock_gateway_anomaly_score(features);

    printf("Gateway anomaly score: %.2f\n", score);
    printf("Gateway health band: %s\n", classify(score));
    printf("Model version: gateway-health-0.1.0\n");

    return 0;
}
