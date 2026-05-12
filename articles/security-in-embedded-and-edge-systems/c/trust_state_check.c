/*
 * C Example: Constrained Trust-State Check
 *
 * This example represents a device-side security readiness check that could be
 * adapted for constrained embedded systems.
 */

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    bool secure_boot;
    bool firmware_verified;
    bool rollback_ready;
    bool debug_locked;
    bool credential_current;
} TrustState;

bool is_trusted(TrustState state) {
    return state.secure_boot &&
           state.firmware_verified &&
           state.rollback_ready &&
           state.debug_locked &&
           state.credential_current;
}

int main(void) {
    TrustState device = {
        .secure_boot = true,
        .firmware_verified = true,
        .rollback_ready = true,
        .debug_locked = true,
        .credential_current = true
    };

    printf("Device trust state: %s\n", is_trusted(device) ? "TRUSTED" : "REVIEW");
    return 0;
}
