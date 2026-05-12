# Fleet Reliability, Reset Patterns, and Fault-Tolerance Reporting

library(readr)
library(dplyr)
library(ggplot2)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_dir <- file.path(root, "data")
out_dir <- file.path(root, "outputs")
dir.create(out_dir, showWarnings = FALSE)

faults <- read_csv(file.path(data_dir, "fault_events.csv"), show_col_types = FALSE)
resets <- read_csv(file.path(data_dir, "reset_log.csv"), show_col_types = FALSE)
fleet <- read_csv(file.path(data_dir, "device_fleet.csv"), show_col_types = FALSE)

device_reliability <- faults %>%
  group_by(device_id) %>%
  summarise(
    fault_events = n(),
    detected_events = sum(detected == TRUE),
    recovery_successes = sum(recovery_success == TRUE),
    service_loss_s = sum(service_loss_s, na.rm = TRUE),
    safe_state_entries = sum(safe_state_entered == TRUE),
    .groups = "drop"
  ) %>%
  mutate(
    detection_rate = detected_events / fault_events,
    recovery_success_rate = recovery_successes / fault_events,
    availability_estimate = pmax(0, 1 - service_loss_s / (24 * 3600))
  ) %>%
  left_join(fleet, by = "device_id") %>%
  arrange(availability_estimate, desc(fault_events))

write_csv(device_reliability, file.path(out_dir, "device_reliability_report.csv"))

reset_patterns <- resets %>%
  group_by(device_id, reset_cause, firmware_version) %>%
  summarise(
    resets = n(),
    mean_uptime_before_reset_s = mean(uptime_before_reset_s, na.rm = TRUE),
    max_watchdog_count = max(watchdog_count, na.rm = TRUE),
    persistent_state_failures = sum(persistent_state_valid == FALSE),
    .groups = "drop"
  ) %>%
  arrange(desc(resets), mean_uptime_before_reset_s)

write_csv(reset_patterns, file.path(out_dir, "fleet_reset_patterns.csv"))

p <- ggplot(device_reliability, aes(x = reorder(device_id, service_loss_s), y = service_loss_s)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Service Loss by Device",
    x = "Device",
    y = "Service loss (seconds)"
  )

ggsave(file.path(out_dir, "r_service_loss_by_device.png"), p, width = 8, height = 5, dpi = 160)

print(device_reliability)
print(reset_patterns)
