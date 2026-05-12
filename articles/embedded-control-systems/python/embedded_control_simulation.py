"""
Python Workflow: Embedded Control Simulation with Saturation, Delay, and Jitter

This script simulates a simple embedded control loop with PID feedback,
actuator saturation, anti-windup, safety filtering, measurement noise,
process disturbance, loop jitter, and deadline-slack reporting.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import random

import pandas as pd
import yaml


@dataclass
class PIDState:
    integral_error: float = 0.0
    previous_error: float = 0.0
    previous_command: float = 0.0


@dataclass(frozen=True)
class PIDConfig:
    kp: float
    ki: float
    kd: float
    dt: float
    command_min: float
    command_max: float
    anti_windup: bool


@dataclass(frozen=True)
class PlantConfig:
    time_constant_s: float
    gain_rpm_per_unit_command: float
    process_noise_std_rpm: float
    measurement_noise_std_rpm: float


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def safety_filter(
    candidate_command: float,
    previous_command: float,
    control_error: float,
    current_a: float,
    temperature_c: float,
    actuator: dict,
    envelope: dict,
) -> tuple[float, str]:
    """Apply command bounds, slew rate, thermal limits, and safety constraints."""
    command = candidate_command
    reason = "allowed"

    if temperature_c >= envelope["temperature_fault_c"]:
        return 0.0, "thermal_fault_safe_stop"

    if temperature_c >= envelope["temperature_warning_c"]:
        command = min(command, 0.75)
        reason = "thermal_derate"

    if abs(control_error) >= envelope["control_error_fault_rpm"]:
        command = min(command, 0.65)
        reason = "error_fault_derate"

    if current_a >= envelope["current_max_a"]:
        command = min(command, previous_command)
        reason = "current_limit_hold"

    command = max(min(command, actuator["command_max"]), actuator["command_min"])

    delta = command - previous_command
    max_delta = actuator["slew_rate_limit_per_cycle"]
    if delta > max_delta:
        command = previous_command + max_delta
        reason = "slew_rate_limited"
    elif delta < -max_delta:
        command = previous_command - max_delta
        reason = "slew_rate_limited"

    if not math.isclose(command, candidate_command, rel_tol=1e-12, abs_tol=1e-12) and reason == "allowed":
        reason = "command_clipped"

    return command, reason


def simulate(duration_s: float = 3.0, seed: int = 13) -> pd.DataFrame:
    rng = random.Random(seed)
    article_root = Path(__file__).resolve().parents[1]

    controller_cfg = load_yaml(article_root / "config" / "controller_config.yml")["controller"]
    plant_cfg = load_yaml(article_root / "config" / "plant_model.yml")["plant_model"]["dynamics"]
    plant_uncertainty = load_yaml(article_root / "config" / "plant_model.yml")["plant_model"]["uncertainty"]
    actuator_cfg = load_yaml(article_root / "config" / "actuator_profile.yml")["actuators"][0]
    envelope = load_yaml(article_root / "config" / "safety_envelope.yml")["safety_envelope"]
    timing = load_yaml(article_root / "config" / "timing_budget.yml")["timing_budget"]

    pid = PIDConfig(
        kp=float(controller_cfg["gains"]["kp"]),
        ki=float(controller_cfg["gains"]["ki"]),
        kd=float(controller_cfg["gains"]["kd"]),
        dt=float(controller_cfg["sampling_period_s"]),
        command_min=float(controller_cfg["command_limits"]["min"]),
        command_max=float(controller_cfg["command_limits"]["max"]),
        anti_windup=bool(controller_cfg["anti_windup"]),
    )

    plant = PlantConfig(
        time_constant_s=float(plant_cfg["time_constant_s"]),
        gain_rpm_per_unit_command=float(plant_cfg["gain_rpm_per_unit_command"]),
        process_noise_std_rpm=float(plant_uncertainty["process_noise_std_rpm"]),
        measurement_noise_std_rpm=float(plant_uncertainty["measurement_noise_std_rpm"]),
    )

    steps = int(duration_s / pid.dt)
    speed_rpm = 0.0
    estimated_speed_rpm = 0.0
    pid_state = PIDState()
    rows = []

    for k in range(steps):
        time_s = k * pid.dt
        setpoint = 1200.0 if time_s >= 0.25 else 1200.0 * (time_s / 0.25)

        measurement = speed_rpm + rng.gauss(0.0, plant.measurement_noise_std_rpm)
        estimated_speed_rpm = 0.25 * measurement + 0.75 * estimated_speed_rpm

        error = setpoint - estimated_speed_rpm
        integral_candidate = pid_state.integral_error + error * pid.dt
        derivative = (error - pid_state.previous_error) / pid.dt

        candidate = (
            pid.kp * error
            + pid.ki * integral_candidate
            + pid.kd * derivative
        )

        # Simulate current and temperature from command and load.
        current_a = 0.8 + 3.0 * max(0.0, min(candidate, 1.2)) + rng.gauss(0.0, 0.08)
        temperature_c = 40.0 + 28.0 * max(0.0, min(candidate, 1.0)) + 0.004 * k

        filtered, reason = safety_filter(
            candidate_command=candidate,
            previous_command=pid_state.previous_command,
            control_error=error,
            current_a=current_a,
            temperature_c=temperature_c,
            actuator=actuator_cfg,
            envelope=envelope,
        )

        saturated = not math.isclose(filtered, candidate, rel_tol=1e-12, abs_tol=1e-12)

        if not (pid.anti_windup and saturated):
            pid_state.integral_error = integral_candidate

        pid_state.previous_error = error
        pid_state.previous_command = filtered

        # First-order plant.
        target_speed = plant.gain_rpm_per_unit_command * filtered
        speed_dot = (target_speed - speed_rpm) / plant.time_constant_s
        disturbance = rng.gauss(0.0, plant.process_noise_std_rpm)
        speed_rpm = max(0.0, speed_rpm + pid.dt * speed_dot + disturbance * math.sqrt(pid.dt))

        loop_jitter_ms = rng.gauss(0.0, 0.12)
        stage_budget_sum_ms = (
            timing["stages"]["sensor_acquisition_ms"]
            + timing["stages"]["adc_or_encoder_processing_ms"]
            + timing["stages"]["filtering_or_estimation_ms"]
            + timing["stages"]["control_compute_ms"]
            + timing["stages"]["safety_filter_ms"]
            + timing["stages"]["bus_transmission_ms"]
            + timing["stages"]["actuator_update_ms"]
        )
        observed_loop_ms = stage_budget_sum_ms + abs(loop_jitter_ms)
        deadline_slack_ms = timing["deadline_ms"] - observed_loop_ms
        deadline_missed = deadline_slack_ms < 0

        if deadline_missed or abs(error) >= envelope["control_error_fault_rpm"]:
            safety_state = "degraded"
            supervisory_state = "degraded_control"
        elif abs(error) >= envelope["control_error_warning_rpm"] or saturated:
            safety_state = "warning"
            supervisory_state = "warning"
        else:
            safety_state = "normal"
            supervisory_state = "closed_loop_nominal"

        rows.append({
            "time_s": round(time_s, 4),
            "device_id": "ctrl-sim-001",
            "loop_id": "motor-speed",
            "operating_mode": "simulation",
            "setpoint": setpoint,
            "measurement": measurement,
            "estimate": estimated_speed_rpm,
            "control_error": error,
            "candidate_command": candidate,
            "filtered_command": filtered,
            "saturated": saturated,
            "deadline_missed": deadline_missed,
            "loop_jitter_ms": loop_jitter_ms,
            "deadline_slack_ms": deadline_slack_ms,
            "safety_state": safety_state,
            "supervisory_state": supervisory_state,
            "safety_filter_reason": reason,
            "current_a": current_a,
            "temperature_c": temperature_c,
            "true_speed_rpm": speed_rpm,
        })

    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([{
        "samples": len(df),
        "mean_abs_control_error": df["control_error"].abs().mean(),
        "max_abs_control_error": df["control_error"].abs().max(),
        "saturation_rate": df["saturated"].mean(),
        "safety_filter_rate": (df["safety_filter_reason"] != "allowed").mean(),
        "deadline_miss_rate": df["deadline_missed"].mean(),
        "mean_abs_jitter_ms": df["loop_jitter_ms"].abs().mean(),
        "min_deadline_slack_ms": df["deadline_slack_ms"].min(),
        "warning_or_degraded_rate": (df["safety_state"] != "normal").mean(),
    }]).round(4)


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = simulate()
    summary = summarize(df)

    df.to_csv(output_dir / "python_embedded_control_simulation.csv", index=False)
    summary.to_csv(output_dir / "python_embedded_control_summary.csv", index=False)

    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
