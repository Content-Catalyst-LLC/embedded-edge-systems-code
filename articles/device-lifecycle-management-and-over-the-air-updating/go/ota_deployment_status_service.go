// Go Example: OTA Deployment Status Service
//
// This example simulates a lightweight gateway service that classifies OTA
// deployment phase outcomes for reporting and escalation.

package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type DeploymentEvent struct {
	DeviceID  string `json:"device_id"`
	PackageID string `json:"package_id"`
	Phase     string `json:"phase"`
	Status    string `json:"status"`
	ErrorCode string `json:"error_code,omitempty"`
}

func Escalation(event DeploymentEvent) string {
	if event.Status == "failed" {
		return "incident-review"
	}
	if event.Status == "deferred" {
		return "retry-or-maintenance-window"
	}
	if event.Status == "succeeded" {
		return "record-evidence"
	}
	return "operator-review"
}

func main() {
	raw := []byte(`{
		"device_id": "plc-007",
		"package_id": "ota-5-9-1",
		"phase": "install",
		"status": "failed",
		"error_code": "ROLLBACK_NOT_READY"
	}`)

	var event DeploymentEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Device: %s\n", event.DeviceID)
	fmt.Printf("Escalation: %s\n", Escalation(event))
}
