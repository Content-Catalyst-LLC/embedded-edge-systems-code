/*
 * TinyML Example: Update-Gating Stub for Constrained Inference Devices
 *
 * This stub shows how a constrained inference device might block model update
 * activation if battery, rollback, or compatibility conditions are not met.
 */

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    float battery_percent;
    bool rollback_ready;
    bool model_schema_compatible;
    bool signature_valid;
} UpdateGate;

bool allow_model_update(UpdateGate gate) {
    return gate.battery_percent >= 40.0f &&
           gate.rollback_ready &&
           gate.model_schema_compatible &&
           gate.signature_valid;
}

int main(void) {
    UpdateGate gate = {52.0f, true, true, true};

    if (allow_model_update(gate)) {
        printf("TinyML model update activation: ALLOW\n");
    } else {
        printf("TinyML model update activation: HOLD\n");
    }

    return 0;
}
