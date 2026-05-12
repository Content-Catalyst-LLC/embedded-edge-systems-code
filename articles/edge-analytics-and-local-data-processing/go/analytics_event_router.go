// Go Example: Analytics Event Router, Selective Uplink Service, and Local Health API Scaffold

package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type AnalyticsEvent struct {
	EventID              string  `json:"event_id"`
	SiteID               string  `json:"site_id"`
	GatewayID            string  `json:"gateway_id"`
	SignalID             string  `json:"signal_id"`
	SignalFamily         string  `json:"signal_family"`
	FeatureVersion       string  `json:"feature_version"`
	RuleVersion          string  `json:"rule_version"`
	WindowID             string  `json:"window_id"`
	LocalLatencyMS        float64 `json:"local_latency_ms"`
	FreshnessS           float64 `json:"freshness_s"`
	FreshnessThresholdS  float64 `json:"freshness_threshold_s"`
	MissingSampleRate    float64 `json:"missing_sample_rate"`
	FeatureComplete      bool    `json:"feature_complete"`
	EventDetected         bool    `json:"event_detected"`
	EventState            string  `json:"event_state"`
	UplinkMode            string  `json:"uplink_mode"`
	BufferBacklog         int     `json:"buffer_backlog"`
	ReplayLagS            float64 `json:"replay_lag_s"`
	LineageComplete       bool    `json:"lineage_complete"`
	DropReason            string  `json:"drop_reason"`
	QualityFlag           string  `json:"quality_flag"`
}

func Route(event AnalyticsEvent) []string {
	var routes []string

	routes = append(routes, "analytics_events")

	if event.EventDetected {
		routes = append(routes, "local_event_records")
	}

	if event.EventState == "fault" || event.EventState == "warning" {
		routes = append(routes, "priority_uplink_events")
	}

	if event.FreshnessS > event.FreshnessThresholdS {
		routes = append(routes, "stale_output_events")
	}

	if event.MissingSampleRate > 0.05 || !event.FeatureComplete {
		routes = append(routes, "feature_quality_events")
	}

	if event.BufferBacklog > 200 {
		routes = append(routes, "buffer_pressure_events")
	}

	if event.ReplayLagS > 300 {
		routes = append(routes, "replay_lag_events")
	}

	if !event.LineageComplete {
		routes = append(routes, "lineage_gap_events")
	}

	if event.UplinkMode == "suppressed" {
		routes = append(routes, "suppression_records")
	}

	return routes
}

func main() {
	raw := []byte(`{
		"event_id": "evt-004",
		"site_id": "site-b",
		"gateway_id": "gw-002",
		"signal_id": "current-main",
		"signal_family": "power",
		"feature_version": "features-1.1",
		"rule_version": "rules-1.1",
		"window_id": "win-004",
		"local_latency_ms": 24.4,
		"freshness_s": 330,
		"freshness_threshold_s": 60,
		"missing_sample_rate": 0.12,
		"feature_complete": false,
		"event_detected": true,
		"event_state": "fault",
		"uplink_mode": "suppressed",
		"buffer_backlog": 250,
		"replay_lag_s": 330,
		"lineage_complete": false,
		"drop_reason": "missing_feature_context",
		"quality_flag": "invalid"
	}`)

	var event AnalyticsEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	routes := Route(event)
	fmt.Println("Routes:")
	for _, route := range routes {
		fmt.Println("-", route)
	}
}
