from pathlib import Path
import pandas as pd
import yaml

LAYER_SCORES = {
    "device": {"latency": 1.00, "bandwidth": 0.70, "privacy": 0.90, "continuity": 0.95, "trust": 0.75, "assurance": 0.75, "management": 0.70},
    "gateway": {"latency": 0.85, "bandwidth": 0.90, "privacy": 0.80, "continuity": 0.90, "trust": 0.80, "assurance": 0.80, "management": 0.55},
    "local-edge": {"latency": 0.75, "bandwidth": 0.85, "privacy": 0.75, "continuity": 0.85, "trust": 0.85, "assurance": 0.85, "management": 0.50},
    "regional-edge": {"latency": 0.55, "bandwidth": 0.60, "privacy": 0.55, "continuity": 0.50, "trust": 0.88, "assurance": 0.80, "management": 0.45},
    "cloud": {"latency": 0.25, "bandwidth": 0.35, "privacy": 0.45, "continuity": 0.20, "trust": 0.95, "assurance": 0.90, "management": 0.25},
}

def placement_cost(row, layer, weights):
    s = LAYER_SCORES[layer]
    benefit = (
        weights["latency"] * row["latency_sensitivity"] * s["latency"]
        + weights["bandwidth"] * row["raw_data_volume"] * s["bandwidth"]
        + weights["privacy"] * row["privacy_requirement"] * s["privacy"]
        + weights["continuity"] * row["offline_requirement"] * s["continuity"]
        + weights["trust"] * row["trust_requirement"] * s["trust"]
        + weights["assurance"] * s["assurance"]
    )
    return round(weights["management"] * s["management"] - benefit, 4)

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)
    weights = yaml.safe_load((root / "config/workload_placement_policy.yml").read_text())["workload_placement_policy"]["weights"]
    placement = pd.read_csv(root / "data/workload_placement_matrix.csv")
    layers = list(LAYER_SCORES)
    for layer in layers:
        placement[f"cost_{layer}"] = placement.apply(lambda r: placement_cost(r, layer, weights), axis=1)
    placement["recommended_layer"] = placement[[f"cost_{x}" for x in layers]].idxmin(axis=1).str.replace("cost_", "", regex=False)
    placement["placement_matches_recommendation"] = placement["assigned_layer"] == placement["recommended_layer"]
    placement["version_compliant"] = placement["active_version"] == placement["approved_version"]
    placement.to_csv(out / "python_workload_placement_scores.csv", index=False)

    fleet = pd.read_csv(root / "data/sample_edge_fleet_inventory.csv")
    fleet["latency_violation"] = fleet["latency_ms"] > fleet["latency_budget_ms"]
    fleet["version_skew"] = fleet["active_version"] != fleet["approved_version"]
    fleet["trust_verified"] = fleet["trust_state"] == "verified"
    fleet["runtime_ready"] = fleet["runtime_assurance_state"] == "ready"
    summary = pd.DataFrame([{
        "workloads": len(placement),
        "placement_match_rate": placement["placement_matches_recommendation"].mean(),
        "workload_version_compliance_rate": placement["version_compliant"].mean(),
        "fleet_assets": len(fleet),
        "online_rate": (fleet["connectivity_state"] == "online").mean(),
        "latency_violation_rate": fleet["latency_violation"].mean(),
        "version_skew_rate": fleet["version_skew"].mean(),
        "trust_verified_rate": fleet["trust_verified"].mean(),
        "runtime_ready_rate": fleet["runtime_ready"].mean(),
        "offline_ready_rate": fleet["offline_ready"].mean(),
        "rollback_ready_rate": fleet["rollback_ready"].mean()
    }]).round(4)
    summary.to_csv(out / "python_edge_workload_placement_continuity_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
