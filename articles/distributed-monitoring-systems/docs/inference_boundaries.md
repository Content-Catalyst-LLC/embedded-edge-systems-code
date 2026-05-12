# Coverage and Inference Boundaries

A distributed monitoring system should state what it can and cannot validly claim.

## Claim types

- Node-local condition: requires fresh, calibrated, quality-valid measurement from a known node.
- Zone condition: requires required node coverage and a valid aggregation rule.
- Cross-node comparison: requires comparable calibration, synchronized event times, and compatible semantics.
- Gradient or spatial trend: requires node placement across expected gradient and adequate spatial density.
- Event propagation: requires strong timing discipline and known node positions.
- System-level health: requires preserved coverage, freshness, quality, and aggregation confidence.

Inference boundaries prevent dashboards from implying total awareness when visibility is partial or degraded.
