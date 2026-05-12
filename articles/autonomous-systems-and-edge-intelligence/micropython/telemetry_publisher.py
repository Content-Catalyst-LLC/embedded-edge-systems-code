def make_autonomy_event(device_id, observation, confidence, candidate_action, filtered_action):
    return {
        "device_id": device_id,
        "observation": observation,
        "decision_confidence": confidence,
        "candidate_action": candidate_action,
        "filtered_action": filtered_action,
        "action_type": "nominal" if candidate_action == filtered_action else "fallback"
    }


def publish_event(event):
    print("Autonomy event:")
    print(event)
