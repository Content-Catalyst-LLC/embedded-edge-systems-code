# Worked Example: Industrial Temperature and Vibration Monitoring

Scenario:

- An industrial edge node monitors motor temperature and vibration.
- Temperature values come from an RTD or thermistor channel.
- Vibration values come from an accelerometer.
- Channels are sampled through an ADC with a defined channel sequence and settling delay.
- Firmware applies calibration coefficients and filter versions.
- The edge node forwards calibrated values, uncertainty estimates, SNR, quality flags, and provenance.

Failure scenario:

- A firmware update loads a stale calibration coefficient.
- Vibration SNR falls below threshold after a mounting issue.
- ADC channel settling risk increases after channel-order change.
- The quality gate blocks high-confidence alarm and model-feature use while preserving diagnostic records.
