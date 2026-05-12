# Firmware Telemetry and Driver Reliability Reporting

library(readr)
library(dplyr)
library(ggplot2)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_dir <- file.path(root, "data")
out_dir <- file.path(root, "outputs")
dir.create(out_dir, showWarnings = FALSE)

telemetry <- read_csv(file.path(data_dir, "firmware_fleet_telemetry.csv"), show_col_types = FALSE)
events <- read_csv(file.path(data_dir, "device_lifecycle_events.csv"), show_col_types = FALSE)

fleet_report <- telemetry %>%
  mutate(
    firmware_risk = case_when(
      rollback_count > 0 ~ "rollback_observed",
      suspend_resume_failures > 2 ~ "suspend_resume_risk",
      driver_errors > 3 ~ "driver_error_risk",
      bus_timeouts > 5 ~ "bus_timeout_risk",
      watchdog_resets > 1 ~ "watchdog_reset_risk",
      TRUE ~ "normal"
    ),
    total_control_faults = watchdog_resets + brownout_count + bus_timeouts + driver_errors + suspend_resume_failures
  ) %>%
  arrange(desc(total_control_faults), firmware_version)

write_csv(fleet_report, file.path(out_dir, "r_firmware_fleet_report.csv"))

firmware_summary <- fleet_report %>%
  group_by(firmware_version, board_revision) %>%
  summarise(
    devices = n(),
    total_boots = sum(boot_count, na.rm = TRUE),
    total_watchdog_resets = sum(watchdog_resets, na.rm = TRUE),
    total_bus_timeouts = sum(bus_timeouts, na.rm = TRUE),
    total_driver_errors = sum(driver_errors, na.rm = TRUE),
    total_suspend_resume_failures = sum(suspend_resume_failures, na.rm = TRUE),
    total_rollbacks = sum(rollback_count, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(desc(total_driver_errors), desc(total_suspend_resume_failures))

write_csv(firmware_summary, file.path(out_dir, "r_firmware_version_summary.csv"))

driver_event_summary <- events %>%
  group_by(driver_id, event_type, result) %>%
  summarise(
    events = n(),
    mean_latency_ms = mean(latency_ms, na.rm = TRUE),
    max_latency_ms = max(latency_ms, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(driver_id, desc(events))

write_csv(driver_event_summary, file.path(out_dir, "r_driver_event_summary.csv"))

p1 <- ggplot(fleet_report, aes(x = reorder(device_id, total_control_faults), y = total_control_faults)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Firmware Control Faults by Device",
    x = "Device",
    y = "Total control faults"
  )

ggsave(file.path(out_dir, "r_firmware_control_faults_by_device.png"), p1, width = 8, height = 5, dpi = 160)

p2 <- ggplot(firmware_summary, aes(x = firmware_version, y = total_driver_errors)) +
  geom_col() +
  labs(
    title = "Driver Errors by Firmware Version",
    x = "Firmware version",
    y = "Driver errors"
  )

ggsave(file.path(out_dir, "r_driver_errors_by_firmware_version.png"), p2, width = 8, height = 5, dpi = 160)

print(fleet_report)
print(firmware_summary)
