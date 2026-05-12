-- Missing or degraded coverage
SELECT z.coverage_zone, z.required_nodes, COUNT(n.node_id) AS active_nodes
FROM topology_zones z
LEFT JOIN node_inventory n
  ON z.coverage_zone = n.coverage_zone
 AND n.connectivity_state = 'online'
 AND n.health_state = 'healthy'
 AND n.calibration_state = 'valid'
GROUP BY z.coverage_zone, z.required_nodes
HAVING COUNT(n.node_id) < z.required_nodes;

-- Stale or unsynchronized telemetry
SELECT event_id, node_id, coverage_zone, quality_state, clock_skew_ms
FROM telemetry_records
WHERE quality_state != 'valid'
   OR clock_skew_ms > 1000
   OR duplicate_detected = TRUE;

-- Gateway pressure or gateway rule skew
SELECT gateway_id, site_id, coverage_zone, buffer_depth, buffer_capacity, active_rule_version, approved_rule_version
FROM gateway_state
WHERE CAST(buffer_depth AS REAL) / buffer_capacity > 0.60
   OR active_rule_version != approved_rule_version;

-- Aggregations with weak lineage or low confidence
SELECT aggregation_id, coverage_zone, quality_state, confidence, inference_boundary
FROM aggregation_records
WHERE lineage_complete = FALSE
   OR confidence < 0.75
   OR inference_boundary NOT IN ('normal_monitoring', 'normal_aggregation');
