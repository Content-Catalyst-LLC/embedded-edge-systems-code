def make_event_record(device_id, event_state, firmware_version, config_version):
    return {
        "device_id": device_id,
        "output_type": event_state,
        "privacy_transform": "local_reduction",
        "raw_value_transferred": False,
        "firmware_version": firmware_version,
        "configuration_version": config_version,
    }


def publish_event(record):
    print("Privacy-preserving event:")
    print(record)
