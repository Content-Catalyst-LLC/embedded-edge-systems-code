"""
Sensor Feature Engineering
--------------------------

Transforms a window of sensor readings into features suitable for TinyML or
edge anomaly detection.
"""

from __future__ import annotations

import numpy as np


def extract_signal_features(values: np.ndarray) -> dict:
    """Extract simple features from a sensor signal window."""

    centered = values - np.mean(values)

    zero_crossings = np.where(np.diff(np.signbit(centered)))[0]

    return {
        "mean_value": float(np.mean(values)),
        "standard_deviation": float(np.std(values)),
        "minimum_value": float(np.min(values)),
        "maximum_value": float(np.max(values)),
        "signal_energy": float(np.sum(values ** 2)),
        "zero_crossing_rate": float(len(zero_crossings) / max(len(values), 1)),
    }


def main() -> None:
    rng = np.random.default_rng(seed=42)
    values = rng.normal(loc=0.0, scale=1.0, size=128)
    features = extract_signal_features(values)

    print(features)


if __name__ == "__main__":
    main()
