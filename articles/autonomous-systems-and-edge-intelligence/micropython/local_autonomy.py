try:
    import random
except ImportError:
    random = None


def read_observation():
    if random is None:
        return "obstacle", 0.82
    value = random.random()
    if value < 0.60:
        return "clear", 0.90
    if value < 0.90:
        return "obstacle", 0.82
    return "hazard", 0.66


def choose_candidate_action(observation):
    if observation == "clear":
        return "continue"
    if observation == "obstacle":
        return "reroute"
    return "proceed_slow"


def safety_filter(candidate_action, confidence):
    if confidence < 0.65:
        return "safe_stop"
    if confidence < 0.75:
        return "pause_and_request_review"
    if candidate_action == "proceed_slow":
        return "pause_and_request_review"
    return candidate_action
