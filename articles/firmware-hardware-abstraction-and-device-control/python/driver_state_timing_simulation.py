"""Driver State, Timing, and Fault-Path Simulation.

This workflow models firmware device control through driver contracts,
lifecycle events, control-path latency, fault detection, suspend/resume
behavior, and update compatibility evidence.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

contracts = pd.read_csv(DATA / "driver_contracts.csv")
events = pd.read_csv(DATA / "device_lifecycle_events.csv")
telemetry = pd.read_csv(DATA / "firmware_fleet_telemetry.csv")
updates = pd.read_csv(DATA / "update_manifest.csv")

events["event_time"] = pd.to_datetime(events["event_time"])
events["fault_detected"] = events["result"].ne("success") | events["error_code"].ne("none")

required_states = {
    "init", "active", "suspended", "resume", "fault", "recovery", "update", "rollback"
}

state_coverage = (
    events.groupby("driver_id")["lifecycle_state"]
    .agg(lambda s: len(set(s) & required_states) / len(required_states))
    .reset_index(name="state_coverage")
)

latency_summary = (
    events.groupby(["driver_id", "event_type"], dropna=False)
    .agg(
        events=("event_id", "count"),
        mean_latency_ms=("latency_ms", "mean"),
        max_latency_ms=("latency_ms", "max"),
        faults_detected=("fault_detected", "sum"),
    )
    .reset_index()
)

driver_summary = (
    events.groupby("driver_id")
    .agg(
        lifecycle_events=("event_id", "count"),
        fault_events=("fault_detected", "sum"),
        mean_latency_ms=("latency_ms", "mean"),
        max_latency_ms=("latency_ms", "max"),
    )
    .reset_index()
    .merge(contracts, on="driver_id", how="left")
    .merge(state_coverage, on="driver_id", how="left")
)

driver_summary["fault_rate"] = driver_summary["fault_events"] / driver_summary["lifecycle_events"]
driver_summary.to_csv(OUT / "driver_lifecycle_quality_summary.csv", index=False)
latency_summary.to_csv(OUT / "driver_latency_summary.csv", index=False)

telemetry["firmware_risk"] = np.select(
    [
        telemetry["rollback_count"] > 0,
        telemetry["suspend_resume_failures"] > 2,
        telemetry["driver_errors"] > 3,
        telemetry["bus_timeouts"] > 5,
        telemetry["watchdog_resets"] > 1,
    ],
    [
        "rollback_observed",
        "suspend_resume_risk",
        "driver_error_risk",
        "bus_timeout_risk",
        "watchdog_reset_risk",
    ],
    default="normal",
)
telemetry.to_csv(OUT / "firmware_fleet_risk_report.csv", index=False)

updates["update_risk"] = np.where(
    (updates["rollback_supported"] == True) & (updates["interrupted_update_tested"] == True),
    "release_ready",
    "needs_update_integrity_review",
)
updates.to_csv(OUT / "update_compatibility_review.csv", index=False)

plt.figure(figsize=(8, 5))
plt.bar(driver_summary["driver_id"], driver_summary["state_coverage"].fillna(0))
plt.ylim(0, 1.05)
plt.xlabel("Driver")
plt.ylabel("Lifecycle state coverage")
plt.title("Driver Lifecycle State Coverage")
plt.tight_layout()
plt.savefig(OUT / "driver_state_coverage.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.bar(driver_summary["driver_id"], driver_summary["max_latency_ms"])
plt.xlabel("Driver")
plt.ylabel("Max latency (ms)")
plt.title("Max Driver Control-Path Latency")
plt.tight_layout()
plt.savefig(OUT / "driver_latency_budget.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.bar(telemetry["device_id"], telemetry["driver_errors"])
plt.xlabel("Device")
plt.ylabel("Driver errors")
plt.title("Driver Errors by Device")
plt.tight_layout()
plt.savefig(OUT / "driver_errors_by_device.png", dpi=160)

print(f"Wrote firmware/device-control outputs to {OUT}")
