from local_cps_loop import read_sensor_speed_rpm, estimate_state, compute_candidate_command, runtime_assurance
from telemetry_publisher import make_cps_event, publish_event

DEVICE_ID = "cps-edge-node-001"

setpoint = 1200.0
previous_estimate = 1000.0

measurement = read_sensor_speed_rpm()
estimate = estimate_state(previous_estimate, measurement)
candidate = compute_candidate_command(setpoint, estimate)
filtered, reason = runtime_assurance(
    candidate=candidate,
    sensor_age_ms=1.2,
    deadline_slack_ms=0.62,
    uncertainty=24.0,
    uncertainty_budget=35.0
)

event = make_cps_event(DEVICE_ID, measurement, estimate, candidate, filtered, reason)
publish_event(event)
