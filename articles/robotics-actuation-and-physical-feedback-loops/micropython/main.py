from servo_feedback import read_position, compute_command
from telemetry_publisher import make_control_event, publish_event

DEVICE_ID = "robotics-edge-node-001"

reference = 0.50
measured = read_position()
command, error, saturated = compute_command(reference, measured)

event = make_control_event(
    device_id=DEVICE_ID,
    reference=reference,
    measured=measured,
    command=command,
    error=error,
    saturated=saturated
)

publish_event(event)
