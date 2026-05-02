"""
Edge Telemetry Quality Pipeline
-------------------------------

Creates synthetic edge telemetry, validates quality indicators, and exports
CSV plus SQLite outputs.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "tables"
DATABASE_PATH = PROJECT_ROOT / "outputs" / "embedded_edge_systems.sqlite"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)


def create_synthetic_telemetry() -> pd.DataFrame:
    """Create synthetic telemetry records from edge devices."""

    return pd.DataFrame(
        [
            {"device_id": "EDGE-001", "sensor_type": "temperature", "observed_value": 21.4, "battery_voltage": 3.91, "signal_quality": 0.98, "observed_at": "2026-04-01T10:00:00"},
            {"device_id": "EDGE-001", "sensor_type": "temperature", "observed_value": 21.7, "battery_voltage": 3.90, "signal_quality": 0.97, "observed_at": "2026-04-01T10:05:00"},
            {"device_id": "EDGE-002", "sensor_type": "vibration", "observed_value": 0.81, "battery_voltage": 3.70, "signal_quality": 0.91, "observed_at": "2026-04-01T10:00:00"},
            {"device_id": "EDGE-002", "sensor_type": "vibration", "observed_value": 1.42, "battery_voltage": 3.68, "signal_quality": 0.84, "observed_at": "2026-04-01T10:05:00"},
            {"device_id": "EDGE-003", "sensor_type": "moisture", "observed_value": None, "battery_voltage": 3.50, "signal_quality": 0.76, "observed_at": "2026-04-01T10:00:00"},
        ]
    )


def calculate_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate basic telemetry quality indicators."""

    transmission_ready = (
        df["observed_value"].notna()
        & (df["battery_voltage"] >= 3.3)
        & (df["signal_quality"] >= 0.80)
    )

    report = {
        "record_count": len(df),
        "missing_observed_values": int(df["observed_value"].isna().sum()),
        "mean_battery_voltage": float(df["battery_voltage"].mean()),
        "mean_signal_quality": float(df["signal_quality"].mean()),
        "transmission_ready_records": int(transmission_ready.sum()),
    }

    return pd.DataFrame([report])


def main() -> None:
    telemetry = create_synthetic_telemetry()
    telemetry["observed_at"] = pd.to_datetime(telemetry["observed_at"])

    quality_report = calculate_quality_report(telemetry)

    telemetry_path = DATA_DIR / "edge_telemetry.csv"
    report_path = OUTPUT_DIR / "edge_telemetry_quality_report.csv"

    telemetry.to_csv(telemetry_path, index=False)
    quality_report.to_csv(report_path, index=False)

    with sqlite3.connect(DATABASE_PATH) as connection:
        telemetry.to_sql("edge_telemetry", connection, if_exists="replace", index=False)
        quality_report.to_sql("edge_telemetry_quality_report", connection, if_exists="replace", index=False)

    print("Edge Telemetry Quality Pipeline complete.")
    print(quality_report)


if __name__ == "__main__":
    main()
