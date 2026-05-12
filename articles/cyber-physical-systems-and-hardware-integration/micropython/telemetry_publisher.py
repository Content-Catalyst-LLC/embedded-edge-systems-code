def make_cps_event(device_id, measurement, estimate, candidate, filtered, reason):
    return {
        "device_id": device_id,
        "measurement": measurement,
        "estimate": estimate,
        "candidate_command": candidate,
        "filtered_command": filtered,
        "safety_filter_reason": reason,
        "actuator_saturated": candidate != filtered
    }


def publish_event(event):
    print("CPS event:")
    print(event)
