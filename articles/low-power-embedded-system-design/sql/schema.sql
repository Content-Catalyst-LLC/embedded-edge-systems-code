CREATE TABLE devices (
  device_id TEXT PRIMARY KEY,
  site_id TEXT,
  firmware_version TEXT NOT NULL,
  hardware_revision TEXT,
  install_date DATE,
  power_profile TEXT
);

CREATE TABLE power_state_records (
  record_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  record_time TIMESTAMP NOT NULL,
  state_name TEXT NOT NULL,
  current_ma REAL,
  voltage_v REAL,
  duration_s REAL,
  energy_mj REAL,
  FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

CREATE TABLE power_telemetry (
  record_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  record_time TIMESTAMP NOT NULL,
  battery_v REAL,
  state_of_charge_pct REAL,
  wake_count_24h INTEGER,
  false_wake_count_24h INTEGER,
  sleep_residency_pct REAL,
  tx_count_24h INTEGER,
  retry_count_24h INTEGER,
  rx_window_s_24h REAL,
  brownout_count INTEGER,
  low_energy_mode_entries INTEGER,
  temperature_c REAL,
  solar_input_wh REAL,
  FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

CREATE TABLE wake_events (
  wake_event_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  wake_time TIMESTAMP NOT NULL,
  wake_source TEXT NOT NULL,
  wake_latency_ms REAL,
  was_false_wake BOOLEAN,
  returned_to_sleep BOOLEAN,
  FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

CREATE TABLE brownout_events (
  brownout_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  brownout_time TIMESTAMP NOT NULL,
  battery_v REAL,
  storage_write_inhibited BOOLEAN,
  persistent_state_valid BOOLEAN,
  reset_cause_preserved BOOLEAN,
  FOREIGN KEY (device_id) REFERENCES devices(device_id)
);
