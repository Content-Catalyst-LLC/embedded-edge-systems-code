-- Edge Metric Views

CREATE VIEW IF NOT EXISTS sensor_reliability_summary AS
SELECT
    s.sensor_id,
    s.sensor_type,
    d.device_id,
    d.hardware_platform,
    COUNT(t.reading_id) AS reading_count,
    AVG(t.observed_value) AS mean_observed_value,
    AVG(t.battery_voltage) AS mean_battery_voltage,
    AVG(t.signal_quality) AS mean_signal_quality,
    MAX(t.local_inference_score) AS max_local_inference_score
FROM sensors s
JOIN devices d ON s.device_id = d.device_id
LEFT JOIN telemetry_readings t ON s.sensor_id = t.sensor_id
GROUP BY
    s.sensor_id,
    s.sensor_type,
    d.device_id,
    d.hardware_platform;
