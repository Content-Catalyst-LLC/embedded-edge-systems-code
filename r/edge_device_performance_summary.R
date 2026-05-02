# Edge Device Performance Summary
# -------------------------------
#
# Summarizes device-level signal quality and readiness for transmission.

library(readr)
library(dplyr)

project_root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
input_path <- file.path(project_root, "data", "processed", "edge_telemetry.csv")
output_tables_dir <- file.path(project_root, "outputs", "tables")

dir.create(output_tables_dir, recursive = TRUE, showWarnings = FALSE)

telemetry <- read_csv(input_path, show_col_types = FALSE)

performance_summary <- telemetry |>
  mutate(
    transmission_ready = !is.na(observed_value) &
      battery_voltage >= 3.3 &
      signal_quality >= 0.80
  ) |>
  group_by(device_id) |>
  summarise(
    records = n(),
    readiness_rate = mean(transmission_ready),
    lowest_battery_voltage = min(battery_voltage, na.rm = TRUE),
    lowest_signal_quality = min(signal_quality, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(
  performance_summary,
  file.path(output_tables_dir, "edge_device_performance_summary.csv")
)

print(performance_summary)
