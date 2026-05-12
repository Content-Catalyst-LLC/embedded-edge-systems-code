try:
    import random
except ImportError:
    random = None


def read_sensor_speed_rpm():
    if random is None:
        return 1080.0
    return 1080.0 + random.uniform(-20.0, 20.0)


def estimate_state(previous_estimate, measurement, alpha=0.25):
    return alpha * measurement + (1.0 - alpha) * previous_estimate


def compute_candidate_command(setpoint, estimate):
    return 0.0025 * (setpoint - estimate)


def runtime_assurance(candidate, sensor_age_ms, deadline_slack_ms, uncertainty, uncertainty_budget):
    if sensor_age_ms > 3.0:
        return 0.0, "stale_sensor_safe_stop"
    if deadline_slack_ms < 0.0:
        return 0.0, "deadline_miss_safe_stop"
    if uncertainty > uncertainty_budget:
        return min(max(candidate, 0.0), 0.5), "uncertainty_budget_violation"

    filtered = min(max(candidate, 0.0), 1.0)
    reason = "allowed" if filtered == candidate else "command_clipped"
    return filtered, reason
