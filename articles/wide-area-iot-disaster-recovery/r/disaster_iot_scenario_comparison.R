# Wide-area IoT disaster recovery scenario comparison.
#
# This R workflow estimates:
# 1. Daily energy use.
# 2. Battery life.
# 3. Message delivery probability after retries.
# 4. Alert latency.
#
# Values are synthetic placeholders for planning and education.

library(readr)
library(dplyr)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "raw", "disaster_iot_scenarios_synthetic.csv")
out_path <- file.path(root, "outputs", "tables", "disaster_iot_scenario_summary_r.csv")
processed_path <- file.path(root, "data", "processed", "disaster_iot_scenarios_scored_r.csv")

delivery_probability <- function(p, k) {
  1 - (1 - p)^k
}

df <- read_csv(data_path, show_col_types = FALSE) %>%
  mutate(
    energy_per_message_wh =
      sensing_energy_wh +
      processing_energy_wh +
      transmit_energy_wh * retries +
      receive_energy_wh * retries,
    daily_energy_wh =
      messages_per_day * energy_per_message_wh + sleep_energy_wh_per_day,
    estimated_battery_life_days =
      battery_wh / daily_energy_wh,
    delivery_probability =
      delivery_probability(single_attempt_success, retries),
    alert_latency_s =
      sense_latency_s +
      queue_latency_s +
      tx_latency_s +
      backhaul_latency_s +
      process_latency_s +
      notify_latency_s,
    maintenance_priority =
      estimated_battery_life_days < 60 |
      terrain_difficulty == "high" |
      community_priority == "high"
  )

summary <- df %>%
  select(
    scenario_id,
    protocol,
    hazard_context,
    node_type,
    messages_per_day,
    retries,
    daily_energy_wh,
    estimated_battery_life_days,
    delivery_probability,
    alert_latency_s,
    terrain_difficulty,
    community_priority,
    maintenance_priority
  )

dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(processed_path), recursive = TRUE, showWarnings = FALSE)

write_csv(df, processed_path)
write_csv(summary, out_path)

print(summary)
