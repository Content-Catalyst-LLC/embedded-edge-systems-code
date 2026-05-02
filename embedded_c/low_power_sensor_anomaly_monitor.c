/*
 * Low-Power Sensor Anomaly Monitor
 * --------------------------------
 *
 * Firmware-style example:
 * - sample a sensor
 * - maintain a rolling average
 * - detect anomalies locally
 * - trigger a local alert
 *
 * Replace placeholder functions with hardware-specific ADC, GPIO, sleep,
 * timer, or communication functions.
 */

#include <stdio.h>
#include <stdbool.h>

#define WINDOW_SIZE 8
#define ANOMALY_THRESHOLD 12.0f

static float samples[WINDOW_SIZE];
static int sample_index = 0;
static bool buffer_full = false;

float read_sensor_value(void) {
    static float synthetic_value = 25.0f;
    synthetic_value += 0.7f;
    return synthetic_value;
}

void add_sample(float value) {
    samples[sample_index] = value;
    sample_index++;

    if (sample_index >= WINDOW_SIZE) {
        sample_index = 0;
        buffer_full = true;
    }
}

float rolling_average(void) {
    int count = buffer_full ? WINDOW_SIZE : sample_index;

    if (count == 0) {
        return 0.0f;
    }

    float total = 0.0f;

    for (int i = 0; i < count; i++) {
        total += samples[i];
    }

    return total / count;
}

bool is_anomaly(float current_value, float average_value) {
    float difference = current_value - average_value;

    if (difference < 0.0f) {
        difference = -difference;
    }

    return difference > ANOMALY_THRESHOLD;
}

void trigger_local_alert(float value, float average) {
    printf("ALERT: value=%0.2f rolling_average=%0.2f\n", value, average);
}

int main(void) {
    for (int cycle = 0; cycle < 20; cycle++) {
        float value = read_sensor_value();
        float average = rolling_average();

        if (buffer_full && is_anomaly(value, average)) {
            trigger_local_alert(value, average);
        }

        add_sample(value);
    }

    return 0;
}
