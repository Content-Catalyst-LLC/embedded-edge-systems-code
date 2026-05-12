# Command Authority

IoT systems often begin as telemetry systems and gradually acquire control features. Command authority should be explicit.

## Commands covered

- configuration updates
- firmware updates
- gateway rule updates
- sampling-rate changes
- remote actuation
- credential revocation

## Required checks

- issuer authorized
- command schema valid
- target trust state verified
- telemetry freshness acceptable when command depends on state
- local safety boundary preserved
- staged rollout used for high-impact updates
- rollback path available
- command acknowledgment recorded
