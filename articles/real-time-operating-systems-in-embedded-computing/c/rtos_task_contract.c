#include <stdbool.h>
#include <stdio.h>

typedef enum {
    CRITICALITY_HARD,
    CRITICALITY_FIRM,
    CRITICALITY_SOFT,
    CRITICALITY_BEST_EFFORT
} criticality_t;

typedef struct {
    const char *name;
    criticality_t criticality;
    unsigned priority;
    unsigned period_ms;
    unsigned deadline_ms;
    unsigned wcet_ms;
    unsigned blocking_ms;
    unsigned stack_bytes;
    bool watchdog_required;
} rtos_task_contract_t;

bool task_contract_has_timing_risk(rtos_task_contract_t task) {
    unsigned response = task.wcet_ms + task.blocking_ms;
    return response > task.deadline_ms;
}

int main(void) {
    rtos_task_contract_t control = {
        .name = "control_loop",
        .criticality = CRITICALITY_HARD,
        .priority = 1,
        .period_ms = 20,
        .deadline_ms = 20,
        .wcet_ms = 4,
        .blocking_ms = 1,
        .stack_bytes = 2048,
        .watchdog_required = true
    };

    printf("task=%s timing_risk=%s\n",
           control.name,
           task_contract_has_timing_risk(control) ? "true" : "false");
    return 0;
}
