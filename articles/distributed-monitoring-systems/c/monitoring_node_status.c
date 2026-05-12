#include <stdio.h>
#include <stdbool.h>

typedef enum {
    NODE_OBSERVED_VALID,
    NODE_LOW_CONFIDENCE,
    NODE_STALE,
    NODE_SYNC_DEGRADED,
    NODE_VISIBILITY_LOST
} NodeMonitoringState;

typedef struct {
    bool online;
    bool healthy;
    bool calibration_valid;
    unsigned int heartbeat_age_seconds;
    unsigned int expected_interval_seconds;
    int clock_skew_ms;
    unsigned int queue_depth;
    unsigned int queue_capacity;
} NodeStatus;

NodeMonitoringState evaluate_node(NodeStatus s) {
    if (!s.online || !s.healthy) return NODE_VISIBILITY_LOST;
    if (!s.calibration_valid) return NODE_LOW_CONFIDENCE;
    if (s.heartbeat_age_seconds > 2 * s.expected_interval_seconds) return NODE_STALE;
    if (s.clock_skew_ms > 1000 || s.clock_skew_ms < -1000) return NODE_SYNC_DEGRADED;
    if (((float)s.queue_depth / (float)s.queue_capacity) > 0.80f) return NODE_LOW_CONFIDENCE;
    return NODE_OBSERVED_VALID;
}

const char* state_name(NodeMonitoringState state) {
    switch(state) {
        case NODE_OBSERVED_VALID: return "observed_valid";
        case NODE_LOW_CONFIDENCE: return "observed_low_confidence";
        case NODE_STALE: return "observed_stale";
        case NODE_SYNC_DEGRADED: return "sync_degraded";
        case NODE_VISIBILITY_LOST: return "visibility_lost";
        default: return "unknown";
    }
}

int main(void) {
    NodeStatus node = {true, true, true, 45, 60, 12, 20, 1000};
    printf("Monitoring node state: %s\n", state_name(evaluate_node(node)));
    return 0;
}
