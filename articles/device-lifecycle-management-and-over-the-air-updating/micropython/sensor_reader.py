"""
MicroPython sensor reader scaffold.

Replace the mock reading with a real sensor driver for the target board.
"""

try:
    import random
except ImportError:
    random = None


def read_sensor_value():
    """Return a mock normalized sensor value."""
    if random is None:
        return 0.42
    return round(random.uniform(0.0, 1.0), 3)


def quality_flag(value):
    """Assign a simple telemetry quality flag."""
    if value >= 0.90:
        return "warning"
    if value <= 0.05:
        return "low-signal"
    return "good"
