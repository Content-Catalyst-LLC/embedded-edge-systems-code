-- Privacy quality checks for local edge processing

-- High identifiability with long retention
SELECT event_id, site, device_id, signal_type, identifiability, retention_hours
FROM edge_privacy_events
WHERE identifiability >= 0.75 AND retention_hours > 24;

-- High sharing scope without strong local transformation
SELECT event_id, site, device_id, sharing_scope, local_transformation
FROM edge_privacy_events
WHERE sharing_scope >= 0.60 AND local_transformation < 0.70;

-- Events where minimisation is weak relative to collection breadth
SELECT event_id, signal_type, raw_collection, minimisation
FROM edge_privacy_events
WHERE raw_collection > 0.70 AND minimisation < 0.70;
