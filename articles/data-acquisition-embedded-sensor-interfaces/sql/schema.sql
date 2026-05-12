CREATE TABLE acquisition_devices (
  device_id TEXT PRIMARY KEY,
  site_id TEXT NOT NULL,
  device_class TEXT NOT NULL,
  firmware_version TEXT,
  installed_at TIMESTAMP
);

CREATE TABLE acquisition_channels (
  channel_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  physical_quantity TEXT NOT NULL,
  units TEXT NOT NULL,
  interface_type TEXT NOT NULL,
  sample_rate_hz REAL NOT NULL,
  signal_bandwidth_hz REAL,
  adc_bits INTEGER,
  reference_mv REAL,
  calibration_version TEXT,
  FOREIGN KEY (device_id) REFERENCES acquisition_devices(device_id)
);

CREATE TABLE measurement_events (
  event_id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  site_id TEXT NOT NULL,
  channel_id TEXT NOT NULL,
  acquisition_time TIMESTAMP NOT NULL,
  processing_time TIMESTAMP NOT NULL,
  value REAL NOT NULL,
  raw_code INTEGER,
  reference_mv REAL,
  calibration_version TEXT,
  quality_flag TEXT NOT NULL,
  timestamp_jitter_ms REAL,
  buffer_age_ms REAL,
  bus_retries INTEGER,
  adc_overrun BOOLEAN,
  stale_read BOOLEAN,
  FOREIGN KEY (channel_id) REFERENCES acquisition_channels(channel_id)
);

CREATE TABLE calibration_records (
  calibration_version TEXT PRIMARY KEY,
  channel_id TEXT NOT NULL,
  calibrated_at TIMESTAMP NOT NULL,
  valid_until TIMESTAMP,
  coefficient_json TEXT,
  reference_standard TEXT,
  FOREIGN KEY (channel_id) REFERENCES acquisition_channels(channel_id)
);
