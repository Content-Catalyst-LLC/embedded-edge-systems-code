# Worked Example: Local Vibration Analytics and Selective Uplink

This example models an industrial vibration monitoring system.

## System behavior

1. Accelerometer samples vibration locally.
2. Device or gateway forms fixed-length windows with overlap.
3. Local preprocessing validates units, missing samples, and sensor health.
4. Feature extraction computes RMS, peak, crest factor, spectral energy, and bandpower.
5. Rule logic or local inference classifies normal, warning, degraded, or fault-like conditions.
6. Recent raw windows are retained locally for incident review.
7. Normal summaries are batched or sampled.
8. Warning and fault-like events are forwarded immediately.
9. Buffered summaries replay after connectivity returns with event-time lineage.
10. Cloud or fleet layer compares anomaly rates, feature drift, replay lag, and rule-version behavior across sites.

## Key records

- signal ID
- sensor ID
- gateway ID
- acquisition time
- processing time
- buffer-entry time
- upload time
- upstream ingestion time
- window ID
- feature version
- rule version
- local inference version
- quality flag
- event status
- idempotency key
- replay batch ID
- uplink mode
- drop or suppression reason
- lineage completeness flag
