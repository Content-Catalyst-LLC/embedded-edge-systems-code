-- Candidate platforms with low memory or lifecycle margin.
SELECT
  platform_id,
  platform_name,
  platform_type,
  flash_kb,
  sram_kb,
  lifecycle_support_score
FROM candidate_platforms
WHERE sram_kb < 256
   OR flash_kb < 512
   OR lifecycle_support_score < 7
ORDER BY lifecycle_support_score ASC, sram_kb ASC;

-- Recommended candidate platforms by device class.
SELECT
  device_class,
  platform_id,
  fit_score,
  compute_margin_mhz,
  sram_margin_kb,
  bandwidth_margin_mb_s,
  peripheral_fit,
  security_fit,
  lifecycle_fit
FROM silicon_fit_results
WHERE recommended = TRUE
ORDER BY device_class, fit_score DESC;

-- Events that need lifecycle or security review.
SELECT *
FROM platform_lifecycle_events
WHERE update_result <> 'success'
   OR diagnostic_status <> 'normal'
   OR security_state <> 'locked';
