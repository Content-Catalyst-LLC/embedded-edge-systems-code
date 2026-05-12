-- Lifecycle and OTA governance quality checks

-- Devices that should not receive new OTA deployments
SELECT device_id, site, vendor, support_state, rollout_ring
FROM devices
WHERE support_state IN ('end-of-support', 'limited-support');

-- Devices that have not checked in recently
SELECT device_id, site, device_class, last_checkin_hours
FROM devices
WHERE last_checkin_hours > 24
ORDER BY last_checkin_hours DESC;

-- Failed or deferred deployment events
SELECT timestamp, device_id, package_id, phase, status, error_code
FROM deployment_events
WHERE status IN ('failed', 'deferred')
ORDER BY timestamp DESC;

-- Rollout decisions that need review
SELECT device_id, package_id, ota_readiness_score, rollout_decision
FROM ota_readiness_scores
WHERE rollout_decision <> 'approve'
ORDER BY ota_readiness_score ASC;
