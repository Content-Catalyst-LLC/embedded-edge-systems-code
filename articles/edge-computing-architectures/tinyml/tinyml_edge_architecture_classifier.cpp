#include <stdio.h>

typedef struct {
    float latency_ms;
    float buffer_backlog;
    float cpu_utilization;
    float memory_utilization;
    float watchdog_resets;
    float clock_drift_ms;
    int trusted;
    int cloud_connected;
    int gateway_connected;
} EdgeRuntimeFeatures;

const char* classify(EdgeRuntimeFeatures x) {
    if (!x.trusted) return "fail_safe";
    if (!x.cloud_connected && x.gateway_connected) return "fail_operational";
    if (x.latency_ms > 100.0f || x.buffer_backlog > 250.0f || x.cpu_utilization > 0.85f ||
        x.memory_utilization > 0.85f || x.watchdog_resets > 1.0f || x.clock_drift_ms > 50.0f) return "degraded";
    return "normal";
}

int main(void) {
    EdgeRuntimeFeatures x = {140.0f, 260.0f, 0.88f, 0.79f, 2.0f, 46.0f, 1, 0, 1};
    printf("TinyML edge architecture mode: %s\n", classify(x));
    return 0;
}
