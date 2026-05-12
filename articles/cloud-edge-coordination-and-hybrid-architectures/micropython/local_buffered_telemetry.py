try:
    import time
except ImportError:
    time = None


BUFFER = []


def authority_valid(cloud_reachable, offline_duration_s, authority_window_s=300):
    return cloud_reachable or offline_duration_s <= authority_window_s


def make_event(device_id, gateway_id, measurement, edge_policy_version, edge_model_version, cloud_reachable, offline_duration_s):
    return {
        "device_id": device_id,
        "gateway_id": gateway_id,
        "measurement": measurement,
        "edge_policy_version": edge_policy_version,
        "edge_model_version": edge_model_version,
        "cloud_reachable": cloud_reachable,
        "offline_duration_s": offline_duration_s,
        "authority_valid": authority_valid(cloud_reachable, offline_duration_s)
    }


def buffer_event(event):
    BUFFER.append(event)
    return len(BUFFER)


def flush_buffer():
    while BUFFER:
        event = BUFFER.pop(0)
        print("uplink:", event)
