/*
 * C Example: Rolling Windows, RMS/Peak Features, Thresholding, and Local Event Flags
 */

#include <stdio.h>
#include <stdbool.h>
#include <math.h>

#define WINDOW_SIZE 8

typedef struct {
    float rms;
    float peak;
    float crest_factor;
    bool feature_complete;
} FeatureWindow;

float compute_rms(const float* x, int n) {
    float sum_sq = 0.0f;
    for (int i = 0; i < n; i++) {
        sum_sq += x[i] * x[i];
    }
    return sqrtf(sum_sq / n);
}

float compute_peak(const float* x, int n) {
    float peak = 0.0f;
    for (int i = 0; i < n; i++) {
        float abs_value = fabsf(x[i]);
        if (abs_value > peak) {
            peak = abs_value;
        }
    }
    return peak;
}

FeatureWindow compute_features(const float* x, int n, float missing_sample_rate) {
    FeatureWindow features;
    features.rms = compute_rms(x, n);
    features.peak = compute_peak(x, n);
    features.crest_factor = features.rms > 0.0f ? features.peak / features.rms : 0.0f;
    features.feature_complete = missing_sample_rate <= 0.05f;
    return features;
}

const char* classify_event(FeatureWindow features) {
    if (!features.feature_complete) return "degraded";
    if (features.rms > 0.65f && features.peak > 0.80f) return "fault";
    if (features.rms > 0.45f || features.peak > 0.75f) return "warning";
    return "normal";
}

int main(void) {
    float window[WINDOW_SIZE] = {0.1f, 0.2f, 0.5f, 0.8f, 0.7f, 0.4f, 0.2f, 0.1f};
    FeatureWindow features = compute_features(window, WINDOW_SIZE, 0.01f);
    const char* state = classify_event(features);

    printf("RMS: %.3f\n", features.rms);
    printf("Peak: %.3f\n", features.peak);
    printf("Crest factor: %.3f\n", features.crest_factor);
    printf("Feature complete: %s\n", features.feature_complete ? "true" : "false");
    printf("Event state: %s\n", state);

    return 0;
}
