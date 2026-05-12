def rms(values):
    if not values:
        return 0.0
    return (sum(v * v for v in values) / len(values)) ** 0.5


def peak(values):
    if not values:
        return 0.0
    return max(abs(v) for v in values)


def classify(features, confidence_threshold=0.80):
    score = 0.0
    score += 0.45 if features["rms"] > 0.55 else 0.0
    score += 0.35 if features["peak"] > 0.75 else 0.0
    confidence = min(0.98, max(0.55, score + 0.20))

    if confidence < confidence_threshold:
        return "uncertain", confidence, "fallback_more_samples"

    if score >= 0.70:
        return "fault", confidence, "local_alarm"

    if score >= 0.40:
        return "warning", confidence, "uplink_for_review"

    return "normal", confidence, "no_action"
