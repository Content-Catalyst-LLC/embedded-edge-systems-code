-- Edge AI quality checks

-- Latency violations
SELECT timestamp, device_id, runtime_backend, latency_ms, p95_budget_ms
FROM inference_events
WHERE latency_ms > p95_budget_ms;

-- Memory violations
SELECT timestamp, device_id, model_size_kb, flash_budget_kb, tensor_arena_kb, ram_budget_kb
FROM inference_events
WHERE memory_ok = FALSE;

-- Low confidence and fallback
SELECT timestamp, device_id, confidence, confidence_threshold, predicted_class, fallback_used, local_action
FROM inference_events
WHERE confidence < confidence_threshold OR fallback_used = TRUE;

-- Version skew
SELECT timestamp, device_id, model_version, approved_model_version
FROM inference_events
WHERE model_version != approved_model_version;

-- Backend parity failures
SELECT timestamp, device_id, runtime_backend, backend_output_delta, backend_delta_tolerance
FROM inference_events
WHERE backend_output_delta > backend_delta_tolerance;

-- Drift proxy warnings
SELECT timestamp, device_id, drift_proxy
FROM inference_events
WHERE drift_proxy > 0.15;

-- Rollback not ready
SELECT device_id, site_id, model_version, approved_model_version, rollback_ready
FROM model_inventory
WHERE rollback_ready = FALSE;
