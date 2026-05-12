CREATE TABLE devices (
  device_id TEXT PRIMARY KEY,
  firmware_version TEXT NOT NULL,
  board_revision TEXT NOT NULL,
  bootloader_version TEXT,
  hardware_profile TEXT
);

CREATE TABLE driver_contracts (
  driver_id TEXT PRIMARY KEY,
  device_name TEXT NOT NULL,
  bus TEXT,
  interrupt_line TEXT,
  owner_layer TEXT NOT NULL,
  blocking_behavior TEXT,
  isr_safe BOOLEAN,
  timeout_ms INTEGER,
  power_managed BOOLEAN,
  suspend_resume_supported BOOLEAN,
  error_semantics TEXT
);

CREATE TABLE device_lifecycle_events (
  event_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  driver_id TEXT NOT NULL,
  firmware_version TEXT NOT NULL,
  board_revision TEXT NOT NULL,
  event_time TIMESTAMP NOT NULL,
  lifecycle_state TEXT NOT NULL,
  event_type TEXT NOT NULL,
  latency_ms REAL,
  result TEXT,
  error_code TEXT,
  reset_cause TEXT,
  FOREIGN KEY (driver_id) REFERENCES driver_contracts(driver_id)
);

CREATE TABLE firmware_telemetry (
  record_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  firmware_version TEXT NOT NULL,
  board_revision TEXT NOT NULL,
  record_time TIMESTAMP NOT NULL,
  boot_count INTEGER,
  watchdog_resets INTEGER,
  brownout_count INTEGER,
  bus_timeouts INTEGER,
  driver_errors INTEGER,
  suspend_resume_failures INTEGER,
  interrupt_count_24h INTEGER,
  update_attempts INTEGER,
  update_successes INTEGER,
  rollback_count INTEGER
);

CREATE TABLE update_manifest (
  update_id TEXT PRIMARY KEY,
  firmware_version TEXT NOT NULL,
  target_board_revision TEXT NOT NULL,
  requires_bootloader_version TEXT,
  rollback_supported BOOLEAN,
  interrupted_update_tested BOOLEAN,
  driver_contract_version TEXT,
  compatibility_status TEXT
);
