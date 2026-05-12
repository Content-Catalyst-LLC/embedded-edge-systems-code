/*
 * C Example: Constrained Local Redaction and Event Filtering
 *
 * This example represents a lightweight edge-device rule that suppresses raw
 * values and reports only event states when privacy policy requires minimisation.
 */

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    float signal_value;
    bool person_revealing;
    bool allow_raw_transfer;
} LocalSignal;

const char* classify_event(float value) {
    if (value > 0.80f) {
        return "event_high";
    }
    if (value > 0.50f) {
        return "event_medium";
    }
    return "event_low";
}

int main(void) {
    LocalSignal signal = {0.86f, true, false};

    if (signal.person_revealing && !signal.allow_raw_transfer) {
        printf("Raw value suppressed. Reporting transformed event: %s\n", classify_event(signal.signal_value));
    } else {
        printf("Raw value eligible for transfer: %.2f\n", signal.signal_value);
    }

    return 0;
}
