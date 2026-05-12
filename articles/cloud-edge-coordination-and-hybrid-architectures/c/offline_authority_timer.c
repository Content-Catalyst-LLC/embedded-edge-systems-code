/*
 * C Example: Offline Authority Timer, Local Fallback, and Telemetry Packet Formation
 */

#include <stdio.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    char gateway_id[32];
    char policy_version[32];
    char model_version[32];
    unsigned int offline_duration_s;
    unsigned int authority_window_s;
    bool cloud_reachable;
} EdgeAuthorityContext;

typedef struct {
    char decision_type[32];
    char fallback_action[32];
    bool authority_valid;
} LocalDecision;

LocalDecision evaluate_authority(EdgeAuthorityContext context) {
    LocalDecision decision;
    strcpy(decision.decision_type, "local_anomaly_alert");
    strcpy(decision.fallback_action, "none");
    decision.authority_valid = context.cloud_reachable || context.offline_duration_s <= context.authority_window_s;

    if (!decision.authority_valid) {
        strcpy(decision.fallback_action, "degraded_mode_restrict_action");
    }

    return decision;
}

int main(void) {
    EdgeAuthorityContext context = {
        .gateway_id = "gw-002",
        .policy_version = "policy-1.0",
        .model_version = "model-2.0",
        .offline_duration_s = 520,
        .authority_window_s = 300,
        .cloud_reachable = false
    };

    LocalDecision decision = evaluate_authority(context);

    printf("Gateway: %s\n", context.gateway_id);
    printf("Policy version: %s\n", context.policy_version);
    printf("Model version: %s\n", context.model_version);
    printf("Authority valid: %s\n", decision.authority_valid ? "true" : "false");
    printf("Fallback action: %s\n", decision.fallback_action);

    return 0;
}
