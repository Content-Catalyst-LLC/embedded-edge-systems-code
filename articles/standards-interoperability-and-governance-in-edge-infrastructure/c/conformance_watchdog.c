/*
 * C Example: Conformance Watchdog for Constrained Edge Systems
 *
 * This example simulates a constrained device checking whether a local
 * profile remains inside a governance threshold before reporting itself as
 * operationally conformant.
 */

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    float protocol_conformance;
    float semantic_alignment;
    float lifecycle_control;
    float security_baseline;
    float operational_accountability;
    float unmanaged_divergence;
} GovernanceProfile;

float governance_score(GovernanceProfile profile) {
    float score =
        0.20f * profile.protocol_conformance +
        0.20f * profile.semantic_alignment +
        0.20f * profile.lifecycle_control +
        0.20f * profile.security_baseline +
        0.15f * profile.operational_accountability -
        0.15f * profile.unmanaged_divergence;

    if (score < 0.0f) return 0.0f;
    if (score > 1.0f) return 1.0f;
    return score;
}

bool is_conformant(GovernanceProfile profile) {
    return governance_score(profile) >= 0.70f;
}

int main(void) {
    GovernanceProfile gateway = {0.92f, 0.88f, 0.84f, 0.90f, 0.86f, 0.10f};
    float score = governance_score(gateway);

    printf("Governance score: %.3f\n", score);
    printf("Conformance status: %s\n", is_conformant(gateway) ? "PASS" : "REVIEW");

    return 0;
}
