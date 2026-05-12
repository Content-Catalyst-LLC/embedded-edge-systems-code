# Workflow Overview

This companion workflow turns on-device machine learning concepts into executable artifacts.

## Main computational path

1. Load device capability, model budget, feature schema, quantization profile, runtime manifest, backend validation, decision policy, model lifecycle, monitoring, and security manifests.
2. Generate synthetic embedded AI inference events.
3. Evaluate whether model size, tensor arena, total latency, and energy estimates fit device budgets.
4. Compare reference, quantized, CPU, NPU, DSP, and FPGA/PYNQ output paths using backend-delta tolerances.
5. Apply confidence thresholds, sensor-health checks, model-version checks, and fallback policy.
6. Evaluate field drift proxies from feature summaries and confidence distributions.
7. Check version skew across active, deployed, approved, and decision-used model versions.
8. Run deployment readiness checks before field rollout.
9. Export inference events, backend validation reports, readiness results, fleet summaries, and monitoring outputs.
10. Use R to report latency, fallback, drift, backend-delta, and version-skew behavior across the fleet.

## Engineering emphasis

The code is designed around practical edge AI questions:

- Does the model fit the device, including firmware, buffers, and tensor arena?
- Does total sensing-to-action latency meet the timing budget?
- Does quantization preserve acceptable accuracy and confidence behavior?
- Does the target runtime match reference outputs closely enough?
- Does local action depend on confidence, health, policy, and model version?
- Can the fleet detect drift without uploading all raw data?
- Is rollback tested before deployment?
