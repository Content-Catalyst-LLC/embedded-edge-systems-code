"""Power Budget, Duty Cycle, and Lifetime Simulation.

This workflow estimates state-level energy, average current, lifetime,
communication sensitivity, wake-storm risk, and fleet battery risk for
low-power embedded devices.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

states = pd.read_csv(DATA / "power_states.csv")
telemetry = pd.read_csv(DATA / "device_power_telemetry.csv")
batteries = pd.read_csv(DATA / "battery_profiles.csv")
comm = pd.read_csv(DATA / "communication_energy.csv")

states["energy_mj"] = states["current_ma"] * states["voltage_v"] * states["duration_s"]
total_energy_mj = states["energy_mj"].sum()
total_duration_s = states["duration_s"].sum()
avg_current_ma = (states["current_ma"] * states["duration_s"]).sum() / total_duration_s
avg_power_mw = (states["current_ma"] * states["voltage_v"] * states["duration_s"]).sum() / total_duration_s

state_summary = states.copy()
state_summary["energy_share"] = state_summary["energy_mj"] / total_energy_mj
state_summary.to_csv(OUT / "state_level_energy_budget.csv", index=False)

usable_battery = batteries.copy()
usable_battery["usable_capacity_mah"] = usable_battery["capacity_mah"] * usable_battery["usable_derating_factor"]
usable_battery["estimated_lifetime_days"] = usable_battery["usable_capacity_mah"] / avg_current_ma / 24
usable_battery.to_csv(OUT / "battery_lifetime_estimates.csv", index=False)

telemetry["battery_risk"] = np.select(
    [
        telemetry["battery_v"] < 3.45,
        telemetry["retry_count_24h"] > 8,
        telemetry["false_wake_count_24h"] > 10,
        telemetry["sleep_residency_pct"] < 92,
        telemetry["brownout_count"] > 0,
    ],
    [
        "critical_low_voltage",
        "radio_retry_risk",
        "wake_storm_risk",
        "poor_sleep_residency",
        "brownout_observed",
    ],
    default="normal",
)
telemetry.to_csv(OUT / "fleet_power_risk_report.csv", index=False)

# Communication sensitivity scenario.
retry_counts = np.arange(0, 31, 1)
lora = comm.loc[comm["radio_type"] == "lora"].iloc[0]
comm_energy_mj = 8 * lora["tx_energy_mj"] + 8 * lora["rx_energy_mj"] + retry_counts * lora["retry_energy_mj"]
comm_sensitivity = pd.DataFrame({"retry_count": retry_counts, "daily_comm_energy_mj": comm_energy_mj})
comm_sensitivity.to_csv(OUT / "communication_retry_energy_sensitivity.csv", index=False)

plt.figure(figsize=(9, 5))
plt.bar(state_summary["state_name"], state_summary["energy_mj"])
plt.xticks(rotation=35, ha="right")
plt.ylabel("Energy per modeled period (mJ)")
plt.title("State-Level Energy Budget")
plt.tight_layout()
plt.savefig(OUT / "state_level_energy_budget.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.bar(telemetry["device_id"], telemetry["sleep_residency_pct"])
plt.axhline(92, linestyle="--")
plt.ylabel("Sleep residency (%)")
plt.xlabel("Device")
plt.title("Fleet Sleep Residency")
plt.tight_layout()
plt.savefig(OUT / "fleet_sleep_residency.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.plot(comm_sensitivity["retry_count"], comm_sensitivity["daily_comm_energy_mj"])
plt.xlabel("Daily retry count")
plt.ylabel("Daily communication energy (mJ)")
plt.title("Communication Retry Energy Sensitivity")
plt.tight_layout()
plt.savefig(OUT / "communication_retry_sensitivity.png", dpi=160)

print(f"Average current estimate: {avg_current_ma:.4f} mA")
print(f"Average power estimate: {avg_power_mw:.4f} mW")
print(f"Wrote low-power outputs to {OUT}")
