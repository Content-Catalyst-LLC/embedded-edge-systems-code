#include <stdio.h>

typedef struct {
    float rms;
    float peak;
    float crest_factor;
    float spectral_energy;
    float bandpower_low;
    float bandpower_high;
    float missing_sample_rate;
} EdgeFeatures;

float mock_event_score(EdgeFeatures x) {
    float score = 0.0f;
    score += x.rms > 0.45f ? 0.25f : 0.0f;
    score += x.peak > 0.75f ? 0.25f : 0.0f;
    score += x.crest_factor > 3.0f ? 0.20f : 0.0f;
    score += x.spectral_energy > 0.60f ? 0.20f : 0.0f;
    score += x.bandpower_high > x.bandpower_low ? 0.10f : 0.0f;

    if (score > 1.0f) return 1.0f;
    if (score < 0.0f) return 0.0f;
    return score;
}

const char* classify(float score, float missing_sample_rate) {
    if (missing_sample_rate > 0.05f) return "degraded";
    if (score >= 0.75f) return "fault";
    if (score >= 0.45f) return "warning";
    return "normal";
}

int main(void) {
    EdgeFeatures features = {0.62f, 0.81f, 3.4f, 0.72f, 0.22f, 0.35f, 0.01f};
    float score = mock_event_score(features);
    const char* label = classify(score, features.missing_sample_rate);

    printf("Event score: %.2f\n", score);
    printf("Event state: %s\n", label);
    printf("Model version: edge-event-0.1.0\n");

    return 0;
}
