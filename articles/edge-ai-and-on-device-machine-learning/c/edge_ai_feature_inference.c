/*
 * C Example: Feature Extraction, Thresholding, Memory-Budget Checks, and Local Action
 */

#include <stdio.h>
#include <stdbool.h>
#include <math.h>

#define WINDOW_SIZE 8

typedef struct {
    float rms;
    float peak;
    float confidence;
    const char* predicted_class;
} InferenceResult;

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

InferenceResult mock_infer(const float* x, int n) {
    InferenceResult result;
    result.rms = compute_rms(x, n);
    result.peak = compute_peak(x, n);
    result.confidence = result.rms > 0.60f ? 0.91f : 0.72f;
    result.predicted_class = result.rms > 0.60f ? "fault" : "warning";
    return result;
}

bool memory_budget_ok(unsigned int model_kb, unsigned int tensor_kb, unsigned int flash_kb, unsigned int ram_kb) {
    return model_kb <= flash_kb && tensor_kb <= ram_kb;
}

int main(void) {
    float window[WINDOW_SIZE] = {0.1f, 0.2f, 0.5f, 0.8f, 0.7f, 0.4f, 0.2f, 0.1f};
    InferenceResult result = mock_infer(window, WINDOW_SIZE);

    bool mem_ok = memory_budget_ok(82, 28, 512, 128);
    bool action_allowed = result.confidence >= 0.80f && mem_ok;

    printf("RMS: %.3f\n", result.rms);
    printf("Peak: %.3f\n", result.peak);
    printf("Predicted class: %s\n", result.predicted_class);
    printf("Confidence: %.2f\n", result.confidence);
    printf("Memory OK: %s\n", mem_ok ? "true" : "false");
    printf("Local action: %s\n", action_allowed ? "allowed" : "fallback");

    return 0;
}
