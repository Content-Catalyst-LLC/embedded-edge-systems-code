-- Autonomy quality checks

-- Low-confidence decisions
SELECT timestamp, device_id, mission_type, decision_confidence, candidate_action, filtered_action
FROM autonomy_events
WHERE decision_confidence < 0.70;

-- Latency budget violations
SELECT timestamp, device_id, latency_ms, latency_budget_ms, candidate_action, filtered_action
FROM autonomy_events
WHERE latency_ms > latency_budget_ms;

-- Fallback actions
SELECT timestamp, device_id, candidate_action, filtered_action, safety_state
FROM autonomy_events
WHERE action_type = 'fallback';

-- Human intervention required
SELECT timestamp, device_id, mission_type, belief_state, decision_confidence
FROM autonomy_events
WHERE human_intervention_required = TRUE;

-- Drift warnings
SELECT timestamp, device_id, input_drift_score, confidence_drift_score
FROM autonomy_events
WHERE input_drift_score >= 0.25 OR confidence_drift_score >= 0.20;
