# PYNQ Companion Code

This folder contains PYNQ-oriented companion scaffolding for the article:

**Standards, Interoperability, and Governance in Edge Infrastructure**

The goal is to represent how FPGA-backed edge nodes, programmable overlays, streaming pipelines, and hardware/software co-design patterns can be governed as part of embedded and edge infrastructure.

The examples are intentionally safe and portable. The Python code can run as a metadata validation scaffold without requiring physical PYNQ hardware. On a real PYNQ board, the same structure can be extended to load overlays, validate bitstream versions, check accelerator compatibility, and record lifecycle evidence.

Typical governance concerns represented here include:

- overlay version
- bitstream compatibility
- hardware/software interface contract
- accelerator role
- fallback behavior
- lifecycle status
- rollback overlay
- deployment evidence
