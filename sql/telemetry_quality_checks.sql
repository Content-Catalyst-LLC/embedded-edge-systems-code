-- Telemetry Quality Checks

-- Missing or invalid battery voltage.
SELECT *
FROM telemetry_readings
WHERE battery_voltage IS NULL
   OR battery_voltage < 3.0;

-- Low signal quality.
SELECT *
FROM telemetry_readings
WHERE signal_quality IS NULL
   OR signal_quality < 0.80;

-- Devices without telemetry.
SELECT d.device_id, d.device_type
FROM devices d
LEFT JOIN sensors s ON d.device_id = s.device_id
LEFT JOIN telemetry_readings t ON s.sensor_id = t.sensor_id
WHERE t.reading_id IS NULL;

-- Telemetry completeness by sensor.
SELECT
    sensor_id,
    COUNT(*) AS readings,
    AVG(CASE WHEN observed_value IS NOT NULL THEN 1.0 ELSE 0.0 END) AS observed_value_completeness,
    AVG(CASE WHEN battery_voltage IS NOT NULL THEN 1.0 ELSE 0.0 END) AS battery_voltage_completeness,
    AVG(CASE WHEN signal_quality IS NOT NULL THEN 1.0 ELSE 0.0 END) AS signal_quality_completeness
FROM telemetry_readings
GROUP BY sensor_id;
