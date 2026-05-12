// Go Example: Local Privacy Gateway Service
//
// This example simulates local transformation before upstream disclosure.

package main

import (
	"encoding/json"
	"fmt"
	"log"
)

type Observation struct {
	DeviceID        string  `json:"device_id"`
	SignalType      string  `json:"signal_type"`
	Value           float64 `json:"value"`
	PersonRevealing bool    `json:"person_revealing"`
}

type DisclosureEvent struct {
	DeviceID         string `json:"device_id"`
	OutputType       string `json:"output_type"`
	PrivacyTransform string `json:"privacy_transform"`
	UpstreamAllowed  bool   `json:"upstream_allowed"`
}

func Transform(obs Observation) DisclosureEvent {
	output := "aggregate_state"
	if obs.SignalType == "video" && obs.Value > 0.5 {
		output = "zone_occupied"
	}
	if obs.SignalType == "audio" && obs.Value > 0.7 {
		output = "wake_word_event"
	}

	return DisclosureEvent{
		DeviceID:         obs.DeviceID,
		OutputType:       output,
		PrivacyTransform: "local_event_extraction",
		UpstreamAllowed:  !obs.PersonRevealing,
	}
}

func main() {
	raw := []byte(`{"device_id":"edge-001","signal_type":"video","value":0.76,"person_revealing":true}`)

	var obs Observation
	if err := json.Unmarshal(raw, &obs); err != nil {
		log.Fatal(err)
	}

	event := Transform(obs)
	encoded, _ := json.MarshalIndent(event, "", "  ")
	fmt.Println(string(encoded))
}
