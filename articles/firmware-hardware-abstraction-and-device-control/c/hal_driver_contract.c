#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef enum {
    DRIVER_OK = 0,
    DRIVER_ERR_NOT_INITIALIZED = -1,
    DRIVER_ERR_TIMEOUT = -2,
    DRIVER_ERR_INVALID_STATE = -3
} driver_status_t;

typedef enum {
    DRIVER_STATE_RESET,
    DRIVER_STATE_INITIALIZED,
    DRIVER_STATE_ACTIVE,
    DRIVER_STATE_SUSPENDED,
    DRIVER_STATE_FAULT
} driver_state_t;

typedef struct {
    driver_state_t state;
    bool isr_safe_read_cached_status;
    bool supports_suspend_resume;
    uint32_t timeout_ms;
} driver_contract_t;

driver_status_t driver_read(driver_contract_t *driver) {
    if (driver->state == DRIVER_STATE_RESET) {
        return DRIVER_ERR_NOT_INITIALIZED;
    }
    if (driver->state == DRIVER_STATE_SUSPENDED) {
        return DRIVER_ERR_INVALID_STATE;
    }
    return DRIVER_OK;
}

int main(void) {
    driver_contract_t driver = {
        .state = DRIVER_STATE_INITIALIZED,
        .isr_safe_read_cached_status = true,
        .supports_suspend_resume = true,
        .timeout_ms = 50
    };

    printf("driver_read_status=%d\n", driver_read(&driver));
    return 0;
}
