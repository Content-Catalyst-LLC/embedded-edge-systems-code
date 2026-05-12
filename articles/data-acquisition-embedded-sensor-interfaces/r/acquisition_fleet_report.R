# Fleet-Level Sensor Quality and Measurement Reliability Reporting

library(readr)
library(dplyr)
library(ggplot2)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_dir <- file.path(root, "data")
out_dir <- file.path(root, "outputs")
dir.create(out_dir, showWarnings = FALSE)

events <- read_csv(file.path(data_dir, "acquisition_events.csv"), show_col_types = FALSE)

report <- events %>%
  group_by(site_id, device_id) %>%
  summarise(
    measurements = n(),
    warning_events = sum(quality_flag != "valid"),
    warning_rate = warning_events / measurements,
    max_timestamp_jitter_ms = max(timestamp_jitter_ms, na.rm = TRUE),
    max_buffer_age_ms = max(buffer_age_ms, na.rm = TRUE),
    bus_retries = sum(bus_retries, na.rm = TRUE),
    stale_reads = sum(stale_read, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(desc(warning_rate), desc(max_timestamp_jitter_ms))

write_csv(report, file.path(out_dir, "fleet_acquisition_reliability_report.csv"))

p <- ggplot(report, aes(x = reorder(device_id, warning_rate), y = warning_rate)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Acquisition Warning Rate by Device",
    x = "Device",
    y = "Warning rate"
  )

ggsave(file.path(out_dir, "fleet_acquisition_warning_rate.png"), p, width = 8, height = 5, dpi = 160)

print(report)
