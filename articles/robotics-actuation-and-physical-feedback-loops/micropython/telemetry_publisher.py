def make_control_event(device_id, reference, measured, command, error, saturated):
    return {
        "device_id": device_id,
        "reference_position": reference,
        "measured_position": measured,
        "tracking_error": error,
        "command": command,
        "saturated": saturated,
    }


def publish_event(event):
    print("Robotics feedback event:")
    print(event)
