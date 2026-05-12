# Runtime Trace and Fleet Timing Analysis

library(readr)
library(dplyr)
library(ggplot2)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_dir <- file.path(root, "data")
out_dir <- file.path(root, "outputs")
dir.create(out_dir, showWarnings = FALSE)

runtime <- read_csv(file.path(data_dir, "runtime_trace.csv"), show_col_types = FALSE)
queues <- read_csv(file.path(data_dir, "queue_trace.csv"), show_col_types = FALSE)
fleet <- read_csv(file.path(data_dir, "rtos_fleet_telemetry.csv"), show_col_types = FALSE)

runtime_report <- runtime %>%
  mutate(
    runtime_ms = finish_ms - start_ms,
    completion_slack_ms = deadline_ms - finish_ms
  ) %>%
  group_by(device_id, firmware_version, task_name) %>%
  summarise(
    activations = n(),
    deadline_misses = sum(deadline_miss, na.rm = TRUE),
    mean_runtime_ms = mean(runtime_ms, na.rm = TRUE),
    max_runtime_ms = max(runtime_ms, na.rm = TRUE),
    min_completion_slack_ms = min(completion_slack_ms, na.rm = TRUE),
    max_isr_time_us = max(isr_time_us, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(desc(deadline_misses), min_completion_slack_ms)

write_csv(runtime_report, file.path(out_dir, "r_runtime_deadline_report.csv"))

queue_report <- queues %>%
  mutate(
    pressure_ratio = high_water_mark / capacity,
    queue_risk = case_when(
      overflow_count > 0 ~ "overflow_observed",
      pressure_ratio >= 0.9 ~ "near_capacity",
      pressure_ratio >= 0.75 ~ "elevated_pressure",
      TRUE ~ "normal"
    )
  ) %>%
  arrange(desc(pressure_ratio), desc(overflow_count))

write_csv(queue_report, file.path(out_dir, "r_queue_pressure_report.csv"))

fleet_report <- fleet %>%
  mutate(
    timing_risk = case_when(
      watchdog_resets > 0 ~ "watchdog_reset_risk",
      deadline_misses_24h > 0 ~ "deadline_miss_risk",
      queue_overflows_24h > 0 ~ "queue_overflow_risk",
      min_stack_watermark_bytes < 512 ~ "stack_watermark_risk",
      max_isr_time_us > 250 ~ "isr_latency_risk",
      idle_residency_pct < 70 ~ "low_idle_residency",
      TRUE ~ "normal"
    )
  ) %>%
  arrange(desc(deadline_misses_24h), desc(queue_overflows_24h), min_stack_watermark_bytes)

write_csv(fleet_report, file.path(out_dir, "r_rtos_fleet_timing_risk_report.csv"))

firmware_summary <- fleet_report %>%
  group_by(firmware_version, board_revision) %>%
  summarise(
    devices = n(),
    total_deadline_misses = sum(deadline_misses_24h, na.rm = TRUE),
    total_queue_overflows = sum(queue_overflows_24h, na.rm = TRUE),
    min_stack_watermark_bytes = min(min_stack_watermark_bytes, na.rm = TRUE),
    max_isr_time_us = max(max_isr_time_us, na.rm = TRUE),
    mean_idle_residency_pct = mean(idle_residency_pct, na.rm = TRUE),
    watchdog_resets = sum(watchdog_resets, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(desc(total_deadline_misses), desc(total_queue_overflows))

write_csv(firmware_summary, file.path(out_dir, "r_firmware_timing_summary.csv"))

p1 <- ggplot(fleet_report, aes(x = reorder(device_id, deadline_misses_24h), y = deadline_misses_24h)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Deadline Misses by Device",
    x = "Device",
    y = "Deadline misses / 24h"
  )

ggsave(file.path(out_dir, "r_deadline_misses_by_device.png"), p1, width = 8, height = 5, dpi = 160)

p2 <- ggplot(fleet_report, aes(x = reorder(device_id, min_stack_watermark_bytes), y = min_stack_watermark_bytes)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Minimum Stack Watermark by Device",
    x = "Device",
    y = "Stack watermark bytes"
  )

ggsave(file.path(out_dir, "r_stack_watermark_by_device.png"), p2, width = 8, height = 5, dpi = 160)

print(runtime_report)
print(queue_report)
print(fleet_report)
