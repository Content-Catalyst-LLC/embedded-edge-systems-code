#include <stdio.h>

const char* classify_reliability(float reset_rate, int watchdog_count, int brownout_count) {
    if (watchdog_count >= 3 || brownout_count >= 3) return "escalate";
    if (reset_rate > 0.05f || watchdog_count > 0) return "degraded";
    return "normal";
}

int main(void) {
    printf("%s\n", classify_reliability(0.10f, 3, 0));
    return 0;
}
