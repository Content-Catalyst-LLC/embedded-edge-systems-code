# R Workflow: Fleet Security Posture and Lifecycle Reporting

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

script_path <- tryCatch(normalizePath(sys.frame(1)$ofile), error = function(e) "")
article_root <- if (nzchar(script_path)) normalizePath(file.path(dirname(script_path), "..")) else getwd()
data_path <- file.path(article_root, "data", "sample_security_assets.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

assets <- read_csv(data_path, show_col_types = FALSE)

fleet_scored <- assets |>
  mutate(
    security_readiness_score =
      0.16 * hardware_trust +
      0.16 * boot_integrity +
      0.15 * identity_strength +
      0.14 * update_readiness +
      0.14 * runtime_isolation +
      0.13 * monitoring_maturity -
      0.16 * exposure -
      0.14 * lifecycle_drift,
    security_readiness_score = pmax(0, pmin(1, security_readiness_score)),
    risk_band = case_when(
      support_state == "end-of-support" ~ "critical",
      secure_boot == FALSE ~ "critical",
      security_readiness_score < 0.45 ~ "critical",
      security_readiness_score < 0.60 ~ "high",
      security_readiness_score < 0.75 ~ "moderate",
      TRUE ~ "managed"
    )
  )

security_summary <- fleet_scored |>
  group_by(site, device_class, support_state) |>
  summarise(
    devices = n(),
    mean_security_readiness = mean(security_readiness_score, na.rm = TRUE),
    high_or_critical = sum(risk_band %in% c("high", "critical"), na.rm = TRUE),
    exposed_devices = sum(exposure >= 0.70, na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(high_or_critical), mean_security_readiness)

write_csv(fleet_scored, file.path(output_dir, "r_security_readiness_scores.csv"))
write_csv(security_summary, file.path(output_dir, "r_security_posture_summary.csv"))

plot <- ggplot(fleet_scored, aes(x = device_class, y = security_readiness_score)) +
  geom_point(size = 3) +
  coord_flip() +
  labs(
    title = "Embedded and Edge Security Readiness by Device Class",
    x = "Device class",
    y = "Security readiness score"
  )

ggsave(
  filename = file.path(output_dir, "r_security_readiness_by_device_class.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(security_summary)
