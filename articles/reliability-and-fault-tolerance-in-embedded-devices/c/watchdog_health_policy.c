#include <stdbool.h>
#include <stdio.h>

typedef struct {
    bool critical_task_heartbeat;
    bool communication_healthy;
    bool state_valid;
    bool queue_below_threshold;
    bool persistent_state_valid;
} health_t;

bool may_service_watchdog(health_t h) {
    return h.critical_task_heartbeat &&
           h.communication_healthy &&
           h.state_valid &&
           h.queue_below_threshold &&
           h.persistent_state_valid;
}

int main(void) {
    health_t h = {
        .critical_task_heartbeat = true,
        .communication_healthy = true,
        .state_valid = true,
        .queue_below_threshold = false,
        .persistent_state_valid = true
    };

    if (may_service_watchdog(h)) {
        printf("watchdog_service_allowed=true\n");
    } else {
        printf("watchdog_service_allowed=false\n");
    }

    return 0;
}
