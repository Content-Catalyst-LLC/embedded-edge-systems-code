/*
 * TinyML Companion Example: Policy-Aware On-Device Inference
 *
 * This portable C++ stub is designed to represent the governance wrapper around
 * a TinyML model. In a production embedded system, the mock inference function
 * would be replaced with TensorFlow Lite Micro, Edge Impulse, or another TinyML
 * runtime.
 */

#include <stdio.h>

typedef enum {
    POLICY_ALLOW_REPORTING,
    POLICY_LOCAL_ONLY,
    POLICY_DISABLE_INFERENCE
} InferencePolicy;

typedef struct {
    float sensor_value;
    float device_temperature;
    float voltage_state;
} FeatureVector;

float mock_tinyml_anomaly_score(FeatureVector features) {
    float score = 0.0f;

    if (features.sensor_value > 0.80f) {
        score += 0.50f;
    }
    if (features.device_temperature > 70.0f) {
        score += 0.30f;
    }
    if (features.voltage_state < 0.20f) {
        score += 0.20f;
    }

    if (score > 1.0f) {
        return 1.0f;
    }

    return score;
}

int main(void) {
    FeatureVector sample = {
        .sensor_value = 0.86f,
        .device_temperature = 74.5f,
        .voltage_state = 0.44f
    };

    InferencePolicy policy = POLICY_LOCAL_ONLY;
    float score = mock_tinyml_anomaly_score(sample);

    if (policy == POLICY_DISABLE_INFERENCE) {
        printf("Inference disabled by governance policy.\n");
        return 0;
    }

    if (policy == POLICY_LOCAL_ONLY) {
        printf("Local-only TinyML anomaly score: %.2f\n", score);
        return 0;
    }

    printf("TinyML anomaly score eligible for upstream reporting: %.2f\n", score);
    return 0;
}
