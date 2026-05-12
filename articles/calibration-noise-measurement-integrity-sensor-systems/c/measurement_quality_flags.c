#include <stdio.h>
#include <stdbool.h>

typedef enum {
    QUALITY_VALID,
    QUALITY_CALIBRATION_EXPIRED,
    QUALITY_COEFFICIENT_MISMATCH,
    QUALITY_LOW_SNR,
    QUALITY_DRIFT_WARNING,
    QUALITY_OUT_OF_RANGE,
    QUALITY_SATURATED
} QualityState;

typedef struct {
    float raw_value;
    float gain;
    float offset;
    float reference_value;
    float valid_min;
    float valid_max;
    float signal_rms;
    float noise_rms;
    bool calibration_expired;
    bool coefficient_mismatch;
    bool saturated;
} MeasurementInput;

float calibrate(float raw, float gain, float offset) {
    return gain * raw + offset;
}

QualityState evaluate_quality(MeasurementInput x) {
    float calibrated = calibrate(x.raw_value, x.gain, x.offset);
    float snr_ratio = x.noise_rms > 0.0f ? x.signal_rms / x.noise_rms : 9999.0f;
    float drift = calibrated - x.reference_value;

    if (x.coefficient_mismatch) return QUALITY_COEFFICIENT_MISMATCH;
    if (x.calibration_expired) return QUALITY_CALIBRATION_EXPIRED;
    if (x.saturated) return QUALITY_SATURATED;
    if (snr_ratio < 10.0f) return QUALITY_LOW_SNR;
    if (drift > 2.0f || drift < -2.0f) return QUALITY_DRIFT_WARNING;
    if (calibrated < x.valid_min || calibrated > x.valid_max) return QUALITY_OUT_OF_RANGE;
    return QUALITY_VALID;
}

const char* quality_name(QualityState q) {
    switch(q) {
        case QUALITY_VALID: return "valid";
        case QUALITY_CALIBRATION_EXPIRED: return "calibration_expired";
        case QUALITY_COEFFICIENT_MISMATCH: return "coefficient_mismatch";
        case QUALITY_LOW_SNR: return "low_snr";
        case QUALITY_DRIFT_WARNING: return "drift_warning";
        case QUALITY_OUT_OF_RANGE: return "out_of_range";
        case QUALITY_SATURATED: return "saturated";
        default: return "unknown";
    }
}

int main(void) {
    MeasurementInput input = {1.2f, 36.5f, -10.0f, 35.0f, 0.0f, 120.0f, 1.0f, 0.05f, false, false, false};
    float calibrated = calibrate(input.raw_value, input.gain, input.offset);
    printf("Calibrated value: %.3f\n", calibrated);
    printf("Quality state: %s\n", quality_name(evaluate_quality(input)));
    return 0;
}
