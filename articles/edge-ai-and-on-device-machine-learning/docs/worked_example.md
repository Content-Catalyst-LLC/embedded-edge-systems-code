# Worked Example: TinyML Vibration Anomaly Detection at the Edge

This example models a battery-powered or gateway-connected vibration monitoring system for rotating equipment.

## System behavior

1. Accelerometer samples vibration at a configured rate.
2. Firmware forms fixed-length windows.
3. Feature extraction computes RMS, peak, crest factor, spectral energy, and bandpower.
4. Quantized TinyML model classifies normal, warning, or fault-like state.
5. Confidence logic determines whether local action is allowed.
6. Low confidence, unhealthy sensor state, stale model version, or backend mismatch triggers fallback.
7. Selective uplink sends summaries, anomaly scores, and evidence pointers.
8. Cloud or fleet layer monitors confidence distribution, anomaly rate, fallback rate, drift proxy, model-version skew, latency, and rollback status.

## Key records

- device ID
- model version
- runtime backend
- feature version
- quantization profile
- input window ID
- latency
- tensor arena
- confidence
- predicted class
- backend output delta
- fallback used
- decision policy version
- local action
- upload policy
- rollback status
