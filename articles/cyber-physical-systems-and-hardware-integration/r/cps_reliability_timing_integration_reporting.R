# R Workflow: CPS Reliability, Timing, Traceability, and Integration Reporting

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

script_path <- tryCatch(normalizePath(sys.frame(1)$ofile), error = function(e) "")
article_root <- if (nzchar(script_path)) normalizePath(file.path(dirname(script_path), "..")) else getwd()
data_path <- file.path(article_root, "data", "sample_cps_events.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

cps_events <- read_csv(data_path, show_col_types = FALSE)

cps_summary <- cps_events |>
  group_by(device_id, subsystem, operating_mode) |>
  summarise(
    events = n(),
    mean_sensor_age_ms = mean(sensor_age_ms, na.rm = TRUE),
    deadline_miss_rate = mean(deadline_missed, na.rm = TRUE),
    mean_jitter_ms = mean(loop_jitter_ms, na.rm = TRUE),
    min_deadline_slack_ms = min(deadline_slack_ms, na.rm = TRUE),
    actuator_saturation_rate = mean(actuator_saturated, na.rm = TRUE),
    safety_filter_rate = mean(candidate_command != filtered_command, na.rm = TRUE),
    interface_error_rate = mean(interface_error, na.rm = TRUE),
    uncertainty_warning_rate = mean(total_uncertainty > uncertainty_budget, na.rm = TRUE),
    safety_events = sum(safety_state != "normal", na.rm = TRUE),
    recovery_events = sum(recovery_event, na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(deadline_miss_rate), desc(interface_error_rate), desc(safety_events))

write_csv(cps_summary, file.path(output_dir, "r_cps_reliability_timing_integration_summary.csv"))

traceability_path <- file.path(article_root, "data", "requirements_traceability_matrix.csv")
traceability <- read_csv(traceability_path, show_col_types = FALSE)

traceability_summary <- traceability |>
  count(status, name = "requirements") |>
  mutate(share = requirements / sum(requirements))

write_csv(traceability_summary, file.path(output_dir, "r_traceability_coverage_summary.csv"))

plot <- ggplot(cps_events, aes(x = subsystem, y = deadline_slack_ms)) +
  geom_point(size = 3) +
  labs(
    title = "CPS Deadline Slack by Subsystem",
    x = "Subsystem",
    y = "Deadline slack (ms)"
  )

ggsave(
  filename = file.path(output_dir, "r_cps_deadline_slack_by_subsystem.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(cps_summary)
