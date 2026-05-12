CREATE TABLE devices (
  device_id TEXT PRIMARY KEY,
  device_class TEXT NOT NULL,
  site_id TEXT,
  firmware_version TEXT NOT NULL,
  install_date DATE,
  last_service_date DATE,
  criticality TEXT,
  watchdog_policy TEXT,
  safe_state_policy TEXT
);

CREATE TABLE fault_events (
  event_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  firmware_version TEXT NOT NULL,
  event_time TIMESTAMP NOT NULL,
  fault_class TEXT NOT NULL,
  fault_source TEXT NOT NULL,
  detection_mechanism TEXT,
  detected BOOLEAN NOT NULL,
  recovery_action TEXT,
  recovery_success BOOLEAN,
  recovery_time_ms REAL,
  degraded_mode BOOLEAN,
  safe_state_entered BOOLEAN,
  service_loss_s REAL,
  FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

CREATE TABLE reset_log (
  reset_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  reset_time TIMESTAMP NOT NULL,
  reset_cause TEXT NOT NULL,
  firmware_version TEXT NOT NULL,
  uptime_before_reset_s REAL,
  brownout_count INTEGER,
  watchdog_count INTEGER,
  last_fault_class TEXT,
  persistent_state_valid BOOLEAN,
  FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

CREATE TABLE lifecycle_actions (
  action_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  action_time TIMESTAMP NOT NULL,
  action_type TEXT NOT NULL,
  trigger_condition TEXT,
  notes TEXT,
  FOREIGN KEY (device_id) REFERENCES devices(device_id)
);
