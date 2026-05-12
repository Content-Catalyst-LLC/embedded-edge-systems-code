def read_security_state():
    return {
        "secure_boot": True,
        "firmware_verified": True,
        "rollback_ready": True,
        "debug_locked": True,
        "credential_current": True
    }


def classify_trust_state(state):
    if all(state.values()):
        return "trusted"
    return "review"
