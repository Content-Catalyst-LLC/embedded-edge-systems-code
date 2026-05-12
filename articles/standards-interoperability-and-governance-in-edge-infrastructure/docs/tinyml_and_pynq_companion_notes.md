# TinyML and PYNQ Companion Notes

This article includes TinyML and PYNQ companion-code scaffolds because embedded and edge systems increasingly combine constrained on-device inference with accelerated edge processing.

## TinyML role

TinyML examples are used to represent:

- local inference under constrained memory and power
- model metadata and versioning
- local-only processing policy
- fallback behavior
- OTA model update compatibility
- edge AI lifecycle governance

## PYNQ role

PYNQ examples are used to represent:

- FPGA-backed edge acceleration
- overlay lifecycle management
- bitstream and interface compatibility
- hardware/software co-design
- streaming sensor pipelines
- acceleration governance and rollback planning

The examples are intentionally generic so they can be adapted to specific boards, sensors, accelerators, and deployment environments.
