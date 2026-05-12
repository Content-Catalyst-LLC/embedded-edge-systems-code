from local_window_features import rms, peak, crest_factor, classify

DEVICE_ID = "edge-node-001"
FEATURE_VERSION = "features-1.0"
RULE_VERSION = "rules-1.0"

window = [0.1, 0.2, 0.5, 0.8, 0.7, 0.4, 0.2, 0.1]
features = {
    "rms": rms(window),
    "peak": peak(window),
    "crest_factor": crest_factor(window)
}

event_state, uplink_mode = classify(features, missing_sample_rate=0.01)

event = {
    "device_id": DEVICE_ID,
    "feature_version": FEATURE_VERSION,
    "rule_version": RULE_VERSION,
    "features": features,
    "event_state": event_state,
    "uplink_mode": uplink_mode
}

print(event)
