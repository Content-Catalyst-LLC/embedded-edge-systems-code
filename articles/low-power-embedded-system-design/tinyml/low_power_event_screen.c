#include <stdio.h>

const char* classify_low_power_event(float sensor_delta, float battery_v, int false_wakes) {
    if (battery_v < 3.45f) return "low_energy_defer";
    if (false_wakes > 10) return "sleep_continue";
    if (sensor_delta > 5.0f) return "transmit_now";
    if (sensor_delta > 1.0f) return "sample_now";
    return "sleep_continue";
}

int main(void) {
    printf("%s\n", classify_low_power_event(6.2f, 3.72f, 2));
    return 0;
}
