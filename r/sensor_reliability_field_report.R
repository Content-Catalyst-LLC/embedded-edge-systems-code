# Sensor Reliability and Field Performance Report
# -----------------------------------------------
#
# Reads processed edge telemetry and produces field reliability summaries.

library(readr)
library(dplyr)
library(ggplot2)

project_root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
input_path <- file.path(project_root, "data", "processed", "edge_telemetry.csv")
output_tables_dir <- file.path(project_root, "outputs", "tables")
output_figures_dir <- file.path(project_root, "outputs", "figures")

dir.create(output_tables_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(output_figures_dir, recursive = TRUE, showWarnings = FALSE)

telemetry <- read_csv(input_path, show_col_types = FALSE)

device_summary <- telemetry |>
  group_by(device_id, sensor_type) |>
  summarise(
    records = n(),
    missing_values = sum(is.na(observed_value)),
    mean_observed_value = mean(observed_value, na.rm = TRUE),
    mean_battery_voltage = mean(battery_voltage, na.rm = TRUE),
    mean_signal_quality = mean(signal_quality, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(
  device_summary,
  file.path(output_tables_dir, "sensor_reliability_field_summary.csv")
)

battery_plot <- ggplot(device_summary, aes(x = device_id, y = mean_battery_voltage)) +
  geom_col() +
  labs(
    title = "Mean Battery Voltage by Edge Device",
    x = "Device ID",
    y = "Mean battery voltage"
  ) +
  theme_minimal()

ggsave(
  filename = file.path(output_figures_dir, "mean_battery_voltage_by_device.png"),
  plot = battery_plot,
  width = 8,
  height = 5,
  dpi = 300
)

print(device_summary)
