# Environmental Sensor Network Reporting and Data-Quality Review

library(readr)
library(dplyr)
library(ggplot2)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_dir <- file.path(root, "data")
out_dir <- file.path(root, "outputs")
dir.create(out_dir, showWarnings = FALSE)

measurements <- read_csv(file.path(data_dir, "environmental_measurements.csv"), show_col_types = FALSE)
nodes <- read_csv(file.path(data_dir, "nodes.csv"), show_col_types = FALSE)
calibrations <- read_csv(file.path(data_dir, "calibration_records.csv"), show_col_types = FALSE)

quality_by_site <- measurements %>%
  group_by(site_id, node_id, parameter) %>%
  summarise(
    records = n(),
    warning_records = sum(!quality_flag %in% c("valid", "event_valid")),
    warning_rate = warning_records / records,
    min_battery_v = min(battery_v, na.rm = TRUE),
    mean_link_quality = mean(link_quality, na.rm = TRUE),
    max_buffer_age_s = max(buffer_age_s, na.rm = TRUE),
    retry_total = sum(packet_retries, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  left_join(nodes %>% select(node_id, maintenance_status, last_maintenance_date), by = "node_id") %>%
  arrange(desc(warning_rate), desc(max_buffer_age_s))

write_csv(quality_by_site, file.path(out_dir, "environmental_quality_by_site.csv"))

p1 <- ggplot(quality_by_site, aes(x = reorder(node_id, warning_rate), y = warning_rate)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Environmental Network Warning Rate by Node",
    x = "Node",
    y = "Warning rate"
  )

ggsave(file.path(out_dir, "environmental_warning_rate_by_node.png"), p1, width = 8, height = 5, dpi = 160)

calibration_summary <- calibrations %>%
  mutate(
    valid_until = as.Date(valid_until),
    days_until_expiry = as.integer(valid_until - as.Date("2026-03-28")),
    calibration_risk = case_when(
      days_until_expiry < 0 ~ "expired",
      days_until_expiry < 30 ~ "expires_soon",
      TRUE ~ "current"
    )
  )

write_csv(calibration_summary, file.path(out_dir, "calibration_review.csv"))

print(quality_by_site)
print(calibration_summary)
