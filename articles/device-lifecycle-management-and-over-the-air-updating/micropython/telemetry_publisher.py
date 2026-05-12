"""
MicroPython telemetry publisher scaffold.

This file formats telemetry records. In a real deployment, publish_telemetry()
could send data through MQTT, HTTP, LoRaWAN, BLE, serial, or a gateway protocol.
"""

def make_telemetry(device_id, metric, value, unit, quality_flag, firmware_version, config_version):
    return {
        "device_id": device_id,
        "metric": metric,
        "value": value,
        "unit": unit,
        "quality_flag": quality_flag,
        "firmware_version": firmware_version,
        "configuration_version": config_version,
    }


def publish_telemetry(record):
    print("Telemetry record:")
    print(record)
