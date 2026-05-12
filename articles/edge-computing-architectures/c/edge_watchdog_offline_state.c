#include <stdio.h>
#include <stdbool.h>

typedef struct {
    bool cloud_connected;
    bool gateway_connected;
    bool trusted;
    unsigned int watchdog_resets;
    unsigned int buffer_backlog;
    float cpu_utilization;
    float memory_utilization;
    float clock_drift_ms;
} EdgeHealth;

typedef enum { MODE_NORMAL, MODE_DEGRADED, MODE_FAIL_SAFE, MODE_FAIL_OPERATIONAL } EdgeMode;

EdgeMode evaluate_mode(EdgeHealth h) {
    if (!h.trusted) return MODE_FAIL_SAFE;
    if (!h.cloud_connected && h.gateway_connected) return MODE_FAIL_OPERATIONAL;
    if (h.watchdog_resets > 1 || h.buffer_backlog > 250 || h.cpu_utilization > 0.85f ||
        h.memory_utilization > 0.85f || h.clock_drift_ms > 50.0f) return MODE_DEGRADED;
    return MODE_NORMAL;
}

const char* mode_name(EdgeMode m) {
    switch (m) {
        case MODE_NORMAL: return "normal";
        case MODE_DEGRADED: return "degraded";
        case MODE_FAIL_SAFE: return "fail_safe";
        case MODE_FAIL_OPERATIONAL: return "fail_operational";
        default: return "unknown";
    }
}

int main(void) {
    EdgeHealth h = {false, true, true, 0, 160, 0.65f, 0.58f, 12.0f};
    printf("Edge mode: %s\n", mode_name(evaluate_mode(h)));
    return 0;
}
