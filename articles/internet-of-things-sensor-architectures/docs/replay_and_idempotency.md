# Replay and Idempotency

Store-and-forward systems need explicit replay semantics.

## Required evidence

- event time
- upload time
- ingestion time
- processing time
- sequence number
- replay batch ID
- idempotency key
- duplicate-detected flag
- freshness flag
- drop reason where data are discarded

Backfilled telemetry is valuable for history but should not be mistaken for live operational state.
