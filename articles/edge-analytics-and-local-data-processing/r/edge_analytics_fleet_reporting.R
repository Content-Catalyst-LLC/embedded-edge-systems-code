# R Workflow: Edge Analytics Fleet Reporting and Local Data Quality Analysis

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

script_path <- tryCatch(normalizePath(sys.frame(1)$ofile), error = function(e) "")
article_root <- if (nzchar(script_path)) normalizePath(file.path(dirname(script_path), "..")) else getwd()
data_path <- file.path(article_root, "data", "sample_analytics_events.csv")
replay_path <- file.path(article_root, "data", "replay_records.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

analytics_events <- read_csv(data_path, show_col_types = FALSE)
replay_records <- read_csv(replay_path, show_col_types = FALSE)

edge_analytics_summary <- analytics_events |>
  group_by(site_id, gateway_id, signal_family, feature_version) |>
  summarise(
    events = n(),
    mean_local_latency_ms = mean(local_latency_ms, na.rm = TRUE),
    p95_local_latency_ms = quantile(local_latency_ms, 0.95, na.rm = TRUE),
    mean_freshness_s = mean(freshness_s, na.rm = TRUE),
    stale_output_rate = mean(freshness_s > freshness_threshold_s, na.rm = TRUE),
    feature_completeness_rate = mean(feature_complete == TRUE, na.rm = TRUE),
    event_rate = mean(event_detected == TRUE, na.rm = TRUE),
    immediate_uplink_rate = mean(uplink_mode == "immediate", na.rm = TRUE),
    deferred_uplink_rate = mean(uplink_mode == "deferred", na.rm = TRUE),
    mean_replay_lag_s = mean(replay_lag_s, na.rm = TRUE),
    lineage_completeness_rate = mean(lineage_complete == TRUE, na.rm = TRUE),
    mean_buffer_backlog = mean(buffer_backlog, na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(stale_output_rate), desc(mean_buffer_backlog), desc(mean_replay_lag_s))

write_csv(edge_analytics_summary, file.path(output_dir, "r_edge_analytics_fleet_reporting_summary.csv"))

replay_summary <- replay_records |>
  summarise(
    replay_records = n(),
    late_arrival_rate = mean(late_arrival == TRUE, na.rm = TRUE),
    duplicate_rate = mean(duplicate_detected == TRUE, na.rm = TRUE),
    gap_rate = mean(gap_detected == TRUE, na.rm = TRUE),
    correction_rate = mean(correction_record == TRUE, na.rm = TRUE)
  )

write_csv(replay_summary, file.path(output_dir, "r_replay_backfill_summary.csv"))

plot <- ggplot(analytics_events, aes(x = uplink_mode, y = freshness_s)) +
  geom_point(size = 3) +
  labs(
    title = "Edge Analytics Freshness by Uplink Mode",
    x = "Uplink mode",
    y = "Freshness (seconds)"
  )

ggsave(
  filename = file.path(output_dir, "r_edge_analytics_freshness_by_uplink_mode.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(edge_analytics_summary)
