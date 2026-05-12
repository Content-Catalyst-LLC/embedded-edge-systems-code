"""
Python Workflow: Kalman-Style State Estimation and Residual Monitoring

This script applies a simple linear Kalman filter to the simulated robotic joint.
It reports estimator residuals as an observability and sensor-health signal.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from state_space_feedback_simulation import simulate_feedback_loop


def run_kalman_filter(measurements: pd.Series, dt: float = 0.01) -> pd.DataFrame:
    """Run a simple constant-velocity Kalman filter over measured position."""
    A = np.array([[1.0, dt], [0.0, 1.0]])
    C = np.array([[1.0, 0.0]])

    Q = np.array([[0.0001, 0.0], [0.0, 0.001]])
    R = np.array([[0.01]])

    x_hat = np.array([[0.0], [0.0]])
    P = np.eye(2)

    rows = []

    for k, y in enumerate(measurements):
        # Predict
        x_pred = A @ x_hat
        P_pred = A @ P @ A.T + Q

        # Innovation
        y_vec = np.array([[float(y)]])
        innovation = y_vec - C @ x_pred
        S = C @ P_pred @ C.T + R
        K = P_pred @ C.T @ np.linalg.inv(S)

        # Update
        x_hat = x_pred + K @ innovation
        P = (np.eye(2) - K @ C) @ P_pred

        residual = float(innovation[0, 0])
        residual_abs = abs(residual)

        if residual_abs >= 0.15:
            band = "fault"
        elif residual_abs >= 0.08:
            band = "warning"
        else:
            band = "normal"

        rows.append({
            "step": k,
            "observed_position": float(y),
            "estimated_position": float(x_hat[0, 0]),
            "estimated_velocity": float(x_hat[1, 0]),
            "residual": residual,
            "residual_abs": residual_abs,
            "residual_band": band,
            "position_variance": float(P[0, 0]),
            "velocity_variance": float(P[1, 1]),
        })

    return pd.DataFrame(rows)


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    sim = simulate_feedback_loop()
    estimates = run_kalman_filter(sim["measured_position"])

    estimates.to_csv(output_dir / "python_kalman_state_estimates.csv", index=False)

    summary = pd.DataFrame([{
        "samples": len(estimates),
        "mean_abs_residual": estimates["residual_abs"].mean(),
        "max_abs_residual": estimates["residual_abs"].max(),
        "warning_or_fault_rate": (estimates["residual_band"] != "normal").mean(),
        "final_position_variance": estimates["position_variance"].iloc[-1],
        "final_velocity_variance": estimates["velocity_variance"].iloc[-1],
    }]).round(5)

    summary.to_csv(output_dir / "python_kalman_estimation_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
