/*
 * C Example: A/B Update Slot and Rollback-State Simulation
 *
 * This example models a constrained embedded device with active and inactive
 * firmware slots. A new OTA image is staged to the inactive slot and committed
 * only after validation.
 */

#include <stdio.h>
#include <stdbool.h>

typedef enum {
    SLOT_A,
    SLOT_B
} Slot;

typedef struct {
    Slot active_slot;
    bool inactive_slot_valid;
    bool rollback_available;
    bool pending_validation;
} UpdateState;

const char* slot_name(Slot slot) {
    return slot == SLOT_A ? "A" : "B";
}

Slot inactive_slot(Slot active) {
    return active == SLOT_A ? SLOT_B : SLOT_A;
}

bool stage_update(UpdateState* state) {
    if (!state->rollback_available) {
        return false;
    }
    state->inactive_slot_valid = true;
    state->pending_validation = true;
    return true;
}

bool commit_update(UpdateState* state, bool validation_passed) {
    if (!state->pending_validation || !state->inactive_slot_valid) {
        return false;
    }
    if (!validation_passed) {
        state->pending_validation = false;
        return false;
    }
    state->active_slot = inactive_slot(state->active_slot);
    state->pending_validation = false;
    return true;
}

int main(void) {
    UpdateState device = {SLOT_A, false, true, false};

    printf("Active slot before update: %s\n", slot_name(device.active_slot));

    if (!stage_update(&device)) {
        printf("Update blocked: rollback not available.\n");
        return 1;
    }

    if (commit_update(&device, true)) {
        printf("Update committed. Active slot: %s\n", slot_name(device.active_slot));
    } else {
        printf("Update not committed. Rollback path preserved.\n");
    }

    return 0;
}
