"""Silicon-Fit, Power, Memory, and Peripheral-Constraint Modeling.

This workflow compares candidate microcontroller and SoC platforms against
device-class requirements across compute, memory, bandwidth, power, I/O,
security, lifecycle, and accelerator needs.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

platforms = pd.read_csv(DATA / "candidate_platforms.csv")
requirements = pd.read_csv(DATA / "device_requirements.csv")
security = pd.read_csv(DATA / "security_lifecycle.csv")
power_domains = pd.read_csv(DATA / "power_domains.csv")

def yes(value):
    return str(value).strip().lower() in {"true", "yes", "1"}

rows = []
for _, req in requirements.iterrows():
    for _, platform in platforms.iterrows():
        security_row = security[security["platform_id"] == platform["platform_id"]].iloc[0]

        compute_margin = platform["cpu_mhz"] - req["required_cpu_mhz"]
        flash_margin = platform["flash_kb"] - req["required_flash_kb"]
        sram_margin = platform["sram_kb"] - req["required_sram_kb"]
        bandwidth_margin = platform["bus_bandwidth_mb_s"] - req["required_bandwidth_mb_s"]
        active_margin = req["max_active_ma"] - platform["active_ma"]
        sleep_margin = req["max_sleep_ua"] - platform["sleep_ua"]
        wake_margin = req["max_wake_latency_ms"] - platform["wake_latency_ms"]

        peripheral_fit = (
            platform["adc_channels"] >= req["min_adc_channels"]
            and platform["timers"] >= req["min_timers"]
            and platform["dma_channels"] >= req["min_dma_channels"]
            and (not yes(req["needs_can"]) or platform["can"] >= 1)
            and (not yes(req["needs_ethernet"]) or yes(platform["ethernet"]))
            and (not yes(req["needs_wireless"]) or str(platform["wireless"]).lower() != "none")
        )

        security_fit = (
            (not yes(req["needs_secure_boot"]) or yes(security_row["secure_boot"]))
            and (not yes(req["needs_key_storage"]) or yes(security_row["key_storage"]))
            and yes(security_row["debug_lock"])
        )

        accelerator_fit = (
            (not yes(req["needs_accelerator"]))
            or str(platform["accelerator"]).lower() not in {"none", "nan", ""}
        )

        lifecycle_fit = platform["lifecycle_support_score"] >= req["required_lifecycle_score"]

        margins_ok = (
            compute_margin >= 0
            and flash_margin >= 0
            and sram_margin >= 0
            and bandwidth_margin >= 0
            and active_margin >= 0
            and sleep_margin >= 0
            and wake_margin >= 0
        )

        fit_score = sum([
            compute_margin >= 0,
            flash_margin >= 0,
            sram_margin >= 0,
            bandwidth_margin >= 0,
            active_margin >= 0,
            sleep_margin >= 0,
            wake_margin >= 0,
            peripheral_fit,
            security_fit,
            accelerator_fit,
            lifecycle_fit
        ]) / 11

        rows.append({
            "device_class": req["device_class"],
            "platform_id": platform["platform_id"],
            "platform_name": platform["platform_name"],
            "platform_type": platform["platform_type"],
            "compute_margin_mhz": compute_margin,
            "flash_margin_kb": flash_margin,
            "sram_margin_kb": sram_margin,
            "bandwidth_margin_mb_s": bandwidth_margin,
            "active_current_margin_ma": active_margin,
            "sleep_current_margin_ua": sleep_margin,
            "wake_latency_margin_ms": wake_margin,
            "peripheral_fit": peripheral_fit,
            "security_fit": security_fit,
            "accelerator_fit": accelerator_fit,
            "lifecycle_fit": lifecycle_fit,
            "margins_ok": margins_ok,
            "fit_score": fit_score,
            "recommended": fit_score >= 0.82 and margins_ok and peripheral_fit and security_fit and lifecycle_fit
        })

fit = pd.DataFrame(rows)
fit.to_csv(OUT / "silicon_fit_scorecard.csv", index=False)

best = (
    fit.sort_values(["device_class", "recommended", "fit_score"], ascending=[True, False, False])
    .groupby("device_class")
    .head(3)
)
best.to_csv(OUT / "top_platform_candidates_by_device_class.csv", index=False)

power_domains["daily_energy_proxy"] = (
    power_domains["active_ma"] * 2.0
    + (power_domains["sleep_ua"] / 1000.0) * 22.0
    + power_domains["wake_latency_ms"] * 0.001
)
domain_summary = (
    power_domains.groupby("platform_id")
    .agg(
        domains=("domain_name", "count"),
        active_ma_total=("active_ma", "sum"),
        sleep_ua_total=("sleep_ua", "sum"),
        max_wake_latency_ms=("wake_latency_ms", "max"),
        daily_energy_proxy=("daily_energy_proxy", "sum")
    )
    .reset_index()
)
domain_summary.to_csv(OUT / "power_domain_summary.csv", index=False)

plt.figure(figsize=(10, 5))
plot_data = best.copy()
labels = plot_data["device_class"] + "\n" + plot_data["platform_name"]
plt.bar(labels, plot_data["fit_score"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Fit score")
plt.title("Top Platform Fit Scores by Device Class")
plt.tight_layout()
plt.savefig(OUT / "top_platform_fit_scores.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.bar(platforms["platform_name"], platforms["sram_kb"])
plt.xticks(rotation=35, ha="right")
plt.ylabel("SRAM (KB)")
plt.title("Candidate Platform SRAM")
plt.tight_layout()
plt.savefig(OUT / "candidate_platform_sram.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.bar(domain_summary["platform_id"], domain_summary["sleep_ua_total"])
plt.xlabel("Platform")
plt.ylabel("Total sleep current proxy (uA)")
plt.title("Power-Domain Sleep Current Proxy")
plt.tight_layout()
plt.savefig(OUT / "power_domain_sleep_current.png", dpi=160)

print(f"Wrote silicon-fit outputs to {OUT}")
