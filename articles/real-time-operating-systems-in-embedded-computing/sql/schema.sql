CREATE TABLE rtos_tasks (
  task_id TEXT PRIMARY KEY,
  task_name TEXT NOT NULL,
  criticality TEXT NOT NULL,
  priority INTEGER NOT NULL,
  period_ms REAL,
  deadline_ms REAL,
  wcet_ms REAL,
  blocking_ms REAL,
  stack_bytes INTEGER,
  queue_in TEXT,
  queue_out TEXT,
  watchdog_required BOOLEAN
);

CREATE TABLE runtime_trace (
  trace_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  firmware_version TEXT NOT NULL,
  record_time TIMESTAMP NOT NULL,
  task_name TEXT NOT NULL,
  activation_ms REAL,
  start_ms REAL,
  finish_ms REAL,
  deadline_ms REAL,
  deadline_miss BOOLEAN,
  queue_depth INTEGER,
  stack_watermark_bytes INTEGER,
  isr_count INTEGER,
  isr_time_us REAL,
  idle_residency_pct REAL,
  watchdog_resets INTEGER
);

CREATE TABLE queue_trace (
  record_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  firmware_version TEXT NOT NULL,
  queue_name TEXT NOT NULL,
  record_time TIMESTAMP NOT NULL,
  depth INTEGER,
  high_water_mark INTEGER,
  capacity INTEGER,
  producer_task TEXT,
  consumer_task TEXT,
  overflow_count INTEGER,
  stale_drop_count INTEGER
);

CREATE TABLE rtos_fleet_telemetry (
  record_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  firmware_version TEXT NOT NULL,
  board_revision TEXT NOT NULL,
  record_time TIMESTAMP NOT NULL,
  deadline_misses_24h INTEGER,
  queue_overflows_24h INTEGER,
  min_stack_watermark_bytes INTEGER,
  max_isr_time_us REAL,
  context_switches_24h INTEGER,
  idle_residency_pct REAL,
  watchdog_resets INTEGER,
  brownout_count INTEGER,
  tickless_idle_enabled BOOLEAN
);
