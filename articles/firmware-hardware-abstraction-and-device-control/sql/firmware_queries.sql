-- Driver or lifecycle events requiring engineering review.
SELECT *
FROM device_lifecycle_events
WHERE result <> 'success'
   OR error_code <> 'none'
   OR latency_ms > 250;

-- Firmware/device fleet risk summary.
SELECT
  device_id,
  firmware_version,
  board_revision,
  watchdog_resets,
  brownout_count,
  bus_timeouts,
  driver_errors,
  suspend_resume_failures,
  rollback_count,
  (watchdog_resets + brownout_count + bus_timeouts + driver_errors + suspend_resume_failures + rollback_count) AS total_control_risk_events
FROM firmware_telemetry
ORDER BY total_control_risk_events DESC;

-- Updates that need integrity or compatibility review.
SELECT *
FROM update_manifest
WHERE rollback_supported = FALSE
   OR interrupted_update_tested = FALSE
   OR compatibility_status <> 'compatible';
