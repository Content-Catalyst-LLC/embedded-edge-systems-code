"""
MicroPython main loop scaffold.

This example keeps the loop short and safe for local testing.
"""

from sensor_reader import read_sensor_value, quality_flag
from telemetry_publisher import make_telemetry, publish_telemetry

DEVICE_ID = "edge-node-001"
FIRMWARE_VERSION = "0.1.0"
CONFIG_VERSION = "1.0.0"

value = read_sensor_value()
flag = quality_flag(value)

record = make_telemetry(
    device_id=DEVICE_ID,
    metric="normalized_sensor_value",
    value=value,
    unit="ratio",
    quality_flag=flag,
    firmware_version=FIRMWARE_VERSION,
    config_version=CONFIG_VERSION,
)

publish_telemetry(record)
