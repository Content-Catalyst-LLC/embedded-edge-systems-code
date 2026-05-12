"""
Python Workflow: Edge AI Model Budgeting, Quantization, and Deployment Simulation

This script evaluates whether edge AI inference events fit device budgets for
model size, tensor arena, latency, energy, confidence, model version, and backend
output deviation.
"""

from __future__ import annotations

from pathlib import Path
import random
import pandas as pd
import yaml


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def run() -> None:
    article_root = Path(__file__).resolve().parents[1]
    output_dir = article_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(42)
    capabilities = pd.read_csv(article_root / "data" / "device_capabilities.csv")
    decision_policy = load_yaml(article_root / "config" / "decision_policy.yml")["decision_policy"]
    model_budget = load_yaml(article_root / "config" / "model_budget.yml")["model_budget"]

    rows = []
    device_counter = 1

    for _, device in capabilities.iterrows():
        for minute in range(60):
            device_class = device["device_class"]
            approved_model_version = model_budget["approved_model_version"]
            model_version = approved_model_version if rng.random() > 0.08 else "model-1.1"

            model_size_kb = rng.uniform(0.55, 1.10) * float(model_budget["max_model_size_kb"][device_class])
            tensor_arena_kb = rng.uniform(0.55, 1.20) * float(model_budget["max_tensor_arena_kb"][device_class])
            latency_ms = rng.uniform(0.45, 1.30) * float(model_budget["p95_latency_budget_ms"][device_class])
            energy_mj = rng.uniform(0.35, 1.15) * float(model_budget["energy_budget_mj"][device_class])
            confidence = rng.uniform(0.55, 0.98)
            sensor_health = "healthy" if rng.random() > 0.08 else "degraded"
            backend_delta = abs(rng.gauss(0.012, 0.009))
            drift_proxy = abs(rng.gauss(0.07, 0.06))

            memory_ok = (
                model_size_kb <= float(device["flash_budget_kb"])
                and tensor_arena_kb <= float(device["ram_budget_kb"])
            )
            latency_ok = latency_ms <= float(device["p95_latency_budget_ms"])
            energy_ok = energy_mj <= float(device["energy_budget_mj"])
            backend_ok = backend_delta <= float(decision_policy["backend_delta_tolerance"])
            confidence_ok = confidence >= float(decision_policy["confidence_threshold"])
            version_ok = model_version == approved_model_version

            deployment_feasible = memory_ok and latency_ok and energy_ok and backend_ok
            local_action_allowed = (
                confidence_ok and sensor_health == "healthy" and version_ok and deployment_feasible
            )

            predicted_class = rng.choice(["normal", "warning", "fault"])
            if local_action_allowed:
                local_action = decision_policy["actions"][predicted_class]["action"]
                fallback_used = False
            else:
                fallback_used = True
                if not confidence_ok:
                    local_action = "fallback_more_samples"
                elif sensor_health != "healthy":
                    local_action = "suppress_local_action_and_uplink"
                elif not version_ok:
                    local_action = "restrict_action_and_flag_version_skew"
                elif not backend_ok:
                    local_action = "restrict_action_and_request_backend_review"
                else:
                    local_action = "fallback_uplink_for_review"

            rows.append({
                "timestamp": f"2026-03-28T12:{minute:02d}:00Z",
                "device_id": f"dev-ai-{device_counter:03d}",
                "site_id": rng.choice(["site-a", "site-b", "site-c"]),
                "device_class": device_class,
                "runtime_backend": device["accelerator"] if device["accelerator"] != "none" else device["supported_runtime"],
                "model_version": model_version,
                "approved_model_version": approved_model_version,
                "feature_version": "features-1.0",
                "latency_ms": round(latency_ms, 4),
                "p95_budget_ms": device["p95_latency_budget_ms"],
                "model_size_kb": round(model_size_kb, 4),
                "flash_budget_kb": device["flash_budget_kb"],
                "tensor_arena_kb": round(tensor_arena_kb, 4),
                "ram_budget_kb": device["ram_budget_kb"],
                "energy_mj": round(energy_mj, 4),
                "energy_budget_mj": device["energy_budget_mj"],
                "confidence": round(confidence, 4),
                "confidence_threshold": decision_policy["confidence_threshold"],
                "predicted_class": predicted_class,
                "sensor_health": sensor_health,
                "fallback_used": fallback_used,
                "drift_proxy": round(drift_proxy, 4),
                "backend_output_delta": round(backend_delta, 5),
                "backend_delta_tolerance": decision_policy["backend_delta_tolerance"],
                "memory_ok": memory_ok,
                "latency_ok": latency_ok,
                "decision_policy_version": decision_policy["version"],
                "local_action": local_action,
            })

        device_counter += 1

    events = pd.DataFrame(rows)
    events.to_csv(output_dir / "python_edge_ai_inference_events.csv", index=False)

    summary = pd.DataFrame([{
        "events": len(events),
        "device_classes": events["device_class"].nunique(),
        "fallback_rate": events["fallback_used"].mean(),
        "low_confidence_rate": (events["confidence"] < events["confidence_threshold"]).mean(),
        "model_skew_rate": (events["model_version"] != events["approved_model_version"]).mean(),
        "memory_violation_rate": (~events["memory_ok"]).mean(),
        "latency_violation_rate": (~events["latency_ok"]).mean(),
        "backend_delta_violation_rate": (events["backend_output_delta"] > events["backend_delta_tolerance"]).mean(),
        "mean_drift_proxy": events["drift_proxy"].mean(),
        "p95_latency_ms": events["latency_ms"].quantile(0.95),
    }]).round(4)

    summary.to_csv(output_dir / "python_edge_ai_budget_quantization_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()
