package main

import "fmt"

type MonitoringEvent struct {
    EventID string
    NodeID string
    CoverageZone string
    MonitoringState string
    Fresh bool
    Synchronized bool
    DuplicateDetected bool
    CoverageComplete bool
    GatewayBufferPressure float64
}

func Routes(event MonitoringEvent) []string {
    routes := []string{"monitoring_archive"}

    if !event.Fresh {
        routes = append(routes, "stale_monitoring_events")
    }
    if !event.Synchronized {
        routes = append(routes, "clock_sync_events")
    }
    if event.DuplicateDetected {
        routes = append(routes, "duplicate_replay_events")
    }
    if !event.CoverageComplete {
        routes = append(routes, "coverage_gap_events")
    }
    if event.GatewayBufferPressure > 0.6 {
        routes = append(routes, "gateway_pressure_events")
    }
    if event.MonitoringState != "observed_valid" {
        routes = append(routes, "fault_containment_events")
    }

    return routes
}

func main() {
    event := MonitoringEvent{"evt-water-003", "node-water-downstream-001", "zone-downstream", "sync_degraded", false, false, false, true, 0.02}
    for _, route := range Routes(event) {
        fmt.Println("-", route)
    }
}
