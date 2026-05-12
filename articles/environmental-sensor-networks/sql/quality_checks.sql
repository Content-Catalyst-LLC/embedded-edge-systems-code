-- Measurements with data-quality concerns.
SELECT *
FROM environmental_measurements
WHERE quality_flag NOT IN ('valid', 'event_valid')
   OR link_quality < 0.60
   OR packet_retries > 3
   OR buffer_age_s > 240
   OR battery_v < 11.8;

-- Node-level network health summary.
SELECT
  node_id,
  site_id,
  COUNT(*) AS records,
  SUM(CASE WHEN quality_flag NOT IN ('valid', 'event_valid') THEN 1 ELSE 0 END) AS warning_records,
  AVG(link_quality) AS mean_link_quality,
  MAX(buffer_age_s) AS max_buffer_age_s,
  SUM(packet_retries) AS packet_retry_total,
  MIN(battery_v) AS min_battery_v
FROM environmental_measurements
GROUP BY node_id, site_id
ORDER BY warning_records DESC, max_buffer_age_s DESC;

-- Expired or expiring calibration records.
SELECT *
FROM calibration_records
WHERE status <> 'current'
   OR valid_until < DATE('now');
