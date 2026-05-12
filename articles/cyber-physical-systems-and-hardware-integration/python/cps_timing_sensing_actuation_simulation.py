"""
Python Workflow: CPS Timing, Sensing, and Actuation Simulation

This script simulates a simplified cyber-physical system:
physical process -> sensor observation -> state estimate -> candidate command ->
runtime assurance -> actuator realization -> timing/uncertainty telemetry.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
import math

import pandas as pd
import yaml


@dataclass
class PhysicalState:
    speed_rpm: float


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def sensor_model(state: PhysicalState, rng: random.Random, sensor_noise_rpm: float, calibration_error_rpm: float) -> float:
    return state.speed_rpm + rng.gauss(0.0, sensor_noise_rpm) + calibration_error_rpm


def estimate_state(previous_estimate: float, measurement: float, alpha: float = 0.25) -> float:
    return alpha * measurement + (1.0 - alpha) * previous_estimate


def controller(estimate: float, reference: float) -> float:
    error = reference - estimate
    return 0.0025 * error


def runtime_assurance(
    candidate_command: float,
    previous_command: float,
    sensor_age_ms: float,
    deadline_slack_ms: float,
    temperature_c: float,
    current_a: float,
    total_uncertainty: float,
    uncertainty_budget: float,
    actuator: dict,
) -> tuple[float, str]:
    if sensor_age_ms > 3.0:
        return 0.0, "stale_sensor_safe_stop"

    if deadline_slack_ms < 0.0:
        return 0.0, "deadline_miss_safe_stop"

    if total_uncertainty > uncertainty_budget:
        return min(previous_command, 0.50), "uncertainty_budget_violation"

    if temperature_c >= actuator["thermal_limit_c"]:
        return 0.0, "thermal_fault_safe_stop"

    if temperature_c >= actuator["thermal_warning_c"]:
        return min(max(candidate_command, 0.0), 0.75), "thermal_derate"

    if current_a >= actuator["max_current_a"]:
        return min(previous_command, 0.50), "current_limit_clip"

    command = min(max(candidate_command, actuator["command_min"]), actuator["command_max"])
    delta = command - previous_command
    max_delta = actuator["slew_rate_limit_per_cycle"]

    if delta > max_delta:
        return previous_command + max_delta, "slew_rate_limited"

    if delta < -max_delta:
        return previous_command - max_delta, "slew_rate_limited"

    if not math.isclose(command, candidate_command, rel_tol=1e-12, abs_tol=1e-12):
        return command, "command_clipped"

    return command, "allowed"


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    sensor_manifest = pd.json_normalize(
        pd.read_json(article_root / "config" / "sensor_manifest.json").to_dict()["sensor_manifest"]["sensors"]
    )
    actuator = load_yaml(article_root / "config" / "actuator_profile.yml")["actuators"][0]
    timing = load_yaml(article_root / "config" / "timing_budget.yml")["timing_budget"]
    uncertainty_budget = load_yaml(article_root / "config" / "uncertainty_budget.yml")["uncertainty_budget"]

    rng = random.Random(42)
    state = PhysicalState(speed_rpm=0.0)
    estimate = 0.0
    previous_command = 0.0
    rows = []

    deadline_ms = timing["deadline_ms"]
    stage_base_ms = (
        timing["stages"]["sense_ms"]
        + timing["stages"]["convert_ms"]
        + timing["stages"]["estimate_ms"]
        + timing["stages"]["compute_ms"]
        + timing["stages"]["safety_filter_ms"]
        + timing["stages"]["communicate_ms"]
        + timing["stages"]["actuate_ms"]
    )

    for k in range(1500):
        time_s = k * 0.001
        reference = 1200.0 if time_s >= 0.25 else 1200.0 * time_s / 0.25

        sensor_noise = float(sensor_manifest.loc[sensor_manifest["signal"] == "motor_speed_rpm", "uncertainty_rpm"].iloc[0])
        calibration_error = rng.gauss(0.0, float(uncertainty_budget["components"]["calibration_error_rpm"]) / 3.0)
        measurement = sensor_model(state, rng, sensor_noise, calibration_error)
        estimate = estimate_state(estimate, measurement)

        candidate_command = controller(estimate, reference)

        loop_jitter_ms = abs(rng.gauss(0.0, 0.14))
        observed_loop_ms = stage_base_ms + loop_jitter_ms
        deadline_slack_ms = deadline_ms - observed_loop_ms

        sensor_age_ms = 1.0 + abs(rng.gauss(0.0, 0.35))
        if k in {420, 421, 422}:
            sensor_age_ms = 4.5

        sensor_error = sensor_noise
        calibration_error_abs = abs(calibration_error)
        quantization_error = float(uncertainty_budget["components"]["quantization_error_rpm"])
        estimation_error = abs(measurement - estimate) * 0.25
        model_error = float(uncertainty_budget["components"]["model_error_rpm"])
        total_uncertainty = sensor_error + calibration_error_abs + quantization_error + estimation_error + model_error

        temperature_c = 42.0 + 25.0 * max(previous_command, 0.0) + 0.002 * k
        current_a = 0.8 + 3.0 * max(previous_command, 0.0) + rng.gauss(0.0, 0.08)

        filtered_command, reason = runtime_assurance(
            candidate_command=candidate_command,
            previous_command=previous_command,
            sensor_age_ms=sensor_age_ms,
            deadline_slack_ms=deadline_slack_ms,
            temperature_c=temperature_c,
            current_a=current_a,
            total_uncertainty=total_uncertainty,
            uncertainty_budget=float(uncertainty_budget["total_budget_rpm"]),
            actuator=actuator,
        )

        target_speed = 1600.0 * filtered_command
        state.speed_rpm = max(0.0, state.speed_rpm + 0.001 * ((target_speed - state.speed_rpm) / 0.18) + rng.gauss(0.0, 0.35))

        safety_state = "normal"
        if reason != "allowed" or deadline_slack_ms < 0.2 or total_uncertainty > 0.8 * float(uncertainty_budget["total_budget_rpm"]):
            safety_state = "warning"
        if deadline_slack_ms < 0.0 or reason.endswith("safe_stop"):
            safety_state = "degraded"

        rows.append({
            "time_s": round(time_s, 4),
            "device_id": "cps-sim-001",
            "subsystem": "motor-control",
            "operating_mode": "simulation",
            "sensor_age_ms": sensor_age_ms,
            "measurement": measurement,
            "estimate": estimate,
            "candidate_command": candidate_command,
            "filtered_command": filtered_command,
            "actuator_saturated": filtered_command != candidate_command,
            "deadline_missed": deadline_slack_ms < 0.0,
            "loop_jitter_ms": loop_jitter_ms,
            "deadline_slack_ms": deadline_slack_ms,
            "interface_error": sensor_age_ms > 3.0,
            "safety_state": safety_state,
            "safety_filter_reason": reason,
            "current_a": current_a,
            "temperature_c": temperature_c,
            "true_speed_rpm": state.speed_rpm,
            "total_uncertainty": total_uncertainty,
            "uncertainty_budget": float(uncertainty_budget["total_budget_rpm"]),
            "recovery_event": reason.endswith("safe_stop"),
        })

        previous_command = filtered_command

    events = pd.DataFrame(rows)
    events.to_csv(output_dir / "python_cps_timing_sensing_actuation_events.csv", index=False)

    summary = pd.DataFrame([{
        "events": len(events),
        "mean_sensor_age_ms": events["sensor_age_ms"].mean(),
        "deadline_miss_rate": events["deadline_missed"].mean(),
        "actuator_saturation_rate": events["actuator_saturated"].mean(),
        "safety_filter_rate": (events["safety_filter_reason"] != "allowed").mean(),
        "interface_error_rate": events["interface_error"].mean(),
        "uncertainty_violation_rate": (events["total_uncertainty"] > events["uncertainty_budget"]).mean(),
        "safety_event_rate": (events["safety_state"] != "normal").mean(),
    }]).round(4)

    summary.to_csv(output_dir / "python_cps_simulation_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
