"""
Python Workflow: Autonomous Edge Decision Simulation with Belief, Latency, and Safety Bounds

This script simulates a simple partially observable autonomous edge decision system.
It updates a categorical belief state, proposes candidate actions, applies runtime
assurance, and exports decision-event evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd
import yaml


STATES = ["clear_path", "obstacle_present", "hazard_likely"]


@dataclass(frozen=True)
class Belief:
    clear_path: float
    obstacle_present: float
    hazard_likely: float

    def normalize(self) -> "Belief":
        total = self.clear_path + self.obstacle_present + self.hazard_likely
        if total <= 0:
            return Belief(1 / 3, 1 / 3, 1 / 3)
        return Belief(
            clear_path=self.clear_path / total,
            obstacle_present=self.obstacle_present / total,
            hazard_likely=self.hazard_likely / total,
        )

    @property
    def most_likely_state(self) -> str:
        values = {
            "clear_path": self.clear_path,
            "obstacle_present": self.obstacle_present,
            "hazard_likely": self.hazard_likely,
        }
        return max(values, key=values.get)

    @property
    def confidence(self) -> float:
        return max(self.clear_path, self.obstacle_present, self.hazard_likely)


def observation_likelihood(observation: str) -> Dict[str, float]:
    """Return P(observation | state) for a simplified categorical sensor model."""
    table = {
        "clear": {"clear_path": 0.88, "obstacle_present": 0.10, "hazard_likely": 0.02},
        "obstacle": {"clear_path": 0.08, "obstacle_present": 0.80, "hazard_likely": 0.12},
        "hazard": {"clear_path": 0.03, "obstacle_present": 0.22, "hazard_likely": 0.75},
    }
    return table.get(observation, {"clear_path": 0.33, "obstacle_present": 0.33, "hazard_likely": 0.34})


def transition_prediction(previous: Belief, previous_action: str) -> Belief:
    """Simple transition model influenced by prior belief and action."""
    if previous_action in {"reroute", "slow_reroute"}:
        return Belief(
            clear_path=0.55 * previous.clear_path + 0.25,
            obstacle_present=0.45 * previous.obstacle_present,
            hazard_likely=0.45 * previous.hazard_likely,
        ).normalize()

    if previous_action == "safe_stop":
        return Belief(
            clear_path=previous.clear_path,
            obstacle_present=previous.obstacle_present,
            hazard_likely=previous.hazard_likely,
        ).normalize()

    return Belief(
        clear_path=0.92 * previous.clear_path + 0.04,
        obstacle_present=0.94 * previous.obstacle_present + 0.03,
        hazard_likely=0.96 * previous.hazard_likely + 0.02,
    ).normalize()


def update_belief(previous: Belief, observation: str, previous_action: str) -> Belief:
    prior = transition_prediction(previous, previous_action)
    likelihood = observation_likelihood(observation)

    updated = Belief(
        clear_path=prior.clear_path * likelihood["clear_path"],
        obstacle_present=prior.obstacle_present * likelihood["obstacle_present"],
        hazard_likely=prior.hazard_likely * likelihood["hazard_likely"],
    ).normalize()

    return updated


def select_candidate_action(belief_state: str) -> str:
    """Simple policy mapping belief state to candidate action."""
    policy = {
        "clear_path": "continue",
        "obstacle_present": "reroute",
        "hazard_likely": "proceed_slow",
    }
    return policy.get(belief_state, "pause_and_request_review")


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    observations = pd.read_csv(article_root / "data" / "sample_observations.csv")
    autonomy_profile = load_yaml(article_root / "config" / "autonomy_profile.yml")["autonomy_profile"]
    assurance = load_yaml(article_root / "config" / "runtime_assurance.yml")["runtime_assurance"]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Local import avoids circular path issues when running directly.
    from runtime_assurance_filter import filter_action

    belief = Belief(0.85, 0.10, 0.05)
    previous_action = "continue"
    events: List[dict] = []

    for idx, row in observations.iterrows():
        belief = update_belief(belief, row["observation"], previous_action)
        belief_state = belief.most_likely_state
        candidate_action = select_candidate_action(belief_state)

        result = filter_action(
            candidate_action=candidate_action,
            belief_state=belief_state,
            confidence=min(belief.confidence, float(row["observation_confidence"])),
            latency_ms=float(row["latency_ms"]),
            input_drift_score=float(row["input_drift_score"]),
            autonomy_level=autonomy_profile["default_autonomy_level"],
            safety_state="normal",
            assurance=assurance,
            allowed_actions=autonomy_profile["allowed_actions"],
        )

        filtered_action = result["filtered_action"]
        previous_action = filtered_action

        events.append({
            "time_s": row["time_s"],
            "device_id": "amr-sim-001",
            "mission_type": "warehouse_delivery",
            "autonomy_level": autonomy_profile["default_autonomy_level"],
            "observation": row["observation"],
            "clear_path_probability": round(belief.clear_path, 4),
            "obstacle_probability": round(belief.obstacle_present, 4),
            "hazard_probability": round(belief.hazard_likely, 4),
            "belief_state": belief_state,
            "decision_confidence": round(min(belief.confidence, float(row["observation_confidence"])), 4),
            "candidate_action": candidate_action,
            "filtered_action": filtered_action,
            "action_type": "nominal" if result["allowed"] else "fallback",
            "reason_code": result["reason_code"],
            "latency_ms": row["latency_ms"],
            "latency_budget_ms": assurance["thresholds"]["latency_budget_ms"],
            "input_drift_score": row["input_drift_score"],
            "safety_state": "normal" if result["allowed"] else "warning",
            "human_intervention_required": filtered_action == "pause_and_request_review",
        })

    output = pd.DataFrame(events)
    output.to_csv(output_dir / "python_autonomous_edge_decision_events.csv", index=False)

    summary = pd.DataFrame([{
        "decisions": len(output),
        "fallback_rate": float((output["action_type"] == "fallback").mean()),
        "human_intervention_rate": float(output["human_intervention_required"].mean()),
        "latency_violation_rate": float((output["latency_ms"] > output["latency_budget_ms"]).mean()),
        "mean_decision_confidence": float(output["decision_confidence"].mean()),
        "mean_input_drift_score": float(output["input_drift_score"].mean()),
    }]).round(4)

    summary.to_csv(output_dir / "python_autonomy_simulation_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
