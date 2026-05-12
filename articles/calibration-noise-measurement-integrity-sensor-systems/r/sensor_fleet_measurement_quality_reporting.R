suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})

article_root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
output_dir <- file.path(article_root, "outputs")
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

records_path <- file.path(output_dir, "python_measurement_integrity_analysis.csv")
if (!file.exists(records_path)) {
  stop("Run python/sensor_calibration_noise_integrity_analysis.py first.")
}

measurement_records <- read_csv(records_path, show_col_types = FALSE)

sensor_quality_summary <- measurement_records |>
  group_by(site_id, sensor_family, calibration_version, firmware_version) |>
  summarise(
    sensors = n_distinct(sensor_id),
    measurements = n(),
    mean_uncertainty = mean(expanded_uncertainty, na.rm = TRUE),
    p95_uncertainty = quantile(expanded_uncertainty, 0.95, na.rm = TRUE),
    mean_snr_db = mean(snr_db, na.rm = TRUE),
    low_snr_rate = mean(grepl("low_snr", quality_flags), na.rm = TRUE),
    calibration_expired_rate = mean(grepl("calibration_expired", quality_flags), na.rm = TRUE),
    coefficient_mismatch_rate = mean(grepl("coefficient_mismatch", quality_flags), na.rm = TRUE),
    drift_warning_rate = mean(grepl("drift_warning", quality_flags), na.rm = TRUE),
    out_of_range_rate = mean(grepl("out_of_range", quality_flags), na.rm = TRUE),
    lineage_completeness_rate = mean(lineage_complete == TRUE, na.rm = TRUE),
    traceability_completeness_rate = mean(traceability_complete == TRUE, na.rm = TRUE),
    mean_measurement_confidence = mean(measurement_confidence, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(sensor_quality_summary, file.path(output_dir, "r_sensor_fleet_measurement_quality_summary.csv"))

plot <- ggplot(measurement_records, aes(x = sensor_family, y = expanded_uncertainty)) +
  geom_point(size = 3) +
  labs(
    title = "Expanded Uncertainty by Sensor Family",
    x = "Sensor family",
    y = "Expanded uncertainty"
  )

ggsave(
  filename = file.path(output_dir, "r_expanded_uncertainty_by_sensor_family.png"),
  plot = plot,
  width = 9,
  height = 5,
  dpi = 150
)

print(sensor_quality_summary)
