from security_state import read_security_state, classify_trust_state
from telemetry_publisher import make_security_event, publish_event

DEVICE_ID = "secure-edge-node-001"
FIRMWARE_VERSION = "0.1.0"
CONFIG_VERSION = "1.0.0"

state = read_security_state()
trust_state = classify_trust_state(state)

event = make_security_event(
    device_id=DEVICE_ID,
    firmware_version=FIRMWARE_VERSION,
    config_version=CONFIG_VERSION,
    trust_state=trust_state
)

publish_event(event)
