# R Workflow: Autonomy Monitoring, Drift, and Mission Reliability Reporting

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

script_path <- tryCatch(normalizePath(sys.frame(1)$ofile), error = function(e) "")
article_root <- if (nzchar(script_path)) normalizePath(file.path(dirname(script_path), "..")) else getwd()
data_path <- file.path(article_root, "data", "sample_autonomy_events.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

autonomy_events <- read_csv(data_path, show_col_types = FALSE)

autonomy_summary <- autonomy_events |>
  group_by(device_id, mission_type, autonomy_level) |>
  summarise(
    decisions = n(),
    mean_confidence = mean(decision_confidence, na.rm = TRUE),
    fallback_rate = mean(action_type == "fallback", na.rm = TRUE),
    intervention_rate = mean(human_intervention_required, na.rm = TRUE),
    latency_violation_rate = mean(latency_ms > latency_budget_ms, na.rm = TRUE),
    safety_events = sum(safety_state != "normal", na.rm = TRUE),
    input_drift_index = mean(input_drift_score, na.rm = TRUE),
    confidence_drift_index = mean(confidence_drift_score, na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(fallback_rate), desc(intervention_rate), desc(input_drift_index))

write_csv(autonomy_summary, file.path(output_dir, "r_autonomy_monitoring_summary.csv"))

plot <- ggplot(autonomy_events, aes(x = device_id, y = decision_confidence)) +
  geom_point(size = 3) +
  labs(
    title = "Decision Confidence by Autonomous Edge Device",
    x = "Device",
    y = "Decision confidence"
  )

ggsave(
  filename = file.path(output_dir, "r_decision_confidence_by_device.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(autonomy_summary)
