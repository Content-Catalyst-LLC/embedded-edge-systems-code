# Firmware Notes

Firmware should preserve the distinction between:

- raw register or ADC values
- scaled engineering units
- calibrated values
- filtered values
- fused estimates
- telemetry payloads

Each stage should carry channel identity, acquisition time, calibration version, and quality flags where practical.
