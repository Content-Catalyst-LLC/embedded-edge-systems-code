#include <stdio.h>

const char* classify_rtos_timing_anomaly(
    int deadline_misses,
    int queue_overflows,
    int stack_watermark_bytes,
    int max_isr_time_us,
    float idle_residency_pct
) {
    if (deadline_misses > 0) return "deadline_risk";
    if (queue_overflows > 0) return "queue_risk";
    if (stack_watermark_bytes < 512) return "stack_risk";
    if (max_isr_time_us > 250) return "isr_risk";
    if (idle_residency_pct < 70.0f) return "power_risk";
    return "normal";
}

int main(void) {
    printf("%s\n", classify_rtos_timing_anomaly(1, 0, 768, 120, 88.5f));
    return 0;
}
