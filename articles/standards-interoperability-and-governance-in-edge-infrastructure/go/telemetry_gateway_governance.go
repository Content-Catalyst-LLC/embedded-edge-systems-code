// Go Example: Telemetry Gateway Governance Service
//
// This example simulates a lightweight governance check that can be embedded
// into a telemetry gateway before forwarding edge events upstream.

package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type TelemetryEvent struct {
	DeviceID      string  `json:"device_id"`
	Metric        string  `json:"metric"`
	Value         float64 `json:"value"`
	Unit          string  `json:"unit"`
	SchemaVersion string  `json:"schema_version"`
	QualityFlag   string  `json:"quality_flag"`
}

func ValidateEvent(event TelemetryEvent) []string {
	var issues []string

	if event.DeviceID == "" {
		issues = append(issues, "missing device_id")
	}
	if event.SchemaVersion == "" {
		issues = append(issues, "missing schema_version")
	}
	if event.Unit == "" {
		issues = append(issues, "missing unit")
	}
	if event.QualityFlag == "" {
		issues = append(issues, "missing quality_flag")
	}

	return issues
}

func main() {
	raw := []byte(`{
		"device_id": "gw-chi-001",
		"metric": "latency_ms",
		"value": 18.4,
		"unit": "ms",
		"schema_version": "v2",
		"quality_flag": "good"
	}`)

	var event TelemetryEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	issues := ValidateEvent(event)
	if len(issues) == 0 {
		fmt.Println("Telemetry governance validation: PASS")
	} else {
		fmt.Println("Telemetry governance validation: REVIEW")
		for _, issue := range issues {
			fmt.Println("-", issue)
		}
	}
}
