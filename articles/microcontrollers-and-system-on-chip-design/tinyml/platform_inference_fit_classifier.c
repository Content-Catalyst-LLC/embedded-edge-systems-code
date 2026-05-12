#include <stdio.h>
#include <stdbool.h>

const char* classify_platform_inference_fit(
    int cpu_mhz,
    int sram_kb,
    bool accelerator_present,
    int bandwidth_mb_s,
    int active_ma
) {
    if (!accelerator_present && cpu_mhz < 400) return "not_fit";
    if (sram_kb < 512) return "prototype_only";
    if (bandwidth_mb_s < 500) return "prototype_only";
    if (active_ma > 300) return "prototype_only";
    return "field_ready";
}

int main(void) {
    printf("%s\n", classify_platform_inference_fit(600, 768, true, 900, 120));
    return 0;
}
