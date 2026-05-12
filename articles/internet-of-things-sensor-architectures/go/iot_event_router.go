package main

import "fmt"

type IoTEvent struct {
    EventID string
    DeviceID string
    QualityState string
    TrustState string
    Fresh bool
    DuplicateDetected bool
    FirmwareCompliant bool
    ConfigCompliant bool
    SchemaCompliant bool
    CommandRelated bool
}

func Routes(event IoTEvent) []string {
    routes := []string{"telemetry_archive"}

    if !event.Fresh {
        routes = append(routes, "stale_telemetry_events")
    }
    if event.DuplicateDetected {
        routes = append(routes, "duplicate_replay_events")
    }
    if event.QualityState != "valid" {
        routes = append(routes, "quality_events")
    }
    if event.TrustState != "verified" {
        routes = append(routes, "trust_boundary_events")
    }
    if !event.FirmwareCompliant || !event.ConfigCompliant || !event.SchemaCompliant {
        routes = append(routes, "version_skew_events")
    }
    if event.CommandRelated {
        routes = append(routes, "command_audit_events")
    }

    return routes
}

func main() {
    event := IoTEvent{"evt-005", "dev-vib-002", "valid", "unverified", false, false, false, true, false, false}
    for _, route := range Routes(event) {
        fmt.Println("-", route)
    }
}
