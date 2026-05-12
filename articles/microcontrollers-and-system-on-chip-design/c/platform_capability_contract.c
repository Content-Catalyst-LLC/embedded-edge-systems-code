#include <stdbool.h>
#include <stdio.h>

typedef struct {
    const char *name;
    unsigned cpu_mhz;
    unsigned flash_kb;
    unsigned sram_kb;
    unsigned adc_channels;
    unsigned timers;
    unsigned dma_channels;
    bool secure_boot;
    bool debug_lock;
    bool low_power_sleep;
} platform_capability_t;

bool platform_meets_minimum_sensor_node_contract(platform_capability_t p) {
    return p.cpu_mhz >= 48 &&
           p.flash_kb >= 256 &&
           p.sram_kb >= 64 &&
           p.adc_channels >= 4 &&
           p.timers >= 4 &&
           p.dma_channels >= 2 &&
           p.secure_boot &&
           p.debug_lock &&
           p.low_power_sleep;
}

int main(void) {
    platform_capability_t platform = {
        .name = "low_power_mcu_a",
        .cpu_mhz = 80,
        .flash_kb = 512,
        .sram_kb = 128,
        .adc_channels = 8,
        .timers = 8,
        .dma_channels = 6,
        .secure_boot = true,
        .debug_lock = true,
        .low_power_sleep = true
    };

    printf("platform=%s sensor_node_fit=%s\n",
           platform.name,
           platform_meets_minimum_sensor_node_contract(platform) ? "true" : "false");
    return 0;
}
