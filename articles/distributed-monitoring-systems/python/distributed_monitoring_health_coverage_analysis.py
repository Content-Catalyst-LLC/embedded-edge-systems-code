from pathlib import Path
import pandas as pd
import yaml

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs"
    out.mkdir(exist_ok=True)

    timing = yaml.safe_load((root / "config/timing_policy.yml").read_text())["timing_policy"]

    nodes = pd.read_csv(root / "data/node_inventory.csv")
    zones = pd.read_csv(root / "data/topology_zones.csv")
    gateways = pd.read_csv(root / "data/gateway_state.csv")
    telemetry = pd.read_csv(
        root / "data/telemetry_records.csv",
        parse_dates=["event_time", "upload_time", "ingestion_time", "processing_time"]
    )

    nodes["active"] = (
        (nodes["connectivity_state"] == "online")
        & (nodes["health_state"] == "healthy")
        & (nodes["calibration_state"] == "valid")
    )
    nodes["heartbeat_fresh"] = nodes["heartbeat_age_seconds"] <= (2 * nodes["expected_reporting_interval_seconds"])
    nodes["node_usable"] = nodes["active"] & nodes["heartbeat_fresh"]

    gateways["buffer_pressure"] = gateways["buffer_depth"] / gateways["buffer_capacity"]
    gateways["child_reporting_rate"] = gateways["child_nodes_reporting"] / gateways["child_node_count"]
    gateways["rule_compliant"] = gateways["active_rule_version"] == gateways["approved_rule_version"]
    gateways["gateway_usable"] = (
        (gateways["connectivity_state"] == "online")
        & (gateways["health_state"] == "healthy")
        & (gateways["buffer_pressure"] <= 0.60)
        & gateways["rule_compliant"]
        & gateways["transformation_lineage_preserved"]
    )

    telemetry["freshness_seconds"] = (telemetry["processing_time"] - telemetry["event_time"]).dt.total_seconds()
    telemetry["fresh"] = telemetry["freshness_seconds"] <= timing["freshness_threshold_seconds"]
    telemetry["synchronized"] = telemetry["clock_skew_ms"].abs() <= timing["max_allowed_clock_skew_ms"]
    telemetry["usable"] = (
        telemetry["fresh"]
        & telemetry["synchronized"]
        & (telemetry["quality_state"] == "valid")
        & (telemetry["calibration_state"] == "valid")
        & (~telemetry["duplicate_detected"])
    )

    active_by_zone = nodes.groupby("coverage_zone", as_index=False).agg(
        active_nodes=("node_usable", "sum"),
        total_nodes=("node_id", "count"),
        reference_nodes=("node_role", lambda s: (s == "reference").sum())
    )
    coverage = zones.merge(active_by_zone, on="coverage_zone", how="left").fillna({"active_nodes": 0, "total_nodes": 0, "reference_nodes": 0})
    coverage["coverage_complete"] = coverage["active_nodes"] >= coverage["required_nodes"]
    coverage["reference_requirement_met"] = coverage["reference_nodes"] >= coverage["min_reference_nodes"]
    coverage["coverage_status"] = coverage.apply(
        lambda r: "observed_valid" if r["coverage_complete"] and r["reference_requirement_met"] else "coverage_degraded",
        axis=1
    )

    nodes.to_csv(out / "python_nodes_scored.csv", index=False)
    gateways.to_csv(out / "python_gateways_scored.csv", index=False)
    telemetry.to_csv(out / "python_telemetry_scored.csv", index=False)
    coverage.to_csv(out / "python_coverage_scored.csv", index=False)

    summary = pd.DataFrame([{
        "nodes": len(nodes),
        "node_usable_rate": nodes["node_usable"].mean(),
        "coverage_completeness_rate": coverage["coverage_complete"].mean(),
        "reference_requirement_met_rate": coverage["reference_requirement_met"].mean(),
        "gateway_usable_rate": gateways["gateway_usable"].mean(),
        "mean_gateway_buffer_pressure": gateways["buffer_pressure"].mean(),
        "usable_telemetry_rate": telemetry["usable"].mean(),
        "stale_telemetry_rate": (~telemetry["fresh"]).mean(),
        "clock_skew_violation_rate": (~telemetry["synchronized"]).mean(),
        "duplicate_replay_rate": telemetry["duplicate_detected"].mean(),
        "mean_freshness_seconds": telemetry["freshness_seconds"].mean()
    }]).round(4)

    summary.to_csv(out / "python_distributed_monitoring_health_summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
