// Go Example: Autonomy Event Gateway and Decision Telemetry Router

package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type AutonomyEvent struct {
	DeviceID                  string  `json:"device_id"`
	MissionType               string  `json:"mission_type"`
	AutonomyLevel             string  `json:"autonomy_level"`
	BeliefState               string  `json:"belief_state"`
	DecisionConfidence        float64 `json:"decision_confidence"`
	CandidateAction           string  `json:"candidate_action"`
	FilteredAction            string  `json:"filtered_action"`
	LatencyMS                 float64 `json:"latency_ms"`
	LatencyBudgetMS           float64 `json:"latency_budget_ms"`
	SafetyState               string  `json:"safety_state"`
	HumanInterventionRequired bool    `json:"human_intervention_required"`
	InputDriftScore           float64 `json:"input_drift_score"`
}

func Validate(event AutonomyEvent) []string {
	var issues []string

	if event.DeviceID == "" {
		issues = append(issues, "missing device_id")
	}

	if event.LatencyMS > event.LatencyBudgetMS {
		issues = append(issues, "latency budget violation")
	}

	if event.DecisionConfidence < 0.70 {
		issues = append(issues, "low confidence decision")
	}

	if event.InputDriftScore >= 0.25 {
		issues = append(issues, "input drift warning")
	}

	if event.SafetyState != "normal" {
		issues = append(issues, "non-normal safety state")
	}

	if event.CandidateAction != event.FilteredAction {
		issues = append(issues, "runtime assurance modified or replaced candidate action")
	}

	return issues
}

func main() {
	raw := []byte(`{
		"device_id": "amr-001",
		"mission_type": "warehouse_delivery",
		"autonomy_level": "bounded_local",
		"belief_state": "obstacle_present",
		"decision_confidence": 0.82,
		"candidate_action": "reroute",
		"filtered_action": "reroute",
		"latency_ms": 56,
		"latency_budget_ms": 80,
		"safety_state": "normal",
		"human_intervention_required": false,
		"input_drift_score": 0.12
	}`)

	var event AutonomyEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	issues := Validate(event)
	fmt.Println("Autonomy event accepted:", len(issues) == 0)

	for _, issue := range issues {
		fmt.Println("-", issue)
	}
}
