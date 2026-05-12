-- Tasks with basic timing risk.
SELECT
  task_id,
  task_name,
  criticality,
  priority,
  period_ms,
  deadline_ms,
  wcet_ms,
  blocking_ms,
  (wcet_ms / period_ms) AS utilization,
  (deadline_ms - (wcet_ms + blocking_ms)) AS basic_slack_ms
FROM rtos_tasks
WHERE (deadline_ms - (wcet_ms + blocking_ms)) < 5
   OR (wcet_ms / period_ms) > 0.7
ORDER BY basic_slack_ms ASC;

-- Devices with RTOS timing risks.
SELECT *
FROM rtos_fleet_telemetry
WHERE deadline_misses_24h > 0
   OR queue_overflows_24h > 0
   OR min_stack_watermark_bytes < 512
   OR max_isr_time_us > 250
   OR watchdog_resets > 0
ORDER BY deadline_misses_24h DESC, queue_overflows_24h DESC;

-- Queues near capacity or overflowing.
SELECT
  device_id,
  queue_name,
  high_water_mark,
  capacity,
  CAST(high_water_mark AS REAL) / capacity AS pressure_ratio,
  overflow_count,
  stale_drop_count
FROM queue_trace
WHERE overflow_count > 0
   OR CAST(high_water_mark AS REAL) / capacity >= 0.75
ORDER BY pressure_ratio DESC, overflow_count DESC;
