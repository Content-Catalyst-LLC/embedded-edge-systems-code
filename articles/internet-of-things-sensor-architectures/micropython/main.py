DEVICE_ID = "dev-env-001"
GATEWAY_ID = "gw-001"
SITE_ID = "site-a"
FIRMWARE_VERSION = "fw-1.0"
CONFIG_VERSION = "cfg-1.0"
SCHEMA_VERSION = "schema-1.0"

sequence_number = 101
queue_depth = 3
queue_capacity = 100
trust_state = "verified"
quality_state = "valid"
battery_percent = 84

payload = {
    "device_id": DEVICE_ID,
    "site_id": SITE_ID,
    "gateway_id": GATEWAY_ID,
    "event_id": "evt-local-101",
    "event_time": "device-clock-placeholder",
    "value": 22.4,
    "unit": "C",
    "quality_state": quality_state,
    "trust_state": trust_state,
    "sequence_number": sequence_number,
    "idempotency_key": DEVICE_ID + "-" + str(sequence_number),
    "firmware_version": FIRMWARE_VERSION,
    "configuration_version": CONFIG_VERSION,
    "schema_version": SCHEMA_VERSION,
    "queue_depth": queue_depth,
    "queue_capacity": queue_capacity,
    "battery_percent": battery_percent,
}

print(payload)
