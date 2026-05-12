def make_security_event(device_id, firmware_version, config_version, trust_state):
    return {
        "device_id": device_id,
        "event_type": "trust_state_report",
        "firmware_version": firmware_version,
        "configuration_version": config_version,
        "trust_state": trust_state
    }


def publish_event(record):
    print("Security telemetry:")
    print(record)
