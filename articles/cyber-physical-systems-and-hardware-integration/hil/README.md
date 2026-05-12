# Hardware-in-the-Loop Scaffold

This folder contains a minimal HIL scaffold for CPS validation.

HIL tests should exercise real firmware, real timing, real bus behavior, real drivers, and safety logic against a simulated or controlled physical process.

Recommended test cases:

- stale sensor
- actuator saturation
- bus timeout
- deadline miss
- thermal warning
- thermal fault
- uncertainty-budget violation
- safe stop
- recovery
