// Go Example: Security Telemetry Gateway

package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type SecurityEvent struct {
	DeviceID        string `json:"device_id"`
	EventType       string `json:"event_type"`
	Severity        string `json:"severity"`
	FirmwareVersion string `json:"firmware_version"`
	SupportState    string `json:"support_state"`
	TrustState      string `json:"trust_state"`
}

func ValidateEvent(event SecurityEvent) []string {
	var issues []string

	if event.DeviceID == "" {
		issues = append(issues, "missing device_id")
	}
	if event.EventType == "" {
		issues = append(issues, "missing event_type")
	}
	if event.TrustState == "" {
		issues = append(issues, "missing trust_state")
	}
	if event.SupportState == "end-of-support" && event.Severity != "critical" {
		issues = append(issues, "end-of-support devices should emit critical security events")
	}

	return issues
}

func main() {
	raw := []byte(`{
		"device_id": "gw-chi-001",
		"event_type": "boot_verified",
		"severity": "info",
		"firmware_version": "3.5.1",
		"support_state": "supported",
		"trust_state": "trusted"
	}`)

	var event SecurityEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	issues := ValidateEvent(event)
	fmt.Println("Security telemetry valid:", len(issues) == 0)
	for _, issue := range issues {
		fmt.Println("-", issue)
	}
}
