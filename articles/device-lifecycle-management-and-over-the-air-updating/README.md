# Device Lifecycle Management and Over-the-Air Updating

This companion directory supports the Sustainable Catalyst article **“Device Lifecycle Management and Over-the-Air Updating.”**

The workflows model device lifecycle management and OTA updating as a trust-preserving systems discipline across heterogeneous embedded and edge fleets. The examples include:

- C update slot and rollback-state logic for constrained devices
- C++ staged rollout planning for device groups
- Rust lifecycle policy validation for support-state and rollback readiness
- Go OTA deployment status service for edge gateways
- Python OTA readiness and rollout-risk scoring
- R lifecycle compliance and update-status reporting
- SQL schemas for devices, update packages, deployments, lifecycle events, and recovery evidence
- Jupyter notebooks for reproducible fleet analysis
- TinyML and firmware-style stubs for constrained update contexts
- Hardware/device profiles for compatibility and support-state modeling

The goal is to show how identity, compatibility, validation, rollout staging, rollback, observability, and retirement can be represented as reproducible evidence rather than informal operational knowledge.

## TinyML and PYNQ companion code

This article directory includes TinyML and PYNQ scaffolds as part of the Embedded & Edge Systems companion-code standard.

- `tinyml/` represents constrained on-device inference, model metadata, fallback behavior, and TinyML lifecycle governance.
- `pynq/` represents FPGA-backed edge acceleration, overlay metadata, bitstream compatibility, interface contracts, and acceleration lifecycle governance.
