#include <stdio.h>

typedef struct {
    float auth_failure_rate;
    float network_exposure;
    float firmware_drift;
} SecurityFeatures;

float mock_security_anomaly_score(SecurityFeatures features) {
    float score = 0.40f * features.auth_failure_rate +
                  0.35f * features.network_exposure +
                  0.25f * features.firmware_drift;

    if (score > 1.0f) return 1.0f;
    if (score < 0.0f) return 0.0f;
    return score;
}

int main(void) {
    SecurityFeatures sample = {0.20f, 0.70f, 0.30f};
    float score = mock_security_anomaly_score(sample);

    printf("Local TinyML security anomaly score: %.2f\n", score);
    return 0;
}
