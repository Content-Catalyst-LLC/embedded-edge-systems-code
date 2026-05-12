/*
 * C Example: Constrained Autonomy Mode Selection with Confidence and Fallback Checks
 */

#include <stdio.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    float confidence;
    float latency_ms;
    float latency_budget_ms;
    float input_drift_score;
    char safety_state[16];
    char candidate_action[32];
} AutonomyDecision;

const char* filter_action(AutonomyDecision decision) {
    if (decision.latency_ms > decision.latency_budget_ms) {
        return "safe_stop";
    }

    if (strcmp(decision.safety_state, "degraded") == 0) {
        return "safe_stop";
    }

    if (decision.confidence < 0.65f) {
        return "pause_and_request_review";
    }

    if (decision.confidence < 0.75f) {
        return "pause_and_request_review";
    }

    if (decision.input_drift_score >= 0.40f) {
        return "pause_and_request_review";
    }

    if (decision.input_drift_score >= 0.25f && strcmp(decision.candidate_action, "continue") == 0) {
        return "slow_down";
    }

    return decision.candidate_action;
}

int main(void) {
    AutonomyDecision decision = {
        .confidence = 0.72f,
        .latency_ms = 61.0f,
        .latency_budget_ms = 80.0f,
        .input_drift_score = 0.16f,
        .safety_state = "normal",
        .candidate_action = "reroute"
    };

    printf("Candidate action: %s\n", decision.candidate_action);
    printf("Filtered action: %s\n", filter_action(decision));

    return 0;
}
