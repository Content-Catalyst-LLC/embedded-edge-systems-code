"""Scheduling, Deadline, and Jitter Simulation.

This workflow estimates RTOS task utilization, response-time risk, slack
margin, queue pressure, deadline misses, stack risk, ISR load, and fleet timing risk.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

tasks = pd.read_csv(DATA / "task_manifest.csv")
runtime = pd.read_csv(DATA / "runtime_trace.csv")
queues = pd.read_csv(DATA / "queue_trace.csv")
fleet = pd.read_csv(DATA / "rtos_fleet_telemetry.csv")

tasks["utilization"] = tasks["wcet_ms"] / tasks["period_ms"]
tasks["basic_response_time_ms"] = tasks["wcet_ms"] + tasks["blocking_ms"]
tasks["slack_margin_ms"] = tasks["deadline_ms"] - tasks["basic_response_time_ms"]
tasks["timing_risk"] = np.select(
    [
        tasks["slack_margin_ms"] < 0,
        tasks["slack_margin_ms"] < 5,
        tasks["utilization"] > 0.7,
    ],
    [
        "deadline_not_schedulable_basic",
        "low_slack_margin",
        "high_utilization",
    ],
    default="normal",
)
tasks.to_csv(OUT / "task_timing_summary.csv", index=False)

total_utilization = tasks["utilization"].sum()
utilization_summary = pd.DataFrame(
    [{"total_utilization": total_utilization, "utilization_warning": total_utilization > 0.7}]
)
utilization_summary.to_csv(OUT / "utilization_summary.csv", index=False)

runtime["runtime_ms"] = runtime["finish_ms"] - runtime["start_ms"]
runtime["completion_slack_ms"] = runtime["deadline_ms"] - runtime["finish_ms"]
runtime.to_csv(OUT / "runtime_trace_with_slack.csv", index=False)

deadline_report = (
    runtime.groupby(["device_id", "firmware_version", "task_name"], dropna=False)
    .agg(
        activations=("trace_id", "count"),
        deadline_misses=("deadline_miss", "sum"),
        mean_runtime_ms=("runtime_ms", "mean"),
        max_runtime_ms=("runtime_ms", "max"),
        min_completion_slack_ms=("completion_slack_ms", "min"),
        max_isr_time_us=("isr_time_us", "max"),
    )
    .reset_index()
)
deadline_report.to_csv(OUT / "deadline_and_runtime_report.csv", index=False)

queues["pressure_ratio"] = queues["high_water_mark"] / queues["capacity"]
queues["queue_risk"] = np.select(
    [
        queues["overflow_count"] > 0,
        queues["pressure_ratio"] >= 0.9,
        queues["pressure_ratio"] >= 0.75,
    ],
    [
        "overflow_observed",
        "near_capacity",
        "elevated_pressure",
    ],
    default="normal",
)
queues.to_csv(OUT / "queue_pressure_report.csv", index=False)

fleet["rtos_risk"] = np.select(
    [
        fleet["watchdog_resets"] > 0,
        fleet["deadline_misses_24h"] > 0,
        fleet["queue_overflows_24h"] > 0,
        fleet["min_stack_watermark_bytes"] < 512,
        fleet["max_isr_time_us"] > 250,
        fleet["idle_residency_pct"] < 70,
    ],
    [
        "watchdog_reset_risk",
        "deadline_miss_risk",
        "queue_overflow_risk",
        "stack_watermark_risk",
        "isr_latency_risk",
        "low_idle_residency",
    ],
    default="normal",
)
fleet.to_csv(OUT / "rtos_fleet_timing_risk_report.csv", index=False)

# Simple fixed-priority interference approximation by priority order.
priority_order = tasks.sort_values("priority").copy()
response_estimates = []
for _, task in priority_order.iterrows():
    hp = tasks[tasks["priority"] < task["priority"]]
    interference = hp["wcet_ms"].sum()
    response = task["wcet_ms"] + task["blocking_ms"] + interference
    response_estimates.append(
        {
            "task_name": task["task_name"],
            "priority": task["priority"],
            "deadline_ms": task["deadline_ms"],
            "response_estimate_ms": response,
            "slack_after_interference_ms": task["deadline_ms"] - response,
            "schedulable_basic_estimate": response <= task["deadline_ms"],
        }
    )
response_df = pd.DataFrame(response_estimates)
response_df.to_csv(OUT / "fixed_priority_response_estimates.csv", index=False)

plt.figure(figsize=(8, 5))
plt.bar(tasks["task_name"], tasks["slack_margin_ms"])
plt.axhline(0, linestyle="--")
plt.xticks(rotation=35, ha="right")
plt.ylabel("Slack margin (ms)")
plt.title("Task Slack Margin")
plt.tight_layout()
plt.savefig(OUT / "task_slack_margin.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.bar(queues["queue_name"], queues["pressure_ratio"])
plt.axhline(0.9, linestyle="--")
plt.xticks(rotation=35, ha="right")
plt.ylabel("High-water mark / capacity")
plt.title("Queue Pressure")
plt.tight_layout()
plt.savefig(OUT / "queue_pressure.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.bar(fleet["device_id"], fleet["deadline_misses_24h"])
plt.xlabel("Device")
plt.ylabel("Deadline misses / 24h")
plt.title("Deadline Misses by Device")
plt.tight_layout()
plt.savefig(OUT / "deadline_misses_by_device.png", dpi=160)

plt.figure(figsize=(8, 5))
plt.bar(fleet["device_id"], fleet["idle_residency_pct"])
plt.axhline(70, linestyle="--")
plt.xlabel("Device")
plt.ylabel("Idle residency (%)")
plt.title("RTOS Idle Residency by Device")
plt.tight_layout()
plt.savefig(OUT / "idle_residency_by_device.png", dpi=160)

print(f"Total task utilization estimate: {total_utilization:.3f}")
print(f"Wrote RTOS timing outputs to {OUT}")
