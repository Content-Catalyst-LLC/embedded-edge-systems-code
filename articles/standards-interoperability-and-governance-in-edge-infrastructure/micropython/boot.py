"""
MicroPython boot scaffold.

On a real device, this file can initialize network settings, mount storage,
load configuration, and prepare the device identity before main.py runs.
"""

DEVICE_ID = "edge-node-001"
CONFIG_VERSION = "1.0.0"
FIRMWARE_VERSION = "0.1.0"

print("Booting device:", DEVICE_ID)
print("Config version:", CONFIG_VERSION)
print("Firmware version:", FIRMWARE_VERSION)
