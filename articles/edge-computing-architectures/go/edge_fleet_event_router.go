package main

import "fmt"

type EdgeAsset struct {
    AssetID string
    ConnectivityState string
    LatencyMS float64
    LatencyBudgetMS float64
    BufferBacklog int
    ActiveVersion string
    ApprovedVersion string
    TrustState string
    RuntimeAssuranceState string
    WatchdogResets int
    RollbackReady bool
}

func Route(a EdgeAsset) []string {
    routes := []string{"fleet_inventory"}
    if a.ConnectivityState != "online" { routes = append(routes, "connectivity_events") }
    if a.LatencyMS > a.LatencyBudgetMS { routes = append(routes, "latency_violations") }
    if a.BufferBacklog > 250 { routes = append(routes, "buffer_pressure_events") }
    if a.ActiveVersion != a.ApprovedVersion { routes = append(routes, "version_skew_events") }
    if a.TrustState != "verified" { routes = append(routes, "trust_boundary_events") }
    if a.RuntimeAssuranceState != "ready" || a.WatchdogResets > 0 { routes = append(routes, "runtime_assurance_events") }
    if !a.RollbackReady { routes = append(routes, "rollback_risk_events") }
    return routes
}

func main() {
    a := EdgeAsset{"gw-002", "degraded", 140, 100, 260, "gw-2.0", "gw-2.1", "verified", "degraded", 2, true}
    for _, route := range Route(a) { fmt.Println("-", route) }
}
