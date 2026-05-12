"""Sensor Acquisition Integrity and Sampling-Chain Simulation.

This workflow simulates a simple embedded acquisition chain: physical signal,
sensor noise, ADC quantization, timestamp jitter, stale readings, buffer age, and
quality flags. It writes engineering review outputs into ../outputs.
"""

from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

events = pd.read_csv(DATA / "acquisition_events.csv")
channels = pd.read_csv(DATA / "channel_manifest.csv")

events["acquisition_time"] = pd.to_datetime(events["acquisition_time"])
events["processing_time"] = pd.to_datetime(events["processing_time"])

events["processing_delay_ms"] = (
    events["processing_time"] - events["acquisition_time"]
).dt.total_seconds() * 1000

events = events.merge(channels, on="channel_id", how="left")
events["ideal_lsb"] = events["reference_mv"] / (2 ** events["adc_bits"])
events["nyquist_margin"] = (events["sample_rate_hz"] / 2) / events["signal_bandwidth_hz"].replace(0, np.nan)

def classify(row: pd.Series) -> str:
    flags = []
    if row["timestamp_jitter_ms"] > 20:
        flags.append("timestamp_fail")
    elif row["timestamp_jitter_ms"] > 5:
        flags.append("timestamp_warn")
    if row["buffer_age_ms"] > 250:
        flags.append("stale_buffer")
    if row["bus_retries"] > 2:
        flags.append("bus_retry_excess")
    if bool(row["adc_overrun"]):
        flags.append("adc_overrun")
    if bool(row["stale_read"]):
        flags.append("stale_read")
    if row["nyquist_margin"] < 1.25:
        flags.append("low_nyquist_margin")
    return "valid" if not flags else "|".join(flags)

events["computed_quality"] = events.apply(classify, axis=1)
events.to_csv(OUT / "measurement_quality_events.csv", index=False)

summary = (
    events.groupby(["site_id", "device_id", "interface_type"], dropna=False)
    .agg(
        measurements=("event_id", "count"),
        mean_processing_delay_ms=("processing_delay_ms", "mean"),
        max_timestamp_jitter_ms=("timestamp_jitter_ms", "max"),
        max_buffer_age_ms=("buffer_age_ms", "max"),
        retry_total=("bus_retries", "sum"),
        valid_share=("computed_quality", lambda s: (s == "valid").mean()),
    )
    .reset_index()
)
summary.to_csv(OUT / "acquisition_quality_summary.csv", index=False)

# Synthetic signal/quantization example for article figures.
sample_rate = 200
duration = 1.0
t = np.arange(0, duration, 1 / sample_rate)
physical_signal = 1.25 + 0.35 * np.sin(2 * math.pi * 12 * t) + 0.04 * np.random.default_rng(42).normal(size=len(t))
adc_bits = 12
v_ref = 3.3
codes = np.clip(np.round((physical_signal / v_ref) * (2**adc_bits - 1)), 0, 2**adc_bits - 1)
reconstructed = codes * v_ref / (2**adc_bits - 1)

pd.DataFrame({"time_s": t, "physical_signal_v": physical_signal, "adc_code": codes, "reconstructed_v": reconstructed}).to_csv(
    OUT / "simulated_adc_trace.csv", index=False
)

plt.figure(figsize=(10, 5))
plt.plot(t, physical_signal, label="physical signal")
plt.plot(t, reconstructed, label="quantized reconstruction", alpha=0.8)
plt.xlabel("Time (s)")
plt.ylabel("Voltage")
plt.title("ADC Quantization Simulation")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "adc_quantization_simulation.png", dpi=160)

print(f"Wrote outputs to {OUT}")
