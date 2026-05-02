INSERT INTO devices VALUES
('EDGE-001', 'environmental_station', 'RP2040', '1.0.0', 'North Field', '2026-04-01', 1),
('EDGE-002', 'vibration_monitor', 'STM32', '1.2.1', 'Pump House', '2026-04-01', 1),
('EDGE-003', 'moisture_probe', 'ESP32', '0.9.5', 'Research Plot', '2026-04-01', 1);

INSERT INTO sensors VALUES
('TEMP-001', 'EDGE-001', 'temperature', 'celsius', 300),
('VIB-001', 'EDGE-002', 'vibration', 'g', 60),
('MOIST-001', 'EDGE-003', 'soil_moisture', 'percent', 900);

INSERT INTO calibration_records
(sensor_id, calibrated_at, calibration_method, offset_value, scale_factor, technician_or_process)
VALUES
('TEMP-001', '2026-03-20', 'ice_point_reference', 0.10, 1.00, 'lab_calibration'),
('VIB-001', '2026-03-21', 'known_vibration_reference', 0.00, 1.02, 'lab_calibration'),
('MOIST-001', '2026-03-22', 'gravimetric_soil_reference', -0.20, 0.98, 'lab_calibration');

INSERT INTO telemetry_readings
(sensor_id, observed_at, observed_value, battery_voltage, signal_quality, local_inference_score, transmitted)
VALUES
('TEMP-001', '2026-04-01T10:00:00', 21.4, 3.91, 0.98, 0.12, 1),
('TEMP-001', '2026-04-01T10:05:00', 21.7, 3.90, 0.97, 0.13, 1),
('VIB-001', '2026-04-01T10:00:00', 0.81, 3.70, 0.91, 0.44, 1),
('VIB-001', '2026-04-01T10:05:00', 1.42, 3.68, 0.84, 0.78, 1),
('MOIST-001', '2026-04-01T10:00:00', 34.2, 3.50, 0.76, 0.20, 0);
