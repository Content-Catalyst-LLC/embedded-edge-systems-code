# R Workflow: Edge Privacy Reporting and Retention Governance

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

script_path <- tryCatch(normalizePath(sys.frame(1)$ofile), error = function(e) "")
article_root <- if (nzchar(script_path)) normalizePath(file.path(dirname(script_path), "..")) else getwd()
data_path <- file.path(article_root, "data", "sample_edge_privacy_events.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

events <- read_csv(data_path, show_col_types = FALSE)

events_scored <- events |>
  mutate(
    normalized_retention = pmin(retention_hours / 168, 1),
    exposure =
      0.18 * raw_collection +
      0.22 * identifiability +
      0.12 * normalized_retention +
      0.18 * linkability +
      0.18 * sharing_scope,
    controls =
      0.16 * minimisation +
      0.18 * local_transformation +
      0.14 * ephemeral_processing,
    privacy_risk_score = pmax(0, pmin(1, exposure - controls)),
    privacy_risk_band = case_when(
      privacy_risk_score >= 0.70 ~ "high",
      privacy_risk_score >= 0.50 ~ "moderate",
      privacy_risk_score >= 0.30 ~ "managed",
      TRUE ~ "low"
    )
  )

privacy_summary <- events_scored |>
  group_by(site, signal_type, privacy_risk_band) |>
  summarise(
    events = n(),
    mean_privacy_risk = mean(privacy_risk_score, na.rm = TRUE),
    mean_retention_hours = mean(retention_hours, na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(mean_privacy_risk))

write_csv(events_scored, file.path(output_dir, "r_edge_privacy_risk_scores.csv"))
write_csv(privacy_summary, file.path(output_dir, "r_edge_privacy_summary.csv"))

plot <- ggplot(events_scored, aes(x = signal_type, y = privacy_risk_score)) +
  geom_point(size = 3) +
  coord_flip() +
  labs(
    title = "Residual Privacy Risk by Edge Signal Type",
    x = "Signal type",
    y = "Privacy risk score"
  )

ggsave(
  filename = file.path(output_dir, "r_privacy_risk_by_signal_type.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(privacy_summary)
