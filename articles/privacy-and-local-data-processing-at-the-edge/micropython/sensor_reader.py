try:
    import random
except ImportError:
    random = None


def read_person_revealing_signal():
    if random is None:
        return 0.42
    return round(random.uniform(0.0, 1.0), 3)


def reduce_to_event(value):
    if value > 0.80:
        return "event_high"
    if value > 0.50:
        return "event_medium"
    return "event_low"
