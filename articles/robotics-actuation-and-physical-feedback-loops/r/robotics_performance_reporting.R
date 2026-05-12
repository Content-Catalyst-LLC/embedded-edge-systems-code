# R Workflow: Actuator Performance, Tracking Error, and Reliability Reporting

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

robotics_summary <- control_logs |>
  group_by(robot_id, joint_id, task_mode) |>
  summarise(
    samples = n(),
    mean_abs_error = mean(abs(tracking_error), na.rm = TRUE),
    max_abs_error = max(abs(tracking_error), na.rm = TRUE),
    saturation_rate = mean(saturated, na.rm = TRUE),
    mean_loop_jitter_ms = mean(loop_jitter_ms, na.rm = TRUE),
    max_loop_jitter_ms = max(loop_jitter_ms, na.rm = TRUE),
    safety_events = sum(safety_state != "normal", na.rm = TRUE),
    faults = sum(fault_state != "normal", na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(max_abs_error), desc(saturation_rate))

write_csv(robotics_summary, file.path(output_dir, "r_robotics_performance_summary.csv"))

plot <- ggplot(control_logs, aes(x = joint_id, y = abs(tracking_error))) +
  geom_point(size = 3) +
  labs(
    title = "Tracking Error by Joint",
    x = "Joint",
    y = "Absolute tracking error"
  )

ggsave(
  filename = file.path(output_dir, "r_tracking_error_by_joint.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(robotics_summary)
