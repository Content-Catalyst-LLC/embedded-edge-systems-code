-- Edge AI and on-device machine learning evidence schema

CREATE TABLE IF NOT EXISTS inference_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    device_class TEXT NOT NULL,
    runtime_backend TEXT NOT NULL,
    model_version TEXT NOT NULL,
    approved_model_version TEXT NOT NULL,
    feature_version TEXT NOT NULL,
    latency_ms REAL NOT NULL,
    p95_budget_ms REAL NOT NULL,
    model_size_kb REAL NOT NULL,
    flash_budget_kb REAL NOT NULL,
    tensor_arena_kb REAL NOT NULL,
    ram_budget_kb REAL NOT NULL,
    energy_mj REAL NOT NULL,
    energy_budget_mj REAL NOT NULL,
    confidence REAL NOT NULL,
    confidence_threshold REAL NOT NULL,
    predicted_class TEXT NOT NULL,
    sensor_health TEXT NOT NULL,
    fallback_used BOOLEAN NOT NULL,
    drift_proxy REAL NOT NULL,
    backend_output_delta REAL NOT NULL,
    backend_delta_tolerance REAL NOT NULL,
    memory_ok BOOLEAN NOT NULL,
    latency_ok BOOLEAN NOT NULL,
    decision_policy_version TEXT NOT NULL,
    local_action TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS backend_validation (
    test_id TEXT PRIMARY KEY,
    model_version TEXT NOT NULL,
    input_window_id TEXT NOT NULL,
    reference_output REAL NOT NULL,
    quantized_output REAL NOT NULL,
    cpu_output REAL,
    npu_output REAL,
    dsp_output REAL,
    pynq_output REAL,
    max_backend_delta REAL NOT NULL,
    backend_delta_tolerance REAL NOT NULL,
    class_agreement BOOLEAN NOT NULL,
    passed BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS model_inventory (
    device_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    device_class TEXT NOT NULL,
    approved_model_version TEXT NOT NULL,
    deployed_model_version TEXT NOT NULL,
    active_model_version TEXT NOT NULL,
    decision_used_model_version TEXT NOT NULL,
    runtime_backend TEXT NOT NULL,
    rollout_ring TEXT NOT NULL,
    rollback_ready BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS deployment_readiness_results (
    check_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_version TEXT NOT NULL,
    check_name TEXT NOT NULL,
    passed BOOLEAN NOT NULL,
    evidence_path TEXT,
    notes TEXT
);
