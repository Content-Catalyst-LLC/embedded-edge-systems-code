#include <stdbool.h>
#include <stdio.h>

typedef struct {
    bool critical_task_idle;
    bool sensor_ready_to_suspend;
    bool radio_idle;
    bool storage_write_pending;
    bool retained_state_valid;
    bool battery_above_storage_threshold;
} power_context_t;

bool can_enter_sleep(power_context_t ctx) {
    return ctx.critical_task_idle &&
           ctx.sensor_ready_to_suspend &&
           ctx.radio_idle &&
           !ctx.storage_write_pending &&
           ctx.retained_state_valid &&
           ctx.battery_above_storage_threshold;
}

int main(void) {
    power_context_t ctx = {
        .critical_task_idle = true,
        .sensor_ready_to_suspend = true,
        .radio_idle = true,
        .storage_write_pending = false,
        .retained_state_valid = true,
        .battery_above_storage_threshold = true
    };

    printf("can_enter_sleep=%s\n", can_enter_sleep(ctx) ? "true" : "false");
    return 0;
}
