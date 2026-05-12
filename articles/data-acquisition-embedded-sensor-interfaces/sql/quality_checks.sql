-- Measurements with evidence-quality concerns.
SELECT *
FROM measurement_events
WHERE quality_flag <> 'valid'
   OR timestamp_jitter_ms > 5
   OR buffer_age_ms > 250
   OR bus_retries > 2
   OR adc_overrun = TRUE
   OR stale_read = TRUE;

-- Device-level acquisition health.
SELECT
  device_id,
  COUNT(*) AS measurement_count,
  SUM(CASE WHEN quality_flag <> 'valid' THEN 1 ELSE 0 END) AS warning_count,
  AVG(timestamp_jitter_ms) AS avg_timestamp_jitter_ms,
  MAX(buffer_age_ms) AS max_buffer_age_ms,
  SUM(bus_retries) AS bus_retry_total
FROM measurement_events
GROUP BY device_id
ORDER BY warning_count DESC, max_buffer_age_ms DESC;

-- Channel lineage and calibration coverage.
SELECT
  c.channel_id,
  c.physical_quantity,
  c.units,
  c.interface_type,
  c.calibration_version,
  COUNT(e.event_id) AS event_count
FROM acquisition_channels c
LEFT JOIN measurement_events e ON c.channel_id = e.channel_id
GROUP BY c.channel_id, c.physical_quantity, c.units, c.interface_type, c.calibration_version;
