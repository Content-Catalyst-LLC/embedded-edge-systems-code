// Go Example: Control Event Gateway and Timing Telemetry Router

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
)

type ControlLoopEvent struct {
	DeviceID           string  `json:"device_id"`
	LoopID             string  `json:"loop_id"`
	Setpoint           float64 `json:"setpoint"`
	Measurement        float64 `json:"measurement"`
	Estimate           float64 `json:"estimate"`
	ControlError       float64 `json:"control_error"`
	CandidateCommand   float64 `json:"candidate_command"`
	FilteredCommand    float64 `json:"filtered_command"`
	Saturated          bool    `json:"saturated"`
	DeadlineMissed     bool    `json:"deadline_missed"`
	LoopJitterMS       float64 `json:"loop_jitter_ms"`
	DeadlineSlackMS    float64 `json:"deadline_slack_ms"`
	SafetyState        string  `json:"safety_state"`
	SupervisoryState   string  `json:"supervisory_state"`
	SafetyFilterReason string  `json:"safety_filter_reason"`
}

func Validate(event ControlLoopEvent) []string {
	var issues []string

	if event.DeviceID == "" {
		issues = append(issues, "missing device_id")
	}

	if event.DeadlineMissed || event.DeadlineSlackMS < 0.0 {
		issues = append(issues, "deadline violation")
	}

	if math.Abs(event.LoopJitterMS) > 0.35 {
		issues = append(issues, "jitter outside budget")
	}

	if math.Abs(event.ControlError) >= 80.0 {
		issues = append(issues, "high control error")
	}

	if event.CandidateCommand != event.FilteredCommand {
		issues = append(issues, "safety filter modified command")
	}

	if event.SafetyState != "normal" {
		issues = append(issues, "non-normal safety state")
	}

	return issues
}

func main() {
	raw := []byte(`{
		"device_id": "ctrl-001",
		"loop_id": "motor-speed",
		"setpoint": 1200,
		"measurement": 1110,
		"estimate": 1119,
		"control_error": 81,
		"candidate_command": 1.18,
		"filtered_command": 1.00,
		"saturated": true,
		"deadline_missed": false,
		"loop_jitter_ms": 0.30,
		"deadline_slack_ms": 0.62,
		"safety_state": "warning",
		"supervisory_state": "warning",
		"safety_filter_reason": "command_clipped"
	}`)

	var event ControlLoopEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	issues := Validate(event)
	fmt.Println("Control event accepted:", len(issues) == 0)

	for _, issue := range issues {
		fmt.Println("-", issue)
	}
}
