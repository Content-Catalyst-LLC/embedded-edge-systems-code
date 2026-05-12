# Platform Portfolio and Device-Class Comparison

library(readr)
library(dplyr)
library(ggplot2)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_dir <- file.path(root, "data")
out_dir <- file.path(root, "outputs")
dir.create(out_dir, showWarnings = FALSE)

platforms <- read_csv(file.path(data_dir, "candidate_platforms.csv"), show_col_types = FALSE)
requirements <- read_csv(file.path(data_dir, "device_requirements.csv"), show_col_types = FALSE)
security <- read_csv(file.path(data_dir, "security_lifecycle.csv"), show_col_types = FALSE)

portfolio <- platforms %>%
  left_join(security, by = "platform_id") %>%
  mutate(
    platform_risk = case_when(
      lifecycle_support_score < 7 ~ "lifecycle_risk",
      secure_boot == FALSE ~ "secure_boot_gap",
      debug_lock == FALSE ~ "debug_policy_gap",
      sleep_ua > 500 & platform_type != "soc" ~ "sleep_current_risk",
      TRUE ~ "normal"
    ),
    memory_total_kb = flash_kb + sram_kb,
    io_score = adc_channels + timers + dma_channels + uart + spi + i2c + can
  ) %>%
  arrange(platform_type, desc(lifecycle_support_score), desc(memory_total_kb))

write_csv(portfolio, file.path(out_dir, "r_platform_portfolio_summary.csv"))

type_summary <- portfolio %>%
  group_by(platform_type) %>%
  summarise(
    platforms = n(),
    mean_cpu_mhz = mean(cpu_mhz, na.rm = TRUE),
    mean_flash_kb = mean(flash_kb, na.rm = TRUE),
    mean_sram_kb = mean(sram_kb, na.rm = TRUE),
    mean_active_ma = mean(active_ma, na.rm = TRUE),
    mean_sleep_ua = mean(sleep_ua, na.rm = TRUE),
    mean_lifecycle_support_score = mean(lifecycle_support_score, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(type_summary, file.path(out_dir, "r_platform_type_summary.csv"))

device_class_needs <- requirements %>%
  mutate(
    requirement_intensity = required_cpu_mhz / max(required_cpu_mhz) +
      required_sram_kb / max(required_sram_kb) +
      required_bandwidth_mb_s / max(required_bandwidth_mb_s)
  ) %>%
  arrange(desc(requirement_intensity))

write_csv(device_class_needs, file.path(out_dir, "r_device_class_requirements_summary.csv"))

p1 <- ggplot(portfolio, aes(x = reorder(platform_name, cpu_mhz), y = cpu_mhz)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Candidate Platform CPU Capacity",
    x = "Platform",
    y = "CPU MHz"
  )

ggsave(file.path(out_dir, "r_candidate_platform_cpu.png"), p1, width = 8, height = 5, dpi = 160)

p2 <- ggplot(portfolio, aes(x = reorder(platform_name, lifecycle_support_score), y = lifecycle_support_score)) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Lifecycle Support Score by Platform",
    x = "Platform",
    y = "Lifecycle support score"
  )

ggsave(file.path(out_dir, "r_lifecycle_support_score.png"), p2, width = 8, height = 5, dpi = 160)

print(portfolio)
print(type_summary)
print(device_class_needs)
