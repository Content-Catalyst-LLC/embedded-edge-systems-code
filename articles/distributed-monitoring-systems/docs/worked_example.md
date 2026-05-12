# Worked Example: Distributed Water, Air, and Industrial Monitoring

A mixed distributed monitoring deployment includes:

- water-quality nodes along an upstream/downstream corridor
- air-quality stations near urban and industrial boundaries
- industrial vibration and temperature nodes at facilities
- high-assurance reference nodes
- lower-cost distributed nodes
- gateway buffering and edge threshold logic

Failure scenarios modeled:

- upstream water anomaly with cross-node timing requirements
- air-quality gateway outage that creates a coverage gap
- industrial vibration node drift
- delayed gateway backfill that should not trigger live alarms
- low-cost nodes disagreeing with a reference node
- edge filtering that must preserve raw-retention and transformation lineage
