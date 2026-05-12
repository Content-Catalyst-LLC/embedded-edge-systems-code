-- Devices with lifecycle or trust problems
SELECT device_id, site_id, trust_state, lifecycle_state, credential_state
FROM device_inventory
WHERE trust_state != 'verified'
   OR lifecycle_state != 'active'
   OR credential_state != 'valid';

-- Version skew
SELECT device_id, site_id, active_firmware, approved_firmware, active_config, approved_config, active_schema, approved_schema
FROM device_inventory
WHERE active_firmware != approved_firmware
   OR active_config != approved_config
   OR active_schema != approved_schema;

-- Gateway pressure
SELECT gateway_id, site_id, buffer_depth, buffer_capacity
FROM gateway_state
WHERE CAST(buffer_depth AS REAL) / buffer_capacity > 0.60;

-- Duplicate replay
SELECT event_id, device_id, replay_batch_id, idempotency_key
FROM telemetry_records
WHERE duplicate_detected = TRUE;

-- Unsafe or rejected command attempts
SELECT command_id, issuer, command_type, trust_state, authorized, acknowledged, command_result
FROM command_log
WHERE authorized = FALSE
   OR acknowledged = FALSE
   OR command_result LIKE 'blocked%'
   OR command_result LIKE 'rejected%';
