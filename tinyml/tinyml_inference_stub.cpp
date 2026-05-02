/*
 * TinyML Inference Stub
 * ---------------------
 *
 * Educational scaffold showing the shape of on-device inference.
 */

#include <stdint.h>
#include <stdio.h>

typedef struct {
    float mean_value;
    float standard_deviation;
    float minimum_value;
    float maximum_value;
    float signal_energy;
    float zero_crossing_rate;
} SensorFeatureVector;

float run_tinyml_inference_stub(SensorFeatureVector features) {
    float score = 0.0f;

    score += 0.25f * features.mean_value;
    score += 0.20f * features.standard_deviation;
    score += 0.15f * features.signal_energy;
    score += 0.10f * features.zero_crossing_rate;

    return score;
}

int main(void) {
    SensorFeatureVector features = {
        .mean_value = 0.62f,
        .standard_deviation = 0.18f,
        .minimum_value = 0.10f,
        .maximum_value = 0.95f,
        .signal_energy = 0.74f,
        .zero_crossing_rate = 0.08f
    };

    float score = run_tinyml_inference_stub(features);

    printf("TinyML inference score: %0.3f\n", score);

    return 0;
}
