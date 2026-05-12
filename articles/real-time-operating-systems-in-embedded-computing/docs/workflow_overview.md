# Workflow Overview

1. Load task, priority, interrupt, queue, synchronization, memory, power, and telemetry manifests.
2. Estimate task utilization, response-time risk, slack margin, queue pressure, and overload behavior.
3. Simulate fixed-priority scheduling, ISR interference, priority inversion, and deadline misses.
4. Generate Python outputs for task timing, schedule traces, queue trajectories, jitter, and slack.
5. Generate R outputs for fleet timing evidence, deadline misses, stack watermarks, ISR load, and idle residency.
6. Store SQL schemas for task contracts, runtime traces, queue evidence, stack evidence, ISR load, power behavior, and watchdog resets.
7. Provide embedded systems scaffolds for task contracts, schedulers, manifest validation, telemetry aggregation, hardware timestamping, and HDL deadline monitors.
