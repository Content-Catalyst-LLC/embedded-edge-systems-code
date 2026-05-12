# R Workflow: Standards Adoption and Governance Reporting for Edge Estates

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- normalizePath("..", mustWork = FALSE)
}

data_path <- file.path(article_root, "data", "sample_edge_assets.csv")
output_dir <- file.path(article_root, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

edge_assets <- read_csv(data_path, show_col_types = FALSE)

weights <- list(
  protocol_conformance = 0.20,
  semantic_alignment = 0.20,
  lifecycle_control = 0.20,
  security_baseline = 0.20,
  operational_accountability = 0.15,
  unmanaged_divergence = 0.15
)

edge_assets <- edge_assets |>
  mutate(
    governance_score =
      weights$protocol_conformance * protocol_conformance +
      weights$semantic_alignment * semantic_alignment +
      weights$lifecycle_control * lifecycle_control +
      weights$security_baseline * security_baseline +
      weights$operational_accountability * operational_accountability -
      weights$unmanaged_divergence * unmanaged_divergence,
    governance_score = pmax(0, pmin(1, governance_score)),
    risk_band = case_when(
      support_state == "end-of-support" ~ "critical",
      governance_score < 0.55 ~ "critical",
      governance_score < 0.70 ~ "high",
      governance_score < 0.82 ~ "moderate",
      TRUE ~ "low"
    )
  )

site_summary <- edge_assets |>
  group_by(site, standard_profile, support_state) |>
  summarise(
    devices = n(),
    mean_governance_score = mean(governance_score, na.rm = TRUE),
    high_or_critical = sum(risk_band %in% c("high", "critical"), na.rm = TRUE),
    .groups = "drop"
  ) |>
  arrange(desc(high_or_critical), mean_governance_score)

write_csv(edge_assets, file.path(output_dir, "r_edge_governance_scores.csv"))
write_csv(site_summary, file.path(output_dir, "r_site_governance_summary.csv"))

plot <- ggplot(edge_assets, aes(x = standard_profile, y = governance_score)) +
  geom_point(size = 3) +
  coord_flip() +
  labs(
    title = "Edge Governance Score by Standards Profile",
    x = "Standards profile",
    y = "Governance score"
  )

ggsave(
  filename = file.path(output_dir, "r_governance_score_by_profile.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(site_summary)
