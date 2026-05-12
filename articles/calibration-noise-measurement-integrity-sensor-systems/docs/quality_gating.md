# Measurement Quality Gating

Measurement quality gating prevents weak values from silently driving high-consequence actions.

Examples:

- `valid`: eligible for control, alarms, analytics, and reporting.
- `stale`: allowed for historical display only.
- `low_snr`: allowed for low-confidence trend context; restricted from high-confidence alarms.
- `calibration_expired`: allowed for provisional trend analysis; restricted from compliance or high-consequence decisions.
- `reference_warning`: allowed for diagnostics; restricted from unqualified multi-channel comparison.
- `coefficient_mismatch`: diagnostic logging only until configuration is corrected.
- `saturated`: range-exceeded alarm only; magnitude should not be interpreted as true value.
