#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
    float battery_v;
    float link_quality;
    uint16_t buffer_age_s;
    uint8_t packet_retries;
    bool calibration_expired;
    bool enclosure_intrusion;
} node_health_t;

typedef enum {
    NODE_HEALTH_NORMAL = 0,
    NODE_HEALTH_WARNING = 1,
    NODE_HEALTH_DEGRADED = 2
} node_health_state_t;

node_health_state_t classify_node_health(node_health_t h) {
    if (h.enclosure_intrusion || h.calibration_expired || h.battery_v < 11.2f) {
        return NODE_HEALTH_DEGRADED;
    }
    if (h.battery_v < 11.8f || h.link_quality < 0.60f || h.buffer_age_s > 240 || h.packet_retries > 3) {
        return NODE_HEALTH_WARNING;
    }
    return NODE_HEALTH_NORMAL;
}

int main(void) {
    node_health_t h = {
        .battery_v = 11.9f,
        .link_quality = 0.61f,
        .buffer_age_s = 260,
        .packet_retries = 3,
        .calibration_expired = true,
        .enclosure_intrusion = false
    };

    printf("node_health_state=%d\n", classify_node_health(h));
    return 0;
}
