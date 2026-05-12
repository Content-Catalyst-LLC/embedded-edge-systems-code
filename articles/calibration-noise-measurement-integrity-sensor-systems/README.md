# Calibration, Noise, and Measurement Integrity in Sensor Systems

This companion directory supports the article **Calibration, Noise, and Measurement Integrity in Sensor Systems**.

It turns the article into a practical engineering scaffold for sensor calibration, noise characterization, uncertainty propagation, measurement provenance, quality flags, traceability, drift monitoring, firmware filtering, ADC sampling, analog front-end documentation, and fleet-level measurement-integrity reporting.

The companion stack includes:

- Python calibration, uncertainty, SNR, drift, and quality-gating workflows
- R fleet-level measurement quality reporting
- SQL schemas for calibration, measurement records, quality flags, and traceability
- C firmware-adjacent raw-to-calibrated conversion and quality flagging
- C++ measurement state-machine abstraction
- Rust measurement-record validator
- Go telemetry routing for low-confidence measurement events
- MicroPython sensor calibration and quality heartbeat prototype
- TinyML local measurement-quality classifier scaffold
- PYNQ acquisition/quality overlay validation scaffold
- HDL timestamp, saturation, ADC-valid, and quality-frame examples
- Bash runners and manifest validation
- YAML/JSON configs for calibration, ADC, AFE, noise, traceability, quality flags, quality gates, drift, filters, and deployment readiness
