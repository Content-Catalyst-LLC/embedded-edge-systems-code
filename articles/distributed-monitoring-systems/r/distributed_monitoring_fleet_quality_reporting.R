suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

article_root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
output_dir <- file.path(article_root, "outputs")
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

telemetry_path <- file.path(output_dir, "python_fault_containment_telemetry_evaluation.csv")
coverage_path <- file.path(output_dir, "python_inference_boundary_coverage_evaluation.csv")
gateway_path <- file.path(output_dir, "python_gateways_scored.csv")

if (!file.exists(telemetry_path)) {
  stop("Run python workflows first.")
}

telemetry_records <- read_csv(telemetry_path, show_col_types = FALSE)
coverage <- read_csv(coverage_path, show_col_types = FALSE)
gateways <- read_csv(gateway_path, show_col_types = FALSE)

monitoring_summary <- telemetry_records |>
  group_by(site_id, coverage_zone, gateway_id, sensor_family) |>
  summarise(
    nodes = n_distinct(node_id),
    telemetry_records = n(),
    usable_telemetry_rate = mean(usable == TRUE, na.rm = TRUE),
    stale_telemetry_rate = mean(fresh == FALSE, na.rm = TRUE),
    valid_quality_rate = mean(quality_state == "valid", na.rm = TRUE),
    clock_skew_violation_rate = mean(synchronized == FALSE, na.rm = TRUE),
    duplicate_replay_rate = mean(duplicate_detected == TRUE, na.rm = TRUE),
    diagnostic_or_restricted_rate = mean(normal_monitoring_allowed == FALSE, na.rm = TRUE),
    mean_freshness_seconds = mean(freshness_seconds, na.rm = TRUE),
    p95_freshness_seconds = quantile(freshness_seconds, 0.95, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(monitoring_summary, file.path(output_dir, "r_distributed_monitoring_quality_summary.csv"))

coverage_summary <- coverage |>
  group_by(site_id) |>
  summarise(
    zones = n(),
    coverage_complete_rate = mean(coverage_complete == TRUE, na.rm = TRUE),
    system_claim_allowed_zone_rate = mean(system_claim_allowed == TRUE, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(coverage_summary, file.path(output_dir, "r_coverage_summary.csv"))

plot <- ggplot(telemetry_records, aes(x = sensor_family, y = freshness_seconds)) +
  geom_point(size = 3) +
  labs(
    title = "Distributed Monitoring Freshness by Sensor Family",
    x = "Sensor family",
    y = "Freshness (seconds)"
  )

ggsave(
  filename = file.path(output_dir, "r_monitoring_freshness_by_sensor_family.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(monitoring_summary)
