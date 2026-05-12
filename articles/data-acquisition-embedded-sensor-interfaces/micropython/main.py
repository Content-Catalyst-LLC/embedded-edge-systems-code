# MicroPython sensor acquisition prototype.
# Replace simulated_adc_read with machine.ADC or device-specific driver calls.

import time

def simulated_adc_read():
    return 2311

def classify(raw_code, timestamp_jitter_ms=0.5, buffer_age_ms=3):
    if timestamp_jitter_ms > 20 or buffer_age_ms > 250:
        return "invalid"
    if timestamp_jitter_ms > 5:
        return "warning"
    return "valid"

while True:
    raw = simulated_adc_read()
    value = raw * 3.3 / 4095
    quality = classify(raw)
    print({"channel": "temp-01", "raw_code": raw, "voltage": value, "quality": quality})
    time.sleep(1)
