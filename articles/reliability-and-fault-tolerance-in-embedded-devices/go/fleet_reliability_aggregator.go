package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open("../data/fault_events.csv")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	rows, err := csv.NewReader(f).ReadAll()
	if err != nil {
		panic(err)
	}

	header := rows[0]
	idx := map[string]int{}
	for i, h := range header {
		idx[h] = i
	}

	events := len(rows) - 1
	detected := 0
	recovered := 0
	serviceLoss := 0.0
	safeStates := 0

	for _, row := range rows[1:] {
		if row[idx["detected"]] == "true" {
			detected++
		}
		if row[idx["recovery_success"]] == "true" {
			recovered++
		}
		if row[idx["safe_state_entered"]] == "true" {
			safeStates++
		}
		loss, _ := strconv.ParseFloat(row[idx["service_loss_s"]], 64)
		serviceLoss += loss
	}

	fmt.Printf(
		"events=%d detected=%d recovered=%d safe_states=%d service_loss_s=%.1f\n",
		events, detected, recovered, safeStates, serviceLoss,
	)
}
