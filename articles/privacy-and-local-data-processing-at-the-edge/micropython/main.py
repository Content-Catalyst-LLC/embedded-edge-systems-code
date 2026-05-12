from sensor_reader import read_person_revealing_signal, reduce_to_event
from telemetry_publisher import make_event_record, publish_event

DEVICE_ID = "privacy-edge-node-001"
FIRMWARE_VERSION = "0.1.0"
CONFIG_VERSION = "1.0.0"

raw_value = read_person_revealing_signal()
event_state = reduce_to_event(raw_value)

record = make_event_record(
    device_id=DEVICE_ID,
    event_state=event_state,
    firmware_version=FIRMWARE_VERSION,
    config_version=CONFIG_VERSION,
)

publish_event(record)
