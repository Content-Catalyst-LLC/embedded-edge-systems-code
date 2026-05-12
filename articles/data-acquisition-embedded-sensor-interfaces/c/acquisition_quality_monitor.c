#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
    uint16_t raw_code;
    float value;
    float timestamp_jitter_ms;
    uint16_t buffer_age_ms;
    uint8_t bus_retries;
    bool adc_overrun;
    bool stale_read;
} measurement_t;

typedef enum {
    MEASUREMENT_VALID = 0,
    MEASUREMENT_WARN = 1,
    MEASUREMENT_INVALID = 2
} quality_t;

quality_t classify_measurement(measurement_t m) {
    if (m.adc_overrun || m.stale_read || m.timestamp_jitter_ms > 20.0f) {
        return MEASUREMENT_INVALID;
    }
    if (m.timestamp_jitter_ms > 5.0f || m.buffer_age_ms > 250 || m.bus_retries > 2) {
        return MEASUREMENT_WARN;
    }
    return MEASUREMENT_VALID;
}

int main(void) {
    measurement_t sample = {
        .raw_code = 2890,
        .value = 0.74f,
        .timestamp_jitter_ms = 9.6f,
        .buffer_age_ms = 84,
        .bus_retries = 1,
        .adc_overrun = false,
        .stale_read = false
    };

    quality_t q = classify_measurement(sample);
    printf("measurement_quality=%d\n", q);
    return (q == MEASUREMENT_INVALID) ? 1 : 0;
}
