// Go Example: Robot Telemetry Gateway and Control-Event Router

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
)

type ControlEvent struct {
	RobotID          string  `json:"robot_id"`
	JointID          string  `json:"joint_id"`
	Setpoint         float64 `json:"setpoint"`
	MeasuredPosition float64 `json:"measured_position"`
	Command          float64 `json:"command"`
	LoopJitterMS     float64 `json:"loop_jitter_ms"`
	Saturated        bool    `json:"saturated"`
}

func Validate(event ControlEvent) []string {
	var issues []string

	trackingError := event.Setpoint - event.MeasuredPosition

	if math.Abs(trackingError) >= 0.15 {
		issues = append(issues, "tracking error fault")
	} else if math.Abs(trackingError) >= 0.08 {
		issues = append(issues, "tracking error warning")
	}

	if event.LoopJitterMS >= 5.0 {
		issues = append(issues, "loop jitter fault")
	} else if event.LoopJitterMS >= 2.0 {
		issues = append(issues, "loop jitter warning")
	}

	if math.Abs(event.Command) > 1.0 {
		issues = append(issues, "command bound violation")
	}

	if event.Saturated {
		issues = append(issues, "actuator saturated")
	}

	return issues
}

func main() {
	raw := []byte(`{
		"robot_id": "robot-001",
		"joint_id": "joint-1",
		"setpoint": 0.40,
		"measured_position": 0.35,
		"command": 0.90,
		"loop_jitter_ms": 1.4,
		"saturated": false
	}`)

	var event ControlEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	issues := Validate(event)
	fmt.Println("Telemetry accepted:", len(issues) == 0)

	for _, issue := range issues {
		fmt.Println("-", issue)
	}
}
