# Workflow Overview

1. Load driver, HAL, board, device-model, register-access, interrupt, and update manifests.
2. Simulate device lifecycle states: reset, init, configured, active, idle, suspended, resumed, fault, recovery, update, rollback, and disabled.
3. Estimate control-path latency, abstraction overhead, state coverage, fault-detection coverage, and update compatibility.
4. Generate Python outputs for lifecycle coverage, fault injection, suspend/resume behavior, and latency budgets.
5. Generate R outputs for fleet firmware telemetry and driver reliability reporting.
6. Store SQL schemas for driver contracts, reset causes, device faults, update outcomes, interrupt telemetry, and field evidence.
7. Provide embedded systems scaffolds for HAL contracts, state machines, manifest validation, telemetry aggregation, hardware-assisted event tracing, and HDL interface logic.
