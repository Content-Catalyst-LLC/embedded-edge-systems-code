suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

article_root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
output_dir <- file.path(article_root, "outputs")
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

edge_inventory <- read_csv(file.path(article_root, "data", "sample_edge_fleet_inventory.csv"), show_col_types = FALSE)

edge_fleet_summary <- edge_inventory |>
  mutate(
    latency_violation = latency_ms > latency_budget_ms,
    version_skew = active_version != approved_version,
    trust_verified = trust_state == "verified",
    runtime_assurance_ready = runtime_assurance_state == "ready",
    resource_pressure = cpu_utilization > 0.85 | memory_utilization > 0.85 | storage_utilization > 0.90 | thermal_state != "normal"
  ) |>
  group_by(site_id, layer, hardware_class, workload_family) |>
  summarise(
    assets = n(),
    online_rate = mean(connectivity_state == "online", na.rm = TRUE),
    degraded_rate = mean(health_state == "degraded", na.rm = TRUE),
    p95_latency_ms = quantile(latency_ms, 0.95, na.rm = TRUE),
    latency_violation_rate = mean(latency_violation, na.rm = TRUE),
    mean_buffer_backlog = mean(buffer_backlog, na.rm = TRUE),
    offline_ready_rate = mean(offline_ready == TRUE, na.rm = TRUE),
    version_skew_rate = mean(version_skew, na.rm = TRUE),
    trust_verified_rate = mean(trust_verified, na.rm = TRUE),
    runtime_assurance_ready_rate = mean(runtime_assurance_ready, na.rm = TRUE),
    watchdog_reset_rate = mean(watchdog_resets > 0, na.rm = TRUE),
    resource_pressure_rate = mean(resource_pressure, na.rm = TRUE),
    rollback_ready_rate = mean(rollback_ready == TRUE, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(edge_fleet_summary, file.path(output_dir, "r_edge_fleet_reporting_architecture_health_summary.csv"))

plot <- ggplot(edge_inventory, aes(x = layer, y = latency_ms)) +
  geom_point(size = 3) +
  labs(title = "Edge Architecture Latency by Layer", x = "Layer", y = "Latency (ms)")

ggsave(file.path(output_dir, "r_edge_architecture_latency_by_layer.png"), plot = plot, width = 9, height = 5, dpi = 150)

print(edge_fleet_summary)
