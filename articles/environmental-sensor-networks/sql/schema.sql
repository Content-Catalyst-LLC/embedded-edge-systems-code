CREATE TABLE environmental_sites (
  site_id TEXT PRIMARY KEY,
  site_name TEXT NOT NULL,
  site_type TEXT NOT NULL,
  latitude REAL NOT NULL,
  longitude REAL NOT NULL,
  representativeness TEXT,
  access_risk TEXT,
  notes TEXT
);

CREATE TABLE environmental_nodes (
  node_id TEXT PRIMARY KEY,
  site_id TEXT NOT NULL,
  node_class TEXT NOT NULL,
  firmware_version TEXT,
  radio_type TEXT,
  power_profile TEXT,
  battery_wh REAL,
  solar_watts REAL,
  install_date DATE,
  last_maintenance_date DATE,
  maintenance_status TEXT,
  FOREIGN KEY (site_id) REFERENCES environmental_sites(site_id)
);

CREATE TABLE calibration_records (
  calibration_version TEXT PRIMARY KEY,
  node_id TEXT NOT NULL,
  parameter TEXT NOT NULL,
  calibrated_at DATE NOT NULL,
  valid_until DATE,
  method TEXT,
  reference TEXT,
  technician TEXT,
  status TEXT,
  FOREIGN KEY (node_id) REFERENCES environmental_nodes(node_id)
);

CREATE TABLE environmental_measurements (
  event_id TEXT PRIMARY KEY,
  node_id TEXT NOT NULL,
  site_id TEXT NOT NULL,
  parameter TEXT NOT NULL,
  units TEXT NOT NULL,
  acquisition_time TIMESTAMP NOT NULL,
  processing_time TIMESTAMP,
  value REAL NOT NULL,
  quality_flag TEXT NOT NULL,
  calibration_version TEXT,
  battery_v REAL,
  link_quality REAL,
  packet_retries INTEGER,
  buffer_age_s REAL,
  event_mode TEXT,
  FOREIGN KEY (node_id) REFERENCES environmental_nodes(node_id),
  FOREIGN KEY (site_id) REFERENCES environmental_sites(site_id)
);

CREATE TABLE node_health_events (
  health_event_id TEXT PRIMARY KEY,
  node_id TEXT NOT NULL,
  event_time TIMESTAMP NOT NULL,
  battery_v REAL,
  solar_input_w REAL,
  link_quality REAL,
  buffer_occupancy INTEGER,
  watchdog_resets INTEGER,
  enclosure_intrusion BOOLEAN,
  notes TEXT,
  FOREIGN KEY (node_id) REFERENCES environmental_nodes(node_id)
);
