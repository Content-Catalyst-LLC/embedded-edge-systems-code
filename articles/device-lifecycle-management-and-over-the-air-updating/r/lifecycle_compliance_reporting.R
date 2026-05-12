# R Workflow: Lifecycle Compliance and Update Status Reporting Across Device Fleets

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[[1]]) else file.path(getwd(), "lifecycle_compliance_reporting.R")
article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)

data_path <- file.path(article_root, "data", "sample_device_fleet.csv")
events_path <- file.path(article_root, "data", "sample_deployment_events.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

device_fleet <- read_csv(data_path, show_col_types = FALSE)
deployment_events <- read_csv(events_path, show_col_types = FALSE)

fleet_scored <- device_fleet |>
  mutate(
    ota_readiness_score =
      0.16 * identity_assurance +
      0.18 * compatibility_match +
      0.16 * package_integrity +
      0.16 * validation_status +
      0.16 * rollback_readiness +
      0.13 * observability -
      0.15 * lifecycle_drift,
    ota_readiness_score = pmax(0, pmin(1, ota_readiness_score)),
    rollout_decision = case_when(
      support_state == "end-of-support" ~ "block",
      rollback_readiness < 0.50 ~ "hold-for-recovery-review",
      ota_readiness_score >= 0.82 ~ "approve",
      ota_readiness_score >= 0.70 ~ "canary-only",
      TRUE ~ "hold"
    )
  )

lifecycle_summary <- fleet_scored |>
  group_by(site, support_state, rollout_ring) |>
  summarise(
    devices = n(),
    mean_ota_readiness = mean(ota_readiness_score, na.rm = TRUE),
    blocked_or_held = sum(rollout_decision %in% c("block", "hold", "hold-for-recovery-review"), na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(blocked_or_held), mean_ota_readiness)

deployment_summary <- deployment_events |>
  count(device_id, phase, status, error_code, name = "events") |>
  arrange(device_id, phase, status)

write_csv(fleet_scored, file.path(output_dir, "r_ota_readiness_scores.csv"))
write_csv(lifecycle_summary, file.path(output_dir, "r_lifecycle_summary.csv"))
write_csv(deployment_summary, file.path(output_dir, "r_deployment_event_summary.csv"))

plot <- ggplot(fleet_scored, aes(x = rollout_ring, y = ota_readiness_score)) +
  geom_point(size = 3) +
  labs(
    title = "OTA Readiness by Rollout Ring",
    x = "Rollout ring",
    y = "OTA readiness score"
  )

ggsave(
  filename = file.path(output_dir, "r_ota_readiness_by_rollout_ring.png"),
  plot = plot,
  width = 8,
  height = 5,
  dpi = 150
)

print(lifecycle_summary)
