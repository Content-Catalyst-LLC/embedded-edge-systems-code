#include <stdio.h>

typedef struct {
    float expanded_uncertainty;
    float snr_db;
    float absolute_drift;
    int calibration_expired;
    int coefficient_mismatch;
    int lineage_complete;
    int traceability_complete;
} MeasurementQualityFeatures;

const char* classify(MeasurementQualityFeatures x) {
    if (x.coefficient_mismatch) return "coefficient_mismatch";
    if (x.calibration_expired) return "calibration_expired";
    if (!x.lineage_complete || !x.traceability_complete) return "lineage_or_traceability_gap";
    if (x.snr_db < 20.0f) return "low_snr";
    if (x.absolute_drift > 2.0f) return "drift_warning";
    if (x.expanded_uncertainty > 1.5f) return "high_uncertainty";
    return "valid";
}

int main(void) {
    MeasurementQualityFeatures x = {1.8f, 12.0f, 4.0f, 0, 1, 0, 0};
    printf("TinyML measurement quality state: %s\n", classify(x));
    return 0;
}
