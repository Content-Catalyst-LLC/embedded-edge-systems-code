-- Calibration expired or traceability incomplete
SELECT sensor_id, site_id, calibration_version, traceability_record_id
FROM sensor_inventory
WHERE calibration_version IS NULL OR traceability_record_id IS NULL;

-- Low-confidence measurements
SELECT measurement_id, sensor_id, site_id, quality_state, expanded_uncertainty, snr_db
FROM measurement_records
WHERE quality_state != 'valid';

-- Missing lineage
SELECT measurement_id, sensor_id, site_id
FROM measurement_records
WHERE lineage_complete = FALSE OR traceability_complete = FALSE;

-- High uncertainty
SELECT measurement_id, sensor_id, expanded_uncertainty
FROM measurement_records
WHERE expanded_uncertainty > 1.5;
