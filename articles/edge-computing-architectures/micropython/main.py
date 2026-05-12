DEVICE_ID = "edge-node-001"
FIRMWARE_VERSION = "fw-1.0"
APPROVED_VERSION = "fw-1.0"

cloud_connected = False
gateway_connected = True
trusted = True
watchdog_resets = 0
buffer_backlog = 12

def edge_mode():
    if not trusted:
        return "fail_safe"
    if not cloud_connected and gateway_connected:
        return "fail_operational"
    if watchdog_resets > 1 or buffer_backlog > 250:
        return "degraded"
    return "normal"

heartbeat = {
    "device_id": DEVICE_ID,
    "firmware_version": FIRMWARE_VERSION,
    "version_compliant": FIRMWARE_VERSION == APPROVED_VERSION,
    "edge_mode": edge_mode(),
    "buffer_backlog": buffer_backlog
}
print(heartbeat)
