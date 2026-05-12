# R Workflow: Edge AI Fleet Monitoring and Model Performance Reporting

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

script_path <- tryCatch(normalizePath(sys.frame(1)$ofile), error = function(e) "")
article_root <- if (nzchar(script_path)) normalizePath(file.path(dirname(script_path), "..")) else getwd()
data_path <- file.path(article_root, "data", "sample_inference_events.csv")
backend_path <- file.path(article_root, "data", "backend_validation_report.csv")
inventory_path <- file.path(article_root, "data", "model_inventory.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

inference_events <- read_csv(data_path, show_col_types = FALSE)
backend_validation <- read_csv(backend_path, show_col_types = FALSE)
model_inventory <- read_csv(inventory_path, show_col_types = FALSE)

edge_ai_summary <- inference_events |>
  group_by(device_class, model_version, runtime_backend) |>
  summarise(
    events = n(),
    mean_latency_ms = mean(latency_ms, na.rm = TRUE),
    p95_latency_ms = quantile(latency_ms, 0.95, na.rm = TRUE),
    p99_latency_ms = quantile(latency_ms, 0.99, na.rm = TRUE),
    mean_confidence = mean(confidence, na.rm = TRUE),
    low_confidence_rate = mean(confidence < confidence_threshold, na.rm = TRUE),
    fallback_rate = mean(fallback_used == TRUE, na.rm = TRUE),
    model_skew_rate = mean(model_version != approved_model_version, na.rm = TRUE),
    drift_proxy_mean = mean(drift_proxy, na.rm = TRUE),
    backend_delta_p95 = quantile(backend_output_delta, 0.95, na.rm = TRUE),
    memory_violation_rate = mean(memory_ok == FALSE, na.rm = TRUE),
    latency_violation_rate = mean(latency_ok == FALSE, na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(fallback_rate), desc(backend_delta_p95), desc(p95_latency_ms))

write_csv(edge_ai_summary, file.path(output_dir, "r_edge_ai_fleet_monitoring_summary.csv"))

backend_summary <- backend_validation |>
  summarise(
    tests = n(),
    backend_pass_rate = mean(passed == TRUE, na.rm = TRUE),
    class_agreement_rate = mean(class_agreement == TRUE, na.rm = TRUE),
    max_backend_delta = max(max_backend_delta, na.rm = TRUE)
  )

write_csv(backend_summary, file.path(output_dir, "r_backend_validation_summary.csv"))

version_summary <- model_inventory |>
  summarise(
    fleet_devices = n(),
    deployed_version_skew_rate = mean(deployed_model_version != approved_model_version, na.rm = TRUE),
    active_version_skew_rate = mean(active_model_version != approved_model_version, na.rm = TRUE),
    decision_used_version_skew_rate = mean(decision_used_model_version != approved_model_version, na.rm = TRUE),
    rollback_ready_rate = mean(rollback_ready == TRUE, na.rm = TRUE)
  )

write_csv(version_summary, file.path(output_dir, "r_model_version_skew_summary.csv"))

plot <- ggplot(inference_events, aes(x = runtime_backend, y = latency_ms)) +
  geom_point(size = 3) +
  labs(
    title = "Edge AI Inference Latency by Runtime Backend",
    x = "Runtime backend",
    y = "Latency (ms)"
  )

ggsave(
  filename = file.path(output_dir, "r_edge_ai_latency_by_runtime_backend.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(edge_ai_summary)
