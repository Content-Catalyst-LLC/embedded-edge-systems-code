NODE_ID = "node-water-midstream-001"
SITE_ID = "site-water"
COVERAGE_ZONE = "zone-midstream"
GATEWAY_ID = "gw-water-001"

sequence_number = 201
clock_skew_ms = 12
queue_depth = 20
queue_capacity = 1000
quality_state = "valid"
calibration_state = "valid"

payload = {
    "node_id": NODE_ID,
    "site_id": SITE_ID,
    "coverage_zone": COVERAGE_ZONE,
    "gateway_id": GATEWAY_ID,
    "event_id": "evt-local-201",
    "event_time": "device-clock-placeholder",
    "value": 7.4,
    "unit": "pH",
    "quality_state": quality_state,
    "calibration_state": calibration_state,
    "clock_skew_ms": clock_skew_ms,
    "sequence_number": sequence_number,
    "idempotency_key": NODE_ID + "-" + str(sequence_number),
    "queue_depth": queue_depth,
    "queue_capacity": queue_capacity,
}

print(payload)
