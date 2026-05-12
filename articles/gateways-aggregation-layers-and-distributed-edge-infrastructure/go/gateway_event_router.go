// Go Example: Gateway Event Router, Selective Uplink Service, and Health API Scaffold

package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type GatewayEvent struct {
	EventID                    string  `json:"event_id"`
	SiteID                     string  `json:"site_id"`
	GatewayID                  string  `json:"gateway_id"`
	DeviceID                   string  `json:"device_id"`
	ProtocolFamily             string  `json:"protocol_family"`
	QualityFlag                string  `json:"quality_flag"`
	DeviceFreshnessS           float64 `json:"device_freshness_s"`
	ChildDeviceStatus          string  `json:"child_device_status"`
	ProtocolError              bool    `json:"protocol_error"`
	BufferBacklog              int     `json:"buffer_backlog"`
	ReplayLagS                 float64 `json:"replay_lag_s"`
	ForwardedUpstream          bool    `json:"forwarded_upstream"`
	LineageComplete            bool    `json:"lineage_complete"`
	SelectiveForwardingReason  string  `json:"selective_forwarding_reason"`
}

func Route(event GatewayEvent) []string {
	var routes []string

	routes = append(routes, "gateway_events")

	if event.ProtocolError {
		routes = append(routes, "protocol_error_events")
	}

	if event.ChildDeviceStatus == "missing" || event.DeviceFreshnessS > 60 {
		routes = append(routes, "child_device_freshness_events")
	}

	if event.BufferBacklog > 200 {
		routes = append(routes, "buffer_pressure_events")
	}

	if event.ReplayLagS > 120 {
		routes = append(routes, "replay_lag_events")
	}

	if !event.LineageComplete {
		routes = append(routes, "lineage_gap_events")
	}

	if event.SelectiveForwardingReason == "incident" || event.QualityFlag == "invalid" {
		routes = append(routes, "priority_uplink_events")
	}

	return routes
}

func main() {
	raw := []byte(`{
		"event_id": "evt-004",
		"site_id": "site-b",
		"gateway_id": "gw-002",
		"device_id": "dev-motor-001",
		"protocol_family": "can",
		"quality_flag": "valid",
		"device_freshness_s": 303,
		"child_device_status": "missing",
		"protocol_error": false,
		"buffer_backlog": 250,
		"replay_lag_s": 303,
		"forwarded_upstream": true,
		"lineage_complete": true,
		"selective_forwarding_reason": "replay_after_outage"
	}`)

	var event GatewayEvent
	if err := json.Unmarshal(raw, &event); err != nil {
		log.Fatal(err)
	}

	routes := Route(event)
	fmt.Println("Routes:")
	for _, route := range routes {
		fmt.Println("-", route)
	}
}
