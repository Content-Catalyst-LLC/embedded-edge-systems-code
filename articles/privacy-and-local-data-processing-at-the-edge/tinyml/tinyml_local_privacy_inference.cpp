#include <stdio.h>

typedef struct {
    float signal_value;
    float context_score;
} FeatureVector;

float mock_privacy_event_score(FeatureVector features) {
    float score = (0.7f * features.signal_value) + (0.3f * features.context_score);
    if (score > 1.0f) return 1.0f;
    if (score < 0.0f) return 0.0f;
    return score;
}

const char* event_label(float score) {
    if (score > 0.80f) return "event_high";
    if (score > 0.50f) return "event_medium";
    return "event_low";
}

int main(void) {
    FeatureVector features = {0.88f, 0.62f};
    float score = mock_privacy_event_score(features);

    printf("Local-only TinyML event label: %s\n", event_label(score));
    printf("Raw input transferred: false\n");

    return 0;
}
