#include <stdio.h>

typedef struct {
    float rms;
    float peak;
    float crest_factor;
    float spectral_energy;
    float bandpower_low;
    float bandpower_high;
} VibrationFeatures;

float mock_fault_score(VibrationFeatures x) {
    float score = 0.0f;
    score += x.rms > 0.55f ? 0.25f : 0.0f;
    score += x.peak > 0.75f ? 0.25f : 0.0f;
    score += x.crest_factor > 3.0f ? 0.20f : 0.0f;
    score += x.spectral_energy > 0.60f ? 0.20f : 0.0f;
    score += x.bandpower_high > x.bandpower_low ? 0.10f : 0.0f;

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
    VibrationFeatures features = {0.62f, 0.81f, 3.4f, 0.72f, 0.22f, 0.35f};
    float score = mock_fault_score(features);
    const char* label = classify(score);

    printf("Fault score: %.2f\n", score);
    printf("Class: %s\n", label);
    printf("Model version: model-1.2\n");

    return 0;
}
