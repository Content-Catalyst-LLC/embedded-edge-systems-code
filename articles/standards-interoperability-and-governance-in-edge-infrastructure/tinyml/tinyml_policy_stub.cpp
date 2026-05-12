/*
 * TinyML Example: Policy-Aware Inference Stub
 *
 * This stub shows how constrained inference logic can include policy-aware
 * fallback behavior. In production, the inference function would be generated
 * by a TinyML toolchain or linked from an embedded model library.
 */

#include <stdio.h>

typedef enum {
    POLICY_ALLOW_INFERENCE,
    POLICY_REQUIRE_LOCAL_ONLY,
    POLICY_DISABLE_INFERENCE
} PolicyState;

float mock_anomaly_score(float sensor_value) {
    if (sensor_value > 90.0f) {
        return 0.97f;
    }
    if (sensor_value > 70.0f) {
        return 0.72f;
    }
    return 0.18f;
}

int main(void) {
    float sensor_value = 96.5f;
    PolicyState policy = POLICY_REQUIRE_LOCAL_ONLY;

    if (policy == POLICY_DISABLE_INFERENCE) {
        printf("Inference disabled by governance policy.\n");
        return 0;
    }

    float score = mock_anomaly_score(sensor_value);

    if (policy == POLICY_REQUIRE_LOCAL_ONLY) {
        printf("Local-only inference score: %.2f\n", score);
    } else {
        printf("Inference score eligible for upstream reporting: %.2f\n", score);
    }

    return 0;
}
