# MicroPython environmental field-node prototype.
# Replace simulated reads with machine.ADC, I2C/SPI drivers, and radio uplink code.

import time

NODE_ID = "node-prototype-001"
BASELINE_INTERVAL_S = 900
EVENT_INTERVAL_S = 60

def read_turbidity_ntu():
    return 5.2

def read_battery_v():
    return 12.3

def classify_quality(value, battery_v):
    if battery_v < 11.2:
        return "degraded"
    if value < 0:
        return "invalid"
    return "valid"

while True:
    turbidity = read_turbidity_ntu()
    battery_v = read_battery_v()
    quality = classify_quality(turbidity, battery_v)
    event_mode = turbidity > 18.0

    payload = {
        "node_id": NODE_ID,
        "parameter": "turbidity",
        "units": "ntu",
        "value": turbidity,
        "battery_v": battery_v,
        "quality": quality,
        "event_mode": event_mode
    }
    print(payload)

    time.sleep(EVENT_INTERVAL_S if event_mode else BASELINE_INTERVAL_S)
