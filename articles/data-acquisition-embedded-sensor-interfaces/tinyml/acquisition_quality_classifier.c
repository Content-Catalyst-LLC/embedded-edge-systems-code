#include <stdio.h>

const char* classify(float jitter_ms, float buffer_age_ms, int bus_retries) {
    if (jitter_ms > 20.0f || buffer_age_ms > 500.0f) return "invalid";
    if (jitter_ms > 5.0f || buffer_age_ms > 250.0f || bus_retries > 2) return "warning";
    return "normal";
}

int main(void) {
    printf("%s\n", classify(9.6f, 84.0f, 1));
    return 0;
}
