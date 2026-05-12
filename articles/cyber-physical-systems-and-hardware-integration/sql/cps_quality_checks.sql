-- CPS quality checks

-- Stale sensors
SELECT timestamp, device_id, subsystem, sensor_age_ms
FROM cps_events
WHERE sensor_age_ms > 3.0;

-- Timing failures
SELECT timestamp, device_id, subsystem, loop_jitter_ms, deadline_slack_ms
FROM cps_events
WHERE deadline_missed = TRUE OR deadline_slack_ms < 0;

-- Runtime assurance activity
SELECT timestamp, device_id, subsystem, candidate_command, filtered_command
FROM cps_events
WHERE candidate_command != filtered_command;

-- Uncertainty-budget violations
SELECT timestamp, device_id, subsystem, total_uncertainty, uncertainty_budget
FROM cps_events
WHERE total_uncertainty > uncertainty_budget;

-- Integration concerns
SELECT timestamp, device_id, subsystem, interface_error, safety_state, recovery_event
FROM cps_events
WHERE interface_error = TRUE OR safety_state != 'normal' OR recovery_event = TRUE;
