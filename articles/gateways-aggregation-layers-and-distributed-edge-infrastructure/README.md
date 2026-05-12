# Gateways, Aggregation Layers, and Distributed Edge Infrastructure

This companion directory supports the article **“Gateways, Aggregation Layers, and Distributed Edge Infrastructure.”**

The goal is to make the article useful to engineers, researchers, and advanced technical readers by pairing the systems explanation with executable gateway buffering, protocol mediation, aggregation, replay, deduplication, selective uplink, gateway SLOs, child-device monitoring, site-state quality scoring, and fleet-level reporting.

The workflows model gateway and aggregation systems as evidence infrastructure involving:

- child-device registries
- parent-child topology
- protocol maps and normalized telemetry schemas
- acquisition, gateway receipt, aggregation, upload, and upstream ingestion time
- gateway buffering and store-and-forward
- replay semantics and idempotency keys
- duplicate handling and late-arrival policy
- aggregation contracts and site-state quality
- freshness, missing-child, and stale-device metrics
- selective uplink policies
- local policy manifests and decision-used versions
- gateway SLOs and capacity budgets
- protocol error monitoring
- security profiles and trust boundaries
- MicroPython child-device heartbeat prototypes
- TinyML gateway anomaly classification
- PYNQ/FPGA preprocessing and buffer-watermark validation
- HDL stream timestamping, buffer watermarking, sync pulse, and telemetry framing
- C/C++/Rust/Go systems examples

This directory is not production gateway infrastructure. It is an engineering-grade companion scaffold intended to make the article's gateway and aggregation architecture executable, inspectable, and extensible.
