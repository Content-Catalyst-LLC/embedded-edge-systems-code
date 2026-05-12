# R Workflow: Hybrid Fleet Reliability and Synchronization Reporting

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

script_path <- tryCatch(normalizePath(sys.frame(1)$ofile), error = function(e) "")
article_root <- if (nzchar(script_path)) normalizePath(file.path(dirname(script_path), "..")) else getwd()
data_path <- file.path(article_root, "data", "sample_hybrid_events.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

hybrid_events <- read_csv(data_path, show_col_types = FALSE)

hybrid_summary <- hybrid_events |>
  group_by(site_id, gateway_id, operating_mode) |>
  summarise(
    events = n(),
    mean_state_age_s = mean(state_age_s, na.rm = TRUE),
    max_sync_lag_s = max(sync_lag_s, na.rm = TRUE),
    mean_buffer_backlog = mean(buffer_backlog, na.rm = TRUE),
    offline_event_rate = mean(cloud_reachable == FALSE, na.rm = TRUE),
    degraded_mode_rate = mean(degraded_mode, na.rm = TRUE),
    authority_violation_rate = mean(authority_valid == FALSE, na.rm = TRUE),
    policy_drift_rate = mean(edge_policy_version != cloud_policy_version, na.rm = TRUE),
    model_skew_rate = mean(edge_model_version != approved_model_version, na.rm = TRUE),
    rollout_gap_rate = mean(active_version != target_version, na.rm = TRUE),
    reconciliation_conflicts = sum(reconciliation_status %in% c("conflict", "hold_for_review", "rollback_required"), na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(degraded_mode_rate), desc(policy_drift_rate), desc(model_skew_rate))

write_csv(hybrid_summary, file.path(output_dir, "r_hybrid_fleet_reliability_sync_summary.csv"))

rollout_path <- file.path(article_root, "data", "rollout_nodes.csv")
rollout_nodes <- read_csv(rollout_path, show_col_types = FALSE)

rollout_summary <- rollout_nodes |>
  filter(eligible == TRUE) |>
  group_by(rollout_ring) |>
  summarise(
    eligible_nodes = n(),
    deployed_convergence_rate = mean(deployed_version == target_version, na.rm = TRUE),
    active_convergence_rate = mean(active_version == target_version, na.rm = TRUE),
    decision_used_convergence_rate = mean(decision_used_version == target_version, na.rm = TRUE),
    unreachable_nodes = sum(cloud_reachable == FALSE, na.rm = TRUE),
    unhealthy_nodes = sum(health_status != "healthy", na.rm = TRUE),
    .groups = "drop"
  )

write_csv(rollout_summary, file.path(output_dir, "r_rollout_convergence_by_ring.csv"))

plot <- ggplot(hybrid_events, aes(x = site_id, y = state_age_s)) +
  geom_point(size = 3) +
  labs(
    title = "Hybrid State Age by Site",
    x = "Site",
    y = "State age (seconds)"
  )

ggsave(
  filename = file.path(output_dir, "r_hybrid_state_age_by_site.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(hybrid_summary)
