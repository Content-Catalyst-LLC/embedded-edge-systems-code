SELECT asset_id, site_id, layer, latency_ms, latency_budget_ms
FROM edge_fleet_inventory
WHERE latency_ms > latency_budget_ms;

SELECT asset_id, site_id, layer, active_version, approved_version
FROM edge_fleet_inventory
WHERE active_version != approved_version;

SELECT asset_id, site_id, layer, trust_state
FROM edge_fleet_inventory
WHERE trust_state != 'verified';

SELECT asset_id, site_id, layer, runtime_assurance_state, watchdog_resets
FROM edge_fleet_inventory
WHERE runtime_assurance_state != 'ready' OR watchdog_resets > 0;
