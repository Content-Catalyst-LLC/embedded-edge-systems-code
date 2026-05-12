-- Embedded control quality checks

-- High control error
SELECT timestamp, device_id, loop_id, control_error
FROM control_loop_events
WHERE ABS(control_error) >= 80;

-- Saturation events
SELECT timestamp, device_id, loop_id, candidate_command, filtered_command, safety_filter_reason
FROM control_loop_events
WHERE saturated = TRUE;

-- Deadline misses or low slack
SELECT timestamp, device_id, loop_id, loop_jitter_ms, deadline_slack_ms
FROM control_loop_events
WHERE deadline_missed = TRUE OR deadline_slack_ms <= 0.20;

-- Non-normal safety states
SELECT timestamp, device_id, loop_id, safety_state, supervisory_state, safety_filter_reason
FROM control_loop_events
WHERE safety_state != 'normal' OR supervisory_state != 'closed_loop_nominal';

-- Safety filter activity
SELECT timestamp, device_id, loop_id, candidate_command, filtered_command, safety_filter_reason
FROM control_loop_events
WHERE candidate_command != filtered_command OR safety_filter_reason != 'allowed';
