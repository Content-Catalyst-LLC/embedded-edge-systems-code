#!/usr/bin/env python3
"""
Wide-area IoT disaster recovery planning model.

This script estimates:
- daily energy use
- battery life
- message delivery probability
- alert latency
- review priority for synthetic LPWAN disaster scenarios

Use this as a planning scaffold, not a final engineering model.
"""

from pathlib import Path
import pandas as pd
from math import pow

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "disaster_iot_scenarios_synthetic.csv"
OUT = ROOT / "outputs" / "tables" / "disaster_iot_scenario_summary.csv"
PROCESSED = ROOT / "data" / "processed" / "disaster_iot_scenarios_scored.csv"

def delivery_probability(p: float, k: int) -> float:
    if not 0 <= p <= 1:
        raise ValueError("single_attempt_success must be between 0 and 1.")
    if k < 1:
        raise ValueError("retries must be at least 1.")
    return 1 - pow(1 - p, k)

def main() -> None:
    df = pd.read_csv(DATA)

    df["energy_per_message_wh"] = (
        df["sensing_energy_wh"]
        + df["processing_energy_wh"]
        + df["transmit_energy_wh"] * df["retries"]
        + df["receive_energy_wh"] * df["retries"]
    )

    df["daily_energy_wh"] = (
        df["messages_per_day"] * df["energy_per_message_wh"]
        + df["sleep_energy_wh_per_day"]
    )

    df["estimated_battery_life_days"] = df["battery_wh"] / df["daily_energy_wh"]

    df["delivery_probability"] = df.apply(
        lambda row: delivery_probability(row["single_attempt_success"], int(row["retries"])),
        axis=1
    )

    df["alert_latency_s"] = (
        df["sense_latency_s"]
        + df["queue_latency_s"]
        + df["tx_latency_s"]
        + df["backhaul_latency_s"]
        + df["process_latency_s"]
        + df["notify_latency_s"]
    )

    df["maintenance_priority"] = (
        (df["estimated_battery_life_days"] < 60)
        | (df["terrain_difficulty"] == "high")
        | (df["community_priority"] == "high")
    )

    summary_columns = [
        "scenario_id",
        "protocol",
        "hazard_context",
        "node_type",
        "messages_per_day",
        "retries",
        "daily_energy_wh",
        "estimated_battery_life_days",
        "delivery_probability",
        "alert_latency_s",
        "terrain_difficulty",
        "community_priority",
        "maintenance_priority",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED, index=False)
    df[summary_columns].to_csv(OUT, index=False)

    print("Disaster IoT scenario summary written to:")
    print(OUT)
    print()
    print(df[summary_columns].to_string(index=False))

if __name__ == "__main__":
    main()
