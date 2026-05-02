"""
Gateway Event Simulation
------------------------

Simulates edge gateway events from multiple devices.
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone


def make_gateway_event(device_id: str, sensor_type: str) -> dict:
    """Create a synthetic gateway event."""

    return {
        "device_id": device_id,
        "sensor_type": sensor_type,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "observed_value": round(random.uniform(0.0, 100.0), 3),
        "battery_voltage": round(random.uniform(3.3, 4.1), 3),
        "signal_quality": round(random.uniform(0.70, 1.0), 3),
    }


def main() -> None:
    devices = [
        ("EDGE-001", "temperature"),
        ("EDGE-002", "vibration"),
        ("EDGE-003", "moisture"),
    ]

    events = [make_gateway_event(device_id, sensor_type) for device_id, sensor_type in devices]

    print(json.dumps(events, indent=2))


if __name__ == "__main__":
    main()
