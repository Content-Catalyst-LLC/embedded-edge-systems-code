# Workflow Overview

This companion workflow turns embedded control concepts into executable artifacts.

## Main computational path

1. Load configuration manifests for plant, controller, timing, actuator, estimator, and safety envelope.
2. Simulate a discrete-time plant under PID control.
3. Inject disturbance, measurement noise, actuator saturation, and loop jitter.
4. Apply safety filtering to candidate commands.
5. Track error, filtered command, saturation, loop timing, deadline slack, and supervisory state.
6. Run a DC motor speed-control demonstration.
7. Export control-loop logs and summary reports.
8. Use R to report saturation, timing, error, and safety-filter behavior.
9. Use systems-language examples to show how the same concerns appear in firmware, middleware, safety validators, telemetry gateways, and hardware-adjacent accelerators.

## Engineering emphasis

The code is designed around engineering questions:

- What was measured?
- What was estimated?
- What command did the controller propose?
- What command did the safety filter allow?
- Did the actuator saturate?
- Did the loop meet its deadline?
- Was jitter inside the timing budget?
- Did supervisory control enter warning, degraded, safe stop, fault, or recovery?
- Can logs reconstruct measured, estimated, commanded, filtered, and physical behavior?
