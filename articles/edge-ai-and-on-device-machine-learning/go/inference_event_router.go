// Go Example: Inference Event Router, Model Inventory, and Fleet Health API Scaffold

package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type InferenceEvent struct {
	DeviceID               string  `json:"device_id"`
	DeviceClass            string  `json:"device_class"`
	RuntimeBackend          string  `json:"runtime_backend"`
	ModelVersion            string  `json:"model_version"`
	ApprovedModelVersion    string  `json:"approved_model_version"`
	LatencyMS               float64 `json:"latency_ms"`
	P95BudgetMS             float64 `json:"p95_budget_ms"`
	Confidence              float64 `json:"confidence"`
	ConfidenceThreshold     float64 `json:"confidence_threshold"`
	SensorHealth            string  `json:"sensor_health"`
	FallbackUsed            bool    `json:"fallback_used"`
	DriftProxy              float64 `json:"drift_proxy"`
	BackendOutputDelta      float64 `json:"backend_output_delta"`
	BackendDeltaTolerance   float64 `json:"backend_delta_tolerance"`
	MemoryOK                bool    `json:"memory_ok"`
	LatencyOK               bool    `json:"latency_ok"`
	LocalAction             string  `json:"local_action"`
}

func Route(event InferenceEvent) []string {
	var routes []string

	routes = append(routes, "inference_events")

	if event.ModelVersion != event.ApprovedModelVersion {
		routes = append(routes, "model_version_skew_events")
	}

	if event.LatencyMS > event.P95BudgetMS || !event.LatencyOK {
		routes = append(routes, "latency_violation_events")
	}

	if !event.MemoryOK {
		routes = append(routes, "memory_budget_events")
	}

	if event.Confidence < event.ConfidenceThreshold || event.FallbackUsed {
		routes = append(routes, "confidence_fallback_events")
	}

	if event.BackendOutputDelta > event.BackendDeltaTolerance {
		routes = append(routes, "backend_validation_events")
	}

	if event.DriftProxy > 0.15 {
		routes = append(routes, "drift_proxy_events")
	}

	if event.LocalAction == "local_alarm" {
		routes = append(routes, "local_alarm_events")
	}

	return routes
}

func main() {
	raw := []byte(`{
		"device_id": "dev-ai-006",
		"device_class": "pynq_device",
		"runtime_backend": "pynq_fpga",
		"model_version": "model-1.2",
		"approved_model_version": "model-1.2",
		"latency_ms": 7.8,
		"p95_budget_ms": 20,
		"confidence": 0.89,
		"confidence_threshold": 0.80,
		"sensor_health": "healthy",
		"fallback_used": false,
		"drift_proxy": 0.07,
		"backend_output_delta": 0.031,
		"backend_delta_tolerance": 0.025,
		"memory_ok": true,
		"latency_ok": true,
		"local_action": "local_alarm"
	}`)

	var event InferenceEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	routes := Route(event)
	fmt.Println("Routes:")
	for _, route := range routes {
		fmt.Println("-", route)
	}
}
