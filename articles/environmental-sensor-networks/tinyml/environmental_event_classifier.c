#include <stdio.h>

const char* classify_event(float value, float previous_value, float battery_v) {
    float delta = value - previous_value;
    if (battery_v < 11.2f) return "sensor_quality_warning";
    if (delta > 15.0f) return "event_candidate";
    return "baseline";
}

int main(void) {
    printf("%s\n", classify_event(38.5f, 5.1f, 11.8f));
    return 0;
}
