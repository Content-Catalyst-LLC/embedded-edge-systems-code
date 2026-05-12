def rms(values):
    if not values:
        return 0.0
    return (sum(v * v for v in values) / len(values)) ** 0.5


def peak(values):
    if not values:
        return 0.0
    return max(abs(v) for v in values)


def crest_factor(values):
    r = rms(values)
    return peak(values) / r if r > 0 else 0.0


def classify(features, missing_sample_rate=0.0):
    if missing_sample_rate > 0.05:
        return "degraded", "immediate"

    if features["rms"] > 0.65 and features["peak"] > 0.80:
        return "fault", "immediate"

    if features["rms"] > 0.45 or features["peak"] > 0.75:
        return "warning", "immediate"

    return "normal", "sampled"
