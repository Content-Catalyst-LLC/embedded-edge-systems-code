SENSOR_ID = "temp-001"
CALIBRATION_VERSION = "cal-2026-01"
FIRMWARE_VERSION = "fw-1.0"

gain = 36.5
offset = -10.0
raw_value = 1.20
valid_min = 0.0
valid_max = 120.0
calibration_expired = False
coefficient_mismatch = False
lineage_complete = True
traceability_complete = True

calibrated_value = gain * raw_value + offset

quality_flags = []
if calibration_expired:
    quality_flags.append("calibration_expired")
if coefficient_mismatch:
    quality_flags.append("coefficient_mismatch")
if calibrated_value < valid_min or calibrated_value > valid_max:
    quality_flags.append("out_of_range")
if not lineage_complete:
    quality_flags.append("lineage_incomplete")
if not traceability_complete:
    quality_flags.append("traceability_incomplete")

heartbeat = {
    "sensor_id": SENSOR_ID,
    "calibration_version": CALIBRATION_VERSION,
    "firmware_version": FIRMWARE_VERSION,
    "calibrated_value": calibrated_value,
    "quality_flags": quality_flags or ["valid"],
}

print(heartbeat)
