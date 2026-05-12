package main

import "fmt"

type MeasurementEvent struct {
    MeasurementID string
    SensorID string
    QualityState string
    ExpandedUncertainty float64
    SNRdB float64
    LineageComplete bool
    TraceabilityComplete bool
}

func Routes(event MeasurementEvent) []string {
    routes := []string{"measurement_archive"}

    if event.QualityState != "valid" {
        routes = append(routes, "measurement_quality_events")
    }
    if event.QualityState == "calibration_expired" || event.QualityState == "coefficient_mismatch" {
        routes = append(routes, "calibration_control_events")
    }
    if event.SNRdB < 20.0 {
        routes = append(routes, "noise_diagnostics")
    }
    if event.ExpandedUncertainty > 1.5 {
        routes = append(routes, "uncertainty_review")
    }
    if !event.LineageComplete || !event.TraceabilityComplete {
        routes = append(routes, "provenance_gaps")
    }

    return routes
}

func main() {
    event := MeasurementEvent{"m-005", "temp-003", "coefficient_mismatch", 1.8, 12.0, false, false}
    for _, route := range Routes(event) {
        fmt.Println("-", route)
    }
}
