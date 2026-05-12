from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)
    thresholds = yaml.safe_load((root / "config/runtime_assurance_policy.yml").read_text())["runtime_assurance_policy"]["thresholds"]
    fleet = pd.read_csv(root / "data/sample_edge_fleet_inventory.csv")
    fleet["cpu_pressure"] = fleet["cpu_utilization"] > thresholds["max_cpu_utilization"]
    fleet["memory_pressure"] = fleet["memory_utilization"] > thresholds["max_memory_utilization"]
    fleet["storage_pressure"] = fleet["storage_utilization"] > thresholds["max_storage_utilization"]
    fleet["clock_drift_violation"] = fleet["clock_drift_ms"] > thresholds["max_clock_drift_ms"]
    fleet["watchdog_violation"] = fleet["watchdog_resets"] > thresholds["max_watchdog_resets_per_hour"]
    fleet["buffer_pressure"] = fleet["buffer_backlog"] > thresholds["max_buffer_backlog"]
    fleet["runtime_degraded"] = fleet["runtime_assurance_state"] != "ready"
    fleet["should_enter_degraded_mode"] = fleet[["cpu_pressure","memory_pressure","storage_pressure","clock_drift_violation","watchdog_violation","buffer_pressure","runtime_degraded"]].any(axis=1) | (fleet["trust_state"] != "verified")
    fleet.to_csv(out / "python_runtime_assurance_degraded_mode_checks.csv", index=False)
    summary = pd.DataFrame([{
        "assets": len(fleet),
        "degraded_mode_entry_rate": fleet["should_enter_degraded_mode"].mean(),
        "watchdog_violation_rate": fleet["watchdog_violation"].mean(),
        "buffer_pressure_rate": fleet["buffer_pressure"].mean(),
        "clock_drift_violation_rate": fleet["clock_drift_violation"].mean()
    }]).round(4)
    summary.to_csv(out / "python_runtime_assurance_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
