def make_control_event(device_id, setpoint, measurement, estimate, error, candidate, filtered, reason):
    return {
        "device_id": device_id,
        "setpoint": setpoint,
        "measurement": measurement,
        "estimate": estimate,
        "control_error": error,
        "candidate_command": candidate,
        "filtered_command": filtered,
        "safety_filter_reason": reason,
        "saturated": candidate != filtered
    }


def publish_event(event):
    print("Control event:")
    print(event)
