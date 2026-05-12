# Worked Example: MCU vs SoC Choice for an Environmental Gateway

A field deployment needs low-power sensing nodes and a local gateway. The sensing nodes require deterministic sampling, sleep residency, ADC precision, and long battery life. The gateway requires protocol translation, secure connectivity, local buffering, and occasional edge inference.

The engineering review checks:

- compute headroom for each device class
- memory margin after buffers, logs, and update slots
- required ADC, timer, DMA, UART, SPI, I2C, Ethernet, radio, and storage interfaces
- pin and package conflicts
- bus and memory-bandwidth pressure
- wake latency and sleep-current behavior
- secure boot and update requirements
- debug policy and provisioning
- SDK maturity and long-term support
- diagnostic evidence after reset, update, and field failure

The likely answer is not one universal chip. It may be a low-power MCU for sensor nodes and a richer SoC for the gateway.
