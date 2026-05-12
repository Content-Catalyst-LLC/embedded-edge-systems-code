# Worked Example: Hybrid Edge-AI Gateway for Industrial Monitoring

This example models an industrial monitoring system using local sensors, an edge gateway, and a cloud control plane.

## System behavior

1. Sensors collect high-frequency vibration, current, temperature, or acoustic signals.
2. A gateway filters and summarizes signals locally.
3. TinyML or edge inference detects anomalies.
4. Local authority policy checks whether action is allowed while connected or offline.
5. The gateway buffers evidence and selectively uplinks summaries.
6. The cloud stores summaries, compares sites, monitors drift, and governs model rollout.
7. Rollout rings update gateways gradually.
8. Reconciliation preserves conflict history when delayed events arrive.

## Key records

- acquisition time
- local decision time
- sync time
- cloud ingest time
- edge policy version
- cloud policy version
- edge model version
- approved model version
- active version
- target version
- state age
- sync lag
- offline duration
- authority status
- reconciliation status
