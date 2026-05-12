#include <stdio.h>

typedef struct {
    float heartbeat_age_seconds;
    float expected_reporting_interval_seconds;
    float clock_skew_ms;
    float battery_percent;
    float queue_pressure;
    float signal_quality;
    int calibration_valid;
} MonitoringFeatures;

const char* classify(MonitoringFeatures x) {
    if (x.heartbeat_age_seconds > 2.0f * x.expected_reporting_interval_seconds) return "observed_stale";
    if (x.clock_skew_ms > 1000.0f || x.clock_skew_ms < -1000.0f) return "sync_degraded";
    if (!x.calibration_valid) return "observed_low_confidence";
    if (x.battery_percent < 15.0f || x.queue_pressure > 0.80f || x.signal_quality < 0.5f) return "observed_low_confidence";
    return "observed_valid";
}

int main(void) {
    MonitoringFeatures x = {480.0f, 60.0f, 1800.0f, 76.0f, 0.02f, 0.9f, 1};
    printf("TinyML monitoring state: %s\n", classify(x));
    return 0;
}
