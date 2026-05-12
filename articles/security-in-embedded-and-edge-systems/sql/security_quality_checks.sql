-- Security quality checks

-- Unsupported or end-of-support devices
SELECT device_id, site, device_class, support_state, firmware_version
FROM device_security_profiles
WHERE support_state IN ('limited-support', 'end-of-support');

-- Devices without rollback readiness
SELECT device_id, site, device_class, firmware_version
FROM device_security_profiles
WHERE rollback_ready = FALSE;

-- Devices with high exposure and weak monitoring
SELECT device_id, site, exposure, monitoring_maturity
FROM device_security_profiles
WHERE exposure >= 0.70 AND monitoring_maturity < 0.60;

-- Devices with weak boot integrity
SELECT device_id, site, boot_integrity, secure_boot
FROM device_security_profiles
WHERE boot_integrity < 0.70 OR secure_boot = FALSE;
