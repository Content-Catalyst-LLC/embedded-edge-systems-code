# MicroPython device-control prototype.
# Replace simulated functions with board-specific I2C/SPI/GPIO APIs.

import time

class DeviceDriver:
    RESET = "reset"
    INIT = "init"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    FAULT = "fault"

    def __init__(self, name):
        self.name = name
        self.state = self.RESET
        self.error_count = 0

    def init(self):
        self.state = self.INIT
        return True

    def read(self):
        if self.state in (self.RESET, self.SUSPENDED):
            self.error_count += 1
            return {"result": "invalid_state", "driver": self.name}
        self.state = self.ACTIVE
        return {"result": "ok", "driver": self.name, "value": 21.4}

    def suspend(self):
        self.state = self.SUSPENDED

    def resume(self):
        self.state = self.ACTIVE

driver = DeviceDriver("example_sensor")
driver.init()

while True:
    print(driver.read())
    driver.suspend()
    time.sleep(5)
    driver.resume()
