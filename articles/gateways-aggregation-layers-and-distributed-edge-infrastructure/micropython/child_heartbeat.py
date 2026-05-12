try:
    import time
except ImportError:
    time = None


def now_seconds():
    if time is None:
        return 0
    try:
        return time.time()
    except Exception:
        return 0


def make_heartbeat(device_id, gateway_id, firmware_version, quality_flag="valid"):
    return {
        "device_id": device_id,
        "gateway_id": gateway_id,
        "firmware_version": firmware_version,
        "local_acquisition_time_s": now_seconds(),
        "quality_flag": quality_flag,
        "heartbeat": True
    }


def make_measurement(device_id, gateway_id, measurement, unit, quality_flag="valid"):
    return {
        "device_id": device_id,
        "gateway_id": gateway_id,
        "measurement": measurement,
        "unit": unit,
        "quality_flag": quality_flag,
        "local_acquisition_time_s": now_seconds()
    }
