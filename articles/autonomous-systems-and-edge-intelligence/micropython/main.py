from local_autonomy import read_observation, choose_candidate_action, safety_filter
from telemetry_publisher import make_autonomy_event, publish_event

DEVICE_ID = "autonomy-edge-node-001"

observation, confidence = read_observation()
candidate_action = choose_candidate_action(observation)
filtered_action = safety_filter(candidate_action, confidence)

event = make_autonomy_event(
    device_id=DEVICE_ID,
    observation=observation,
    confidence=confidence,
    candidate_action=candidate_action,
    filtered_action=filtered_action
)

publish_event(event)
