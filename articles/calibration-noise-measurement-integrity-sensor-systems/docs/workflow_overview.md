# Workflow Overview

This companion workflow turns calibration, noise, and measurement integrity into executable engineering artifacts.

## Main computational path

1. Load sensor inventory, calibration manifest, traceability record, AFE configuration, ADC sampling plan, noise budget, quality flag policy, quality gate policy, drift policy, firmware filter manifest, and readiness config.
2. Load sample measurement records.
3. Convert raw ADC counts to raw engineering values.
4. Apply gain/offset calibration.
5. Compute combined and expanded uncertainty.
6. Estimate SNR.
7. Detect calibration expiration, coefficient mismatch, low SNR, drift, out-of-range values, saturation, staleness, and lineage gaps.
8. Apply quality gates to determine allowed and restricted downstream uses.
9. Generate deployment readiness evidence.
10. Use R to summarize fleet-level measurement quality across sites and sensor families.
