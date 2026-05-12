#include <stdio.h>
#include <stdbool.h>

#define QUEUE_CAPACITY 100

typedef struct {
    unsigned int depth;
    unsigned int capacity;
    bool trust_verified;
    bool credential_valid;
    bool local_safety_ok;
    unsigned int heartbeat_age_seconds;
} EndpointState;

typedef enum {
    ENDPOINT_OK,
    ENDPOINT_QUEUE_PRESSURE,
    ENDPOINT_UNTRUSTED,
    ENDPOINT_STALE_HEARTBEAT,
    ENDPOINT_LOCAL_SAFETY_BLOCK
} EndpointStatus;

EndpointStatus evaluate_endpoint(EndpointState s) {
    if (!s.trust_verified || !s.credential_valid) return ENDPOINT_UNTRUSTED;
    if (!s.local_safety_ok) return ENDPOINT_LOCAL_SAFETY_BLOCK;
    if (s.heartbeat_age_seconds > 300) return ENDPOINT_STALE_HEARTBEAT;
    if (((float)s.depth / (float)s.capacity) > 0.80f) return ENDPOINT_QUEUE_PRESSURE;
    return ENDPOINT_OK;
}

const char* status_name(EndpointStatus status) {
    switch(status) {
        case ENDPOINT_OK: return "ok";
        case ENDPOINT_QUEUE_PRESSURE: return "queue_pressure";
        case ENDPOINT_UNTRUSTED: return "untrusted";
        case ENDPOINT_STALE_HEARTBEAT: return "stale_heartbeat";
        case ENDPOINT_LOCAL_SAFETY_BLOCK: return "local_safety_block";
        default: return "unknown";
    }
}

int main(void) {
    EndpointState state = {85, QUEUE_CAPACITY, true, true, true, 120};
    printf("Endpoint status: %s\n", status_name(evaluate_endpoint(state)));
    return 0;
}
