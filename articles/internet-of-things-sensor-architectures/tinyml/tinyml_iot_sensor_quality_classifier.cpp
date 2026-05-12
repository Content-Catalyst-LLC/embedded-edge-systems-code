#include <stdio.h>

typedef struct {
    float battery_percent;
    float queue_pressure;
    float heartbeat_age_seconds;
    float signal_quality;
    int trust_verified;
    int firmware_compliant;
    int configuration_compliant;
} LocalQualityFeatures;

const char* classify(LocalQualityFeatures x) {
    if (!x.trust_verified) return "untrusted";
    if (!x.firmware_compliant || !x.configuration_compliant) return "lifecycle_risk";
    if (x.heartbeat_age_seconds > 300.0f) return "stale";
    if (x.queue_pressure > 0.80f) return "queue_pressure";
    if (x.battery_percent < 20.0f || x.signal_quality < 0.50f) return "low_confidence";
    return "valid";
}

int main(void) {
    LocalQualityFeatures x = {18.0f, 0.65f, 1800.0f, 0.45f, 1, 1, 0};
    printf("TinyML local quality state: %s\n", classify(x));
    return 0;
}
