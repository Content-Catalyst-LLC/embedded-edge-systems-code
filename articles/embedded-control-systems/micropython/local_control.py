try:
    import random
except ImportError:
    random = None


def read_speed_rpm():
    if random is None:
        return 1080.0
    return 1080.0 + random.uniform(-25.0, 25.0)


def estimate_speed(previous_estimate, measurement, alpha=0.25):
    return alpha * measurement + (1.0 - alpha) * previous_estimate


def compute_command(setpoint, estimate, kp=0.0025):
    error = setpoint - estimate
    candidate = kp * error
    return candidate, error


def safety_filter(candidate, temperature_c=45.0, deadline_missed=False):
    if deadline_missed:
        return 0.0, "deadline_miss_safe_stop"
    if temperature_c >= 80.0:
        return 0.0, "thermal_fault_safe_stop"
    if temperature_c >= 70.0:
        return min(max(candidate, 0.0), 0.75), "thermal_derate"
    filtered = min(max(candidate, 0.0), 1.0)
    reason = "allowed" if filtered == candidate else "command_clipped"
    return filtered, reason
