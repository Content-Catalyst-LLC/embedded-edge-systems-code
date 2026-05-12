// Go Example: CPS Event Gateway and Interface Telemetry Router

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
)

type CpsEvent struct {
	DeviceID          string  `json:"device_id"`
	Subsystem         string  `json:"subsystem"`
	OperatingMode     string  `json:"operating_mode"`
	SensorAgeMS       float64 `json:"sensor_age_ms"`
	Measurement       float64 `json:"measurement"`
	Estimate          float64 `json:"estimate"`
	CandidateCommand  float64 `json:"candidate_command"`
	FilteredCommand   float64 `json:"filtered_command"`
	ActuatorSaturated bool    `json:"actuator_saturated"`
	DeadlineMissed    bool    `json:"deadline_missed"`
	LoopJitterMS      float64 `json:"loop_jitter_ms"`
	DeadlineSlackMS   float64 `json:"deadline_slack_ms"`
	InterfaceError    bool    `json:"interface_error"`
	SafetyState        string  `json:"safety_state"`
	TotalUncertainty  float64 `json:"total_uncertainty"`
	UncertaintyBudget float64 `json:"uncertainty_budget"`
}

func Validate(event CpsEvent) []string {
	var issues []string

	if event.DeviceID == "" {
		issues = append(issues, "missing device_id")
	}

	if event.SensorAgeMS > 3.0 {
		issues = append(issues, "sensor freshness violation")
	}

	if event.DeadlineMissed || event.DeadlineSlackMS < 0.0 {
		issues = append(issues, "deadline violation")
	}

	if math.Abs(event.LoopJitterMS) > 0.35 {
		issues = append(issues, "jitter outside budget")
	}

	if event.CandidateCommand != event.FilteredCommand {
		issues = append(issues, "runtime assurance modified command")
	}

	if event.TotalUncertainty > event.UncertaintyBudget {
		issues = append(issues, "uncertainty budget violation")
	}

	if event.InterfaceError {
		issues = append(issues, "interface error")
	}

	if event.SafetyState != "normal" {
		issues = append(issues, "non-normal safety state")
	}

	return issues
}

func main() {
	raw := []byte(`{
		"device_id": "cps-001",
		"subsystem": "motor-control",
		"operating_mode": "warning",
		"sensor_age_ms": 1.4,
		"measurement": 1110,
		"estimate": 1119,
		"candidate_command": 1.18,
		"filtered_command": 1.00,
		"actuator_saturated": true,
		"deadline_missed": false,
		"loop_jitter_ms": 0.30,
		"deadline_slack_ms": 0.62,
		"interface_error": false,
		"safety_state": "warning",
		"total_uncertainty": 24.8,
		"uncertainty_budget": 35.0
	}`)

	var event CpsEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	issues := Validate(event)
	fmt.Println("CPS event accepted:", len(issues) == 0)

	for _, issue := range issues {
		fmt.Println("-", issue)
	}
}
