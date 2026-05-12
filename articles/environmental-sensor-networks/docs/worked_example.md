# Worked Example: Watershed Turbidity Network

A watershed monitoring network includes upstream, midstream, and downstream nodes. During a rainfall event, turbidity rises downstream, but one midstream station reports stable values.

The engineering review checks:

- site representativeness
- sensor fouling and maintenance date
- calibration age
- sampling cadence
- communication gaps
- buffer replay timestamps
- battery and solar status
- node quality flags

The likely issue is not necessarily a stable midstream condition. It may be fouling, a stale reading, a maintenance gap, or a communication replay artifact.
