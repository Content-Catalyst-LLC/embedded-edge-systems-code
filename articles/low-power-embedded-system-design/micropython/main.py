# MicroPython low-power duty-cycle prototype.
# Replace simulated functions with machine.deepsleep, ADC, I2C/SPI drivers, and radio APIs.

import time

LOW_BATTERY_V = 3.55
BROWNOUT_PROTECT_V = 3.30

def read_battery_v():
    return 3.72

def read_sensor_value():
    return 21.4

def transmit(payload):
    print(payload)

while True:
    battery_v = read_battery_v()

    if battery_v < BROWNOUT_PROTECT_V:
        print({"mode": "brownout_protection", "battery_v": battery_v})
        time.sleep(3600)
        continue

    if battery_v < LOW_BATTERY_V:
        transmit({"mode": "low_energy_heartbeat", "battery_v": battery_v})
        time.sleep(3600)
        continue

    value = read_sensor_value()
    transmit({"mode": "normal", "battery_v": battery_v, "measurement": value})
    time.sleep(900)
