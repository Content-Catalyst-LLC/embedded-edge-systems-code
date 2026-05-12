try:
    import random
except ImportError:
    random = None


def read_position():
    if random is None:
        return 0.42
    return round(random.uniform(0.35, 0.45), 3)


def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


def compute_command(reference, measured, kp=4.0, command_limit=1.0):
    error = reference - measured
    raw = kp * error
    command = clamp(raw, -command_limit, command_limit)
    saturated = command != raw
    return command, error, saturated
