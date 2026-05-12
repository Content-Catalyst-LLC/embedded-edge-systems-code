"""Environmental Network Coverage, Sampling, and Quality Simulation.

This workflow models environmental sensor nodes as distributed measurement
infrastructure. It evaluates data completeness, link health, battery risk,
calibration age, stale records, and event-mode sampling evidence.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

sites = pd.read_csv(DATA / "sites.csv")
nodes = pd.read_csv(DATA / "nodes.csv")
measurements = pd.read_csv(DATA / "environmental_measurements.csv")
calibrations = pd.read_csv(DATA / "calibration_records.csv")

measurements["acquisition_time"] = pd.to_datetime(measurements["acquisition_time"])
measurements["processing_time"] = pd.to_datetime(measurements["processing_time"])
measurements["processing_delay_s"] = (
    measurements["processing_time"] - measurements["acquisition_time"]
).dt.total_seconds()

node_status = (
    measurements.groupby(["site_id", "node_id"], dropna=False)
    .agg(
        measurement_count=("event_id", "count"),
        valid_or_event_count=("quality_flag", lambda s: s.isin(["valid", "event_valid"]).sum()),
        warning_count=("quality_flag", lambda s: (~s.isin(["valid", "event_valid"])).sum()),
        max_processing_delay_s=("processing_delay_s", "max"),
        max_buffer_age_s=("buffer_age_s", "max"),
        mean_link_quality=("link_quality", "mean"),
        packet_retries=("packet_retries", "sum"),
        min_battery_v=("battery_v", "min"),
    )
    .reset_index()
)

node_status["valid_completeness"] = node_status["valid_or_event_count"] / node_status["measurement_count"]
node_status["battery_risk"] = np.where(node_status["min_battery_v"] < 11.8, "warning", "normal")
node_status["link_risk"] = np.where(node_status["mean_link_quality"] < 0.60, "warning", "normal")
node_status["buffer_risk"] = np.where(node_status["max_buffer_age_s"] > 240, "warning", "normal")

node_status = node_status.merge(sites[["site_id", "site_name", "site_type", "representativeness"]], on="site_id", how="left")
node_status.to_csv(OUT / "network_node_quality_summary.csv", index=False)

calibrations["valid_until"] = pd.to_datetime(calibrations["valid_until"])
reference_date = pd.Timestamp("2026-03-28")
calibrations["days_until_expiry"] = (calibrations["valid_until"] - reference_date).dt.days
calibrations["calibration_risk"] = np.where(calibrations["days_until_expiry"] < 0, "expired", np.where(calibrations["days_until_expiry"] < 30, "expires_soon", "current"))
calibrations.to_csv(OUT / "calibration_risk_summary.csv", index=False)

# Synthetic event-capture simulation.
rng = np.random.default_rng(42)
t = pd.date_range("2026-03-28 00:00:00", periods=96, freq="15min")
baseline = 5 + rng.normal(0, 0.7, len(t))
event = np.where((t.hour >= 12) & (t.hour <= 15), 30 * np.exp(-0.5 * ((t.hour + t.minute / 60 - 13.5) / 0.9) ** 2), 0)
signal = baseline + event
event_df = pd.DataFrame({"timestamp": t, "simulated_turbidity_ntu": signal})
event_df["event_mode"] = event_df["simulated_turbidity_ntu"] > 18
event_df.to_csv(OUT / "simulated_event_capture.csv", index=False)

plt.figure(figsize=(10, 5))
plt.plot(event_df["timestamp"], event_df["simulated_turbidity_ntu"])
plt.xlabel("Time")
plt.ylabel("Turbidity (NTU)")
plt.title("Simulated Environmental Event Capture")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(OUT / "simulated_event_capture.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.bar(node_status["node_id"], node_status["valid_completeness"])
plt.ylim(0, 1.05)
plt.xlabel("Node")
plt.ylabel("Valid completeness")
plt.title("Valid Data Completeness by Node")
plt.tight_layout()
plt.savefig(OUT / "valid_completeness_by_node.png", dpi=160)

print(f"Wrote environmental network outputs to {OUT}")
