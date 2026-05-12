#include <stdio.h>

typedef struct {
    float proximity_min_m;
    float depth_obstacle_score;
    float motion_context_score;
} AutonomyFeatures;

typedef struct {
    const char* label;
    float confidence;
} Classification;

Classification mock_classify(AutonomyFeatures x) {
    if (x.proximity_min_m < 0.5f || x.depth_obstacle_score > 0.80f) {
        Classification result = {"hazard", 0.66f};
        return result;
    }

    if (x.proximity_min_m < 1.2f || x.depth_obstacle_score > 0.45f) {
        Classification result = {"obstacle", 0.82f};
        return result;
    }

    Classification result = {"clear", 0.91f};
    return result;
}

const char* safety_filter(const char* label, float confidence) {
    if (confidence < 0.65f) return "safe_stop";
    if (confidence < 0.75f) return "pause_and_request_review";
    if (label[0] == 'h') return "pause_and_request_review";
    if (label[0] == 'o') return "reroute";
    return "continue";
}

int main(void) {
    AutonomyFeatures features = {0.9f, 0.55f, 0.20f};
    Classification result = mock_classify(features);

    printf("TinyML label: %s\n", result.label);
    printf("Confidence: %.2f\n", result.confidence);
    printf("Filtered action: %s\n", safety_filter(result.label, result.confidence));

    return 0;
}
