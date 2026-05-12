# Worked Example: Multiplexed Sensor Acquisition

A device samples temperature, pressure, current, and vibration channels. One high-amplitude current channel is multiplexed immediately before a low-level pressure channel. During field testing, the pressure channel shows intermittent step-like noise.

The acquisition review checks:

- channel order
- source impedance
- ADC sample time
- analog front-end settling
- dummy conversion policy
- timestamp jitter
- buffer occupancy
- saturation and quality flags

The likely fault is not the pressure sensor itself but insufficient settling after switching from the high-amplitude current channel.
