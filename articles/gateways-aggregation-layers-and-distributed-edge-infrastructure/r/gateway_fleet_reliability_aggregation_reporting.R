# R Workflow: Gateway Fleet Reliability and Aggregation Reporting

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

script_path <- tryCatch(normalizePath(sys.frame(1)$ofile), error = function(e) "")
article_root <- if (nzchar(script_path)) normalizePath(file.path(dirname(script_path), "..")) else getwd()
data_path <- file.path(article_root, "data", "sample_gateway_events.csv")
site_state_path <- file.path(article_root, "data", "site_state_events.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

gateway_events <- read_csv(data_path, show_col_types = FALSE)
site_state <- read_csv(site_state_path, show_col_types = FALSE)

gateway_summary <- gateway_events |>
  group_by(site_id, gateway_id, protocol_family) |>
  summarise(
    events = n(),
    mean_buffer_backlog = mean(buffer_backlog, na.rm = TRUE),
    max_replay_lag_s = max(replay_lag_s, na.rm = TRUE),
    stale_device_rate = mean(device_freshness_s > 60, na.rm = TRUE),
    missing_child_rate = mean(child_device_status == "missing", na.rm = TRUE),
    protocol_error_rate = mean(protocol_error == TRUE, na.rm = TRUE),
    selective_uplink_rate = mean(forwarded_upstream == TRUE, na.rm = TRUE),
    lineage_completeness_rate = mean(lineage_complete == TRUE, na.rm = TRUE),
    context_loss_events = sum(lineage_complete == FALSE, na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(protocol_error_rate), desc(missing_child_rate), desc(mean_buffer_backlog))

write_csv(gateway_summary, file.path(output_dir, "r_gateway_fleet_reliability_aggregation_summary.csv"))

site_summary <- site_state |>
  group_by(site_id, gateway_id) |>
  summarise(
    mean_site_quality_score = mean(site_quality_score, na.rm = TRUE),
    mean_aggregation_confidence = mean(aggregation_confidence, na.rm = TRUE),
    total_missing_children = sum(missing_child_count, na.rm = TRUE),
    total_stale_devices = sum(stale_device_count, na.rm = TRUE),
    total_protocol_errors = sum(protocol_error_count, na.rm = TRUE),
    total_lineage_gaps = sum(lineage_gap_count, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(site_summary, file.path(output_dir, "r_site_state_quality_summary.csv"))

plot <- ggplot(gateway_events, aes(x = gateway_id, y = buffer_backlog)) +
  geom_point(size = 3) +
  labs(
    title = "Gateway Buffer Backlog by Gateway",
    x = "Gateway",
    y = "Buffer backlog"
  )

ggsave(
  filename = file.path(output_dir, "r_gateway_buffer_backlog_by_gateway.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(gateway_summary)
