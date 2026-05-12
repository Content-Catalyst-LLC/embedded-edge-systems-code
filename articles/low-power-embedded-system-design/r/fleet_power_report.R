# Fleet Power Reporting and Battery-Risk Review

library(readr)
library(dplyr)
library(ggplot2)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_dir <- file.path(root, "data")
out_dir <- file.path(root, "outputs")
dir.create(out_dir, showWarnings = FALSE)

telemetry <- read_csv(file.path(data_dir, "device_power_telemetry.csv"), show_col_types = FALSE)

fleet_power <- telemetry %>%
  mutate(
    battery_risk = case_when(
      battery_v < 3.45 ~ "critical_low_voltage",
      retry_count_24h > 8 ~ "radio_retry_risk",
      false_wake_count_24h > 10 ~ "wake_storm_risk",
      sleep_residency_pct < 92 ~ "poor_sleep_residency",
      brownout_count > 0 ~ "brownout_observed",
      TRUE ~ "normal"
    ),
    communications_pressure = tx_count_24h + retry_count_24h
  ) %>%
  arrange(battery_v, desc(retry_count_24h), desc(false_wake_count_24h))

write_csv(fleet_power, file.path(out_dir, "r_fleet_power_risk_report.csv"))

firmware_summary <- fleet_power %>%
  group_by(firmware_version) %>%
  summarise(
    devices = n(),
    mean_battery_v = mean(battery_v, na.rm = TRUE),
    mean_sleep_residency_pct = mean(sleep_residency_pct, na.rm = TRUE),
    total_retries = sum(retry_count_24h, na.rm = TRUE),
    total_brownouts = sum(brownout_count, na.rm = TRUE),
    total_false_wakes = sum(false_wake_count_24h, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(mean_sleep_residency_pct)

write_csv(firmware_summary, file.path(out_dir, "r_firmware_power_summary.csv"))

p1 <- ggplot(fleet_power, aes(x = reorder(device_id, battery_v), y = battery_v)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Battery Voltage by Device",
    x = "Device",
    y = "Battery voltage"
  )

ggsave(file.path(out_dir, "r_battery_voltage_by_device.png"), p1, width = 8, height = 5, dpi = 160)

p2 <- ggplot(fleet_power, aes(x = reorder(device_id, false_wake_count_24h), y = false_wake_count_24h)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "False Wake Count by Device",
    x = "Device",
    y = "False wakes / 24h"
  )

ggsave(file.path(out_dir, "r_false_wake_count_by_device.png"), p2, width = 8, height = 5, dpi = 160)

print(fleet_power)
print(firmware_summary)
