# Workflow Overview

1. Load energy-budget, power-state, wake-source, retention, regulator, telemetry, and brownout manifests.
2. Estimate average current, average power, lifetime, energy per event, and energy reserve.
3. Model sleep residency, wake storms, radio retries, receive windows, sensor warm-up, and regulator leakage.
4. Generate Python outputs for state-level energy, lifetime sensitivity, and brownout reserve.
5. Generate R outputs for fleet power reporting and battery-risk review.
6. Store SQL schemas for power-state evidence, battery telemetry, communication energy, wake events, and maintenance thresholds.
7. Provide embedded systems scaffolds for sleep policies, power-state machines, manifest validation, telemetry aggregation, hardware-assisted wake filtering, and HDL wake counters.
