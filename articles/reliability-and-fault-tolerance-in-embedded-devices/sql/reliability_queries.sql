-- Undetected or unrecovered fault events.
SELECT *
FROM fault_events
WHERE detected = FALSE
   OR recovery_success = FALSE
   OR safe_state_entered = TRUE;

-- Device-level dependability summary.
SELECT
  device_id,
  COUNT(*) AS fault_events,
  SUM(CASE WHEN detected THEN 1 ELSE 0 END) AS detected_events,
  SUM(CASE WHEN recovery_success THEN 1 ELSE 0 END) AS recovered_events,
  SUM(service_loss_s) AS total_service_loss_s,
  SUM(CASE WHEN safe_state_entered THEN 1 ELSE 0 END) AS safe_state_entries
FROM fault_events
GROUP BY device_id
ORDER BY total_service_loss_s DESC, fault_events DESC;

-- Repeated watchdog resets indicating unresolved faults.
SELECT
  device_id,
  firmware_version,
  COUNT(*) AS watchdog_resets,
  AVG(uptime_before_reset_s) AS avg_uptime_before_reset_s,
  MAX(watchdog_count) AS max_watchdog_count
FROM reset_log
WHERE reset_cause = 'watchdog'
GROUP BY device_id, firmware_version
HAVING COUNT(*) >= 2
ORDER BY watchdog_resets DESC;
