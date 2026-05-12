"""
Python Workflow: State-Space Feedback Simulation with Saturation, Delay, and Jitter

This script simulates a simple second-order robotic joint model with PID feedback.
It includes actuator saturation, timing jitter, process disturbance, measurement noise,
and output reporting for engineering review.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import random

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PIDConfig:
    kp: float = 4.0
    ki: float = 0.7
    kd: float = 0.15
    dt: float = 0.01
    command_limit: float = 1.0
    anti_windup: bool = True


@dataclass(frozen=True)
class PlantConfig:
    damping: float = 0.35
    stiffness: float = 2.0
    input_gain: float = 1.4
    process_noise_std: float = 0.002
    measurement_noise_std: float = 0.01
    jitter_std_ms: float = 0.35


def reference_signal(t: float) -> float:
    """Smooth reference trajectory."""
    return 0.5 * math.sin(2 * math.pi * 0.35 * t)


def simulate_feedback_loop(
    duration_s: float = 8.0,
    pid: PIDConfig = PIDConfig(),
    plant: PlantConfig = PlantConfig(),
    seed: int = 7,
) -> pd.DataFrame:
    """Simulate state-space dynamics with PID feedback and saturation."""
    rng = random.Random(seed)
    np.random.seed(seed)

    steps = int(duration_s / pid.dt)
    state = np.array([0.0, 0.0], dtype=float)  # position, velocity

    # Continuous-inspired discrete model for a second-order joint.
    A = np.array([
        [1.0, pid.dt],
        [-plant.stiffness * pid.dt, 1.0 - plant.damping * pid.dt],
    ])
    B = np.array([0.0, plant.input_gain * pid.dt])

    rows = []
    integral_error = 0.0
    previous_error = 0.0

    for k in range(steps):
        nominal_t = k * pid.dt
        loop_jitter_ms = rng.gauss(0.0, plant.jitter_std_ms)
        effective_dt = max(0.001, pid.dt + loop_jitter_ms / 1000.0)

        measured_position = state[0] + rng.gauss(0.0, plant.measurement_noise_std)
        reference_position = reference_signal(nominal_t)
        error = reference_position - measured_position

        integral_candidate = integral_error + error * effective_dt
        derivative_error = (error - previous_error) / effective_dt

        raw_command = (
            pid.kp * error
            + pid.ki * integral_candidate
            + pid.kd * derivative_error
        )

        command = max(min(raw_command, pid.command_limit), -pid.command_limit)
        saturated = not math.isclose(command, raw_command, rel_tol=1e-12, abs_tol=1e-12)

        if not (pid.anti_windup and saturated):
            integral_error = integral_candidate

        disturbance = np.array([
            0.0,
            rng.gauss(0.0, plant.process_noise_std),
        ])

        state = A @ state + B * command + disturbance
        previous_error = error

        safety_state = "normal"
        fault_state = "normal"

        if abs(error) >= 0.15:
            safety_state = "degraded"
            fault_state = "tracking_error"
        elif abs(error) >= 0.08 or saturated:
            safety_state = "warning"

        rows.append({
            "time_s": round(nominal_t, 4),
            "reference_position": reference_position,
            "measured_position": measured_position,
            "true_position": state[0],
            "true_velocity": state[1],
            "tracking_error": error,
            "raw_command": raw_command,
            "command": command,
            "saturated": saturated,
            "loop_jitter_ms": loop_jitter_ms,
            "safety_state": safety_state,
            "fault_state": fault_state,
        })

    return pd.DataFrame(rows)


def summarize_simulation(df: pd.DataFrame) -> pd.DataFrame:
    """Create an engineering summary of the simulated run."""
    return pd.DataFrame([{
        "samples": len(df),
        "mean_abs_tracking_error": df["tracking_error"].abs().mean(),
        "max_abs_tracking_error": df["tracking_error"].abs().max(),
        "saturation_rate": df["saturated"].mean(),
        "mean_abs_jitter_ms": df["loop_jitter_ms"].abs().mean(),
        "max_abs_jitter_ms": df["loop_jitter_ms"].abs().max(),
        "warning_or_degraded_rate": (df["safety_state"] != "normal").mean(),
    }]).round(4)


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = simulate_feedback_loop()
    summary = summarize_simulation(df)

    df.to_csv(output_dir / "python_state_space_feedback_simulation.csv", index=False)
    summary.to_csv(output_dir / "python_state_space_feedback_summary.csv", index=False)

    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
