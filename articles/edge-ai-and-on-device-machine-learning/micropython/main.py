from local_features import rms, peak, classify

DEVICE_ID = "dev-ai-001"
MODEL_VERSION = "model-1.2"
FEATURE_VERSION = "features-1.0"

window = [0.1, 0.2, 0.5, 0.8, 0.7, 0.4, 0.2, 0.1]
features = {
    "rms": rms(window),
    "peak": peak(window)
}

predicted_class, confidence, action = classify(features)

event = {
    "device_id": DEVICE_ID,
    "model_version": MODEL_VERSION,
    "feature_version": FEATURE_VERSION,
    "features": features,
    "predicted_class": predicted_class,
    "confidence": confidence,
    "action": action
}

print(event)
