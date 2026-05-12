"""Fault Injection, Recovery Coverage, and Availability Simulation.

This workflow models fault events, detection coverage, recovery coverage,
degraded-mode behavior, safe-state transitions, and effective availability for
embedded device fleets.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

faults = pd.read_csv(DATA / "fault_events.csv")
fleet = pd.read_csv(DATA / "device_fleet.csv")
resets = pd.read_csv(DATA / "reset_log.csv")

faults["event_time"] = pd.to_datetime(faults["event_time"])
faults["detected"] = faults["detected"].astype(str).str.lower().eq("true")
faults["recovery_success"] = faults["recovery_success"].astype(str).str.lower().eq("true")
faults["safe_state_entered"] = faults["safe_state_entered"].astype(str).str.lower().eq("true")

coverage = (
    faults.groupby("fault_class")
    .agg(
        events=("event_id", "count"),
        detected=("detected", "sum"),
        recovered=("recovery_success", "sum"),
        mean_recovery_time_ms=("recovery_time_ms", "mean"),
        total_service_loss_s=("service_loss_s", "sum"),
        safe_state_entries=("safe_state_entered", "sum"),
    )
    .reset_index()
)

coverage["detection_coverage"] = coverage["detected"] / coverage["events"]
coverage["recovery_coverage"] = coverage["recovered"] / coverage["events"]
coverage["effective_coverage"] = coverage["detection_coverage"] * coverage["recovery_coverage"]
coverage.to_csv(OUT / "fault_coverage_by_class.csv", index=False)

fleet_summary = (
    faults.groupby("device_id")
    .agg(
        fault_events=("event_id", "count"),
        detected_events=("detected", "sum"),
        successful_recoveries=("recovery_success", "sum"),
        degraded_entries=("degraded_mode", lambda s: s.astype(str).str.lower().eq("true").sum()),
        safe_state_entries=("safe_state_entered", "sum"),
        service_loss_s=("service_loss_s", "sum"),
    )
    .reset_index()
    .merge(fleet, on="device_id", how="left")
)

fleet_summary["availability_estimate"] = 1 - (fleet_summary["service_loss_s"] / (24 * 3600))
fleet_summary["availability_estimate"] = fleet_summary["availability_estimate"].clip(lower=0, upper=1)
fleet_summary.to_csv(OUT / "fleet_reliability_summary.csv", index=False)

reset_summary = (
    resets.groupby(["device_id", "reset_cause", "firmware_version"])
    .agg(
        resets=("reset_id", "count"),
        mean_uptime_before_reset_s=("uptime_before_reset_s", "mean"),
        max_watchdog_count=("watchdog_count", "max"),
        persistent_state_failures=("persistent_state_valid", lambda s: (~s.astype(str).str.lower().eq("true")).sum()),
    )
    .reset_index()
)
reset_summary.to_csv(OUT / "reset_pattern_summary.csv", index=False)

plt.figure(figsize=(8, 5))
plt.bar(coverage["fault_class"], coverage["effective_coverage"])
plt.ylim(0, 1.05)
plt.xlabel("Fault class")
plt.ylabel("Effective coverage")
plt.title("Effective Fault Coverage by Class")
plt.tight_layout()
plt.savefig(OUT / "effective_fault_coverage_by_class.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.bar(fleet_summary["device_id"], fleet_summary["service_loss_s"])
plt.xlabel("Device")
plt.ylabel("Service loss (s)")
plt.title("Service Loss by Device")
plt.tight_layout()
plt.savefig(OUT / "service_loss_by_device.png", dpi=160)

print(f"Wrote reliability outputs to {OUT}")
