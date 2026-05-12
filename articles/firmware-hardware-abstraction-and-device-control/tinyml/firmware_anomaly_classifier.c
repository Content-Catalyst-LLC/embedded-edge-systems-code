#include <stdio.h>

const char* classify_firmware_anomaly(int driver_errors, int resume_failures, int rollback_count) {
    if (rollback_count > 0) return "update_risk";
    if (resume_failures > 2) return "resume_risk";
    if (driver_errors > 3) return "driver_risk";
    return "normal";
}

int main(void) {
    printf("%s\n", classify_firmware_anomaly(4, 1, 0));
    return 0;
}
