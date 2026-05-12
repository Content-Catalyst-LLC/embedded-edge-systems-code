// Go Example: Gateway Sync Service and Cloud-Edge Health Event Router

package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type HybridEvent struct {
	SiteID               string  `json:"site_id"`
	GatewayID            string  `json:"gateway_id"`
	OperatingMode        string  `json:"operating_mode"`
	CloudReachable       bool    `json:"cloud_reachable"`
	OfflineDurationS     float64 `json:"offline_duration_s"`
	StateAgeS            float64 `json:"state_age_s"`
	SyncLagS             float64 `json:"sync_lag_s"`
	BufferBacklog        int     `json:"buffer_backlog"`
	EdgePolicyVersion    string  `json:"edge_policy_version"`
	CloudPolicyVersion   string  `json:"cloud_policy_version"`
	EdgeModelVersion     string  `json:"edge_model_version"`
	ApprovedModelVersion string  `json:"approved_model_version"`
	TargetVersion        string  `json:"target_version"`
	ActiveVersion        string  `json:"active_version"`
	ReconciliationStatus string  `json:"reconciliation_status"`
	AuthorityValid       bool    `json:"authority_valid"`
}

func Route(event HybridEvent) []string {
	var routes []string

	routes = append(routes, "hybrid_events")

	if !event.CloudReachable || event.OfflineDurationS > 0 {
		routes = append(routes, "connectivity_events")
	}

	if event.StateAgeS > 120 || event.SyncLagS > 60 {
		routes = append(routes, "synchronization_slo_events")
	}

	if event.EdgePolicyVersion != event.CloudPolicyVersion {
		routes = append(routes, "policy_drift_events")
	}

	if event.EdgeModelVersion != event.ApprovedModelVersion || event.ActiveVersion != event.TargetVersion {
		routes = append(routes, "model_lifecycle_events")
	}

	if event.ReconciliationStatus == "conflict" || event.ReconciliationStatus == "hold_for_review" {
		routes = append(routes, "reconciliation_review_events")
	}

	if !event.AuthorityValid {
		routes = append(routes, "authority_violation_events")
	}

	return routes
}

func main() {
	raw := []byte(`{
		"site_id": "site-b",
		"gateway_id": "gw-002",
		"operating_mode": "degraded",
		"cloud_reachable": false,
		"offline_duration_s": 520,
		"state_age_s": 525,
		"sync_lag_s": 520,
		"buffer_backlog": 300,
		"edge_policy_version": "policy-1.0",
		"cloud_policy_version": "policy-1.1",
		"edge_model_version": "model-2.0",
		"approved_model_version": "model-2.1",
		"target_version": "model-2.1",
		"active_version": "model-2.0",
		"reconciliation_status": "hold_for_review",
		"authority_valid": false
	}`)

	var event HybridEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	routes := Route(event)
	fmt.Println("Routes:")
	for _, route := range routes {
		fmt.Println("-", route)
	}
}
