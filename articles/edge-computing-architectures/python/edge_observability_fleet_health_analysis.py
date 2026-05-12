from pathlib import Path
import pandas as pd

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)
    fleet = pd.read_csv(root / "data/sample_edge_fleet_inventory.csv")
    fleet["latency_violation"] = fleet["latency_ms"] > fleet["latency_budget_ms"]
    fleet["version_skew"] = fleet["active_version"] != fleet["approved_version"]
    fleet["trust_verified"] = fleet["trust_state"] == "verified"
    fleet["runtime_ready"] = fleet["runtime_assurance_state"] == "ready"
    fleet["resource_pressure"] = (fleet["cpu_utilization"] > 0.85) | (fleet["memory_utilization"] > 0.85) | (fleet["storage_utilization"] > 0.90) | (fleet["thermal_state"] != "normal")
    summary = fleet.groupby(["site_id", "layer", "hardware_class", "workload_family"]).agg(
        assets=("asset_id","count"),
        online_rate=("connectivity_state", lambda s: (s == "online").mean()),
        degraded_rate=("health_state", lambda s: (s == "degraded").mean()),
        latency_violation_rate=("latency_violation","mean"),
        mean_buffer_backlog=("buffer_backlog","mean"),
        offline_ready_rate=("offline_ready","mean"),
        version_skew_rate=("version_skew","mean"),
        trust_verified_rate=("trust_verified","mean"),
        runtime_ready_rate=("runtime_ready","mean"),
        watchdog_reset_rate=("watchdog_resets", lambda s: (s > 0).mean()),
        resource_pressure_rate=("resource_pressure","mean"),
        rollback_ready_rate=("rollback_ready","mean")
    ).reset_index().round(4)
    summary.to_csv(out / "python_edge_observability_fleet_health_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
