-- Devices with power-risk indicators.
SELECT *
FROM power_telemetry
WHERE battery_v < 3.55
   OR sleep_residency_pct < 92
   OR retry_count_24h > 8
   OR false_wake_count_24h > 10
   OR brownout_count > 0;

-- Fleet-level power summary.
SELECT
  device_id,
  AVG(battery_v) AS mean_battery_v,
  AVG(sleep_residency_pct) AS mean_sleep_residency_pct,
  SUM(wake_count_24h) AS total_wakes,
  SUM(false_wake_count_24h) AS total_false_wakes,
  SUM(tx_count_24h) AS total_transmissions,
  SUM(retry_count_24h) AS total_retries,
  SUM(brownout_count) AS total_brownouts
FROM power_telemetry
GROUP BY device_id
ORDER BY mean_battery_v ASC, total_retries DESC;

-- Wake sources causing false wakes.
SELECT
  device_id,
  wake_source,
  COUNT(*) AS false_wake_events
FROM wake_events
WHERE was_false_wake = TRUE
GROUP BY device_id, wake_source
ORDER BY false_wake_events DESC;
