from local_control import read_speed_rpm, estimate_speed, compute_command, safety_filter
from telemetry_publisher import make_control_event, publish_event

DEVICE_ID = "embedded-control-node-001"

setpoint = 1200.0
previous_estimate = 1000.0

measurement = read_speed_rpm()
estimate = estimate_speed(previous_estimate, measurement)
candidate, error = compute_command(setpoint, estimate)
filtered, reason = safety_filter(candidate)

event = make_control_event(
    device_id=DEVICE_ID,
    setpoint=setpoint,
    measurement=measurement,
    estimate=estimate,
    error=error,
    candidate=candidate,
    filtered=filtered,
    reason=reason
)

publish_event(event)
