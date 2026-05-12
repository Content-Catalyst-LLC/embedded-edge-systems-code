suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

article_root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
output_dir <- file.path(article_root, "outputs")
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

telemetry_path <- file.path(output_dir, "python_telemetry_records_scored.csv")
fleet_path <- file.path(output_dir, "python_device_inventory_scored.csv")
gateway_path <- file.path(output_dir, "python_gateway_state_scored.csv")

if (!file.exists(telemetry_path)) {
  stop("Run python/iot_sensor_fleet_architecture_analysis.py first.")
}

telemetry_records <- read_csv(telemetry_path, show_col_types = FALSE)
fleet <- read_csv(fleet_path, show_col_types = FALSE)
gateways <- read_csv(gateway_path, show_col_types = FALSE)

fleet_summary <- telemetry_records |>
  group_by(site_id, gateway_id, sensor_family) |>
  summarise(
    devices = n_distinct(device_id),
    telemetry_records = n(),
    usable_telemetry_rate = mean(usable == TRUE, na.rm = TRUE),
    stale_telemetry_rate = mean(fresh == FALSE, na.rm = TRUE),
    duplicate_replay_rate = mean(duplicate_detected == TRUE, na.rm = TRUE),
    valid_quality_rate = mean(quality_state == "valid", na.rm = TRUE),
    trusted_rate = mean(trust_state == "verified", na.rm = TRUE),
    firmware_compliance_rate = mean(active_firmware == approved_firmware, na.rm = TRUE),
    configuration_compliance_rate = mean(active_config == approved_config, na.rm = TRUE),
    schema_compliance_rate = mean(active_schema == approved_schema, na.rm = TRUE),
    mean_freshness_seconds = mean(freshness_seconds, na.rm = TRUE),
    p95_freshness_seconds = quantile(freshness_seconds, 0.95, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(fleet_summary, file.path(output_dir, "r_iot_sensor_fleet_health_summary.csv"))

gateway_summary <- gateways |>
  transmute(
    gateway_id,
    site_id,
    buffer_pressure,
    child_reporting_rate,
    rule_compliant,
    firmware_compliant,
    trust_state
  )

write_csv(gateway_summary, file.path(output_dir, "r_gateway_health_summary.csv"))

plot <- ggplot(telemetry_records, aes(x = sensor_family, y = freshness_seconds)) +
  geom_point(size = 3) +
  labs(
    title = "Telemetry Freshness by Sensor Family",
    x = "Sensor family",
    y = "Freshness (seconds)"
  )

ggsave(
  filename = file.path(output_dir, "r_telemetry_freshness_by_sensor_family.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(fleet_summary)
