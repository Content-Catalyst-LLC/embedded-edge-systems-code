# Internet of Things Sensor Architectures

This companion directory supports the article **Internet of Things Sensor Architectures**.

It turns the article into a practical engineering scaffold for IoT sensor fleet architecture, telemetry freshness, device identity, gateway buffering, replay semantics, command authority, lifecycle state, trust-state validation, schema contracts, firmware/configuration skew, quality flags, observability, and deployment readiness.

The companion stack includes:

- Python fleet architecture, freshness, trust, replay, command, and readiness workflows
- R fleet reporting and sensor architecture health summaries
- SQL schemas for devices, gateways, telemetry, identity, command logs, updates, and incidents
- C endpoint queue, heartbeat, telemetry quality, and retry scaffolds
- C++ device/gateway lifecycle and command state-machine examples
- Rust telemetry and device-record validator
- Go telemetry and command routing service scaffold
- MicroPython constrained endpoint prototype
- TinyML local event/quality classifier scaffold
- PYNQ gateway stream/quality overlay validation scaffold
- HDL timestamp, queue, event-trigger, and telemetry-frame modules
- Bash workflow runners and manifest validation
- YAML/JSON configuration for identity, topics, schemas, buffering, replay, security, command authority, OTA rollout, observability, and readiness
