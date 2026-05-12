-- Interoperability governance quality checks

-- Devices missing supported standards profiles
SELECT device_id, site, vendor, standard_profile
FROM edge_assets
WHERE standard_profile IS NULL OR TRIM(standard_profile) = '';

-- End-of-support or limited-support devices
SELECT device_id, site, vendor, device_class, support_state
FROM edge_assets
WHERE support_state IN ('end-of-support', 'limited-support');

-- Governance scores below operational threshold
SELECT device_id, governance_score, risk_band
FROM governance_scores
WHERE governance_score < 0.70
ORDER BY governance_score ASC;

-- Schema drift by site
SELECT site, schema_version, COUNT(*) AS devices
FROM edge_assets
GROUP BY site, schema_version
ORDER BY site, schema_version;
