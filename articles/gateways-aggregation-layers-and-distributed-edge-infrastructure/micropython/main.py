from child_heartbeat import make_heartbeat, make_measurement

DEVICE_ID = "dev-temp-001"
GATEWAY_ID = "gw-001"
FIRMWARE_VERSION = "fw-1.2"

heartbeat = make_heartbeat(DEVICE_ID, GATEWAY_ID, FIRMWARE_VERSION)
measurement = make_measurement(DEVICE_ID, GATEWAY_ID, 41.2, "celsius")

print("heartbeat:", heartbeat)
print("measurement:", measurement)
