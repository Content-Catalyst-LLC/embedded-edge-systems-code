from local_buffered_telemetry import make_event, buffer_event, flush_buffer

DEVICE_ID = "hybrid-edge-device-001"
GATEWAY_ID = "gw-001"

event = make_event(
    device_id=DEVICE_ID,
    gateway_id=GATEWAY_ID,
    measurement=42.0,
    edge_policy_version="policy-1.0",
    edge_model_version="model-2.0",
    cloud_reachable=False,
    offline_duration_s=240
)

backlog = buffer_event(event)
print("buffer backlog:", backlog)

flush_buffer()
