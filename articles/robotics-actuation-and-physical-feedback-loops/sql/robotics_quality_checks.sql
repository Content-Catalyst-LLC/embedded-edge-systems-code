-- Robotics quality checks

-- High tracking error
SELECT timestamp, robot_id, joint_id, tracking_error
FROM control_loop_events
WHERE ABS(tracking_error) >= 0.08;

-- Excessive loop jitter
SELECT timestamp, robot_id, joint_id, loop_jitter_ms
FROM control_loop_events
WHERE loop_jitter_ms >= 2.0;

-- Saturation events
SELECT timestamp, robot_id, joint_id, command, saturated
FROM control_loop_events
WHERE saturated = TRUE;

-- Non-normal safety or fault states
SELECT timestamp, robot_id, joint_id, safety_state, fault_state
FROM control_loop_events
WHERE safety_state != 'normal' OR fault_state != 'normal';
