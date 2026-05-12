# Worked Example: Environmental and Industrial IoT Sensor Fleet

A mixed fleet includes:

- battery-powered outdoor environmental nodes
- wired industrial vibration sensors
- gateway-attached temperature probes
- edge nodes running local anomaly rules

Failure conditions modeled:

- sleeping nodes that should not be mistaken for failed nodes
- gateway outage and replay
- duplicate replay after reconnect
- firmware skew across devices
- configuration rollout changing sampling intervals
- trust-state degradation from certificate expiry
- command authority risk from remote threshold updates
