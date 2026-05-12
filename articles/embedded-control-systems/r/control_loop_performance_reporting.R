# R Workflow: Control-Loop Performance and Reliability Reporting

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

script_path <- tryCatch(normalizePath(sys.frame(1)$ofile), error = function(e) "")
article_root <- if (nzchar(script_path)) normalizePath(file.path(dirname(script_path), "..")) else getwd()
data_path <- file.path(article_root, "data", "sample_control_loop_log.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

control_logs <- read_csv(data_path, show_col_types = FALSE)

control_summary <- control_logs |>
  group_by(device_id, loop_id, operating_mode) |>
  summarise(
    samples = n(),
    mean_abs_error = mean(abs(control_error), na.rm = TRUE),
    max_abs_error = max(abs(control_error), na.rm = TRUE),
    saturation_rate = mean(saturated, na.rm = TRUE),
    safety_filter_rate = mean(candidate_command != filtered_command, na.rm = TRUE),
    deadline_miss_rate = mean(deadline_missed, na.rm = TRUE),
    mean_loop_jitter_ms = mean(loop_jitter_ms, na.rm = TRUE),
    min_deadline_slack_ms = min(deadline_slack_ms, na.rm = TRUE),
    safety_events = sum(safety_state != "normal", na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(saturation_rate), desc(deadline_miss_rate), desc(mean_abs_error))

write_csv(control_summary, file.path(output_dir, "r_control_loop_performance_summary.csv"))

plot <- ggplot(control_logs, aes(x = loop_id, y = abs(control_error))) +
  geom_point(size = 3) +
  labs(
    title = "Control Error by Loop",
    x = "Control loop",
    y = "Absolute control error"
  )

ggsave(
  filename = file.path(output_dir, "r_control_error_by_loop.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(control_summary)
