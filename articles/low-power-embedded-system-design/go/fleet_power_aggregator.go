package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open("../data/device_power_telemetry.csv")
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

	lowBattery := 0
	wakeStorm := 0
	poorSleep := 0
	retries := 0

	for _, row := range rows[1:] {
		battery, _ := strconv.ParseFloat(row[idx["battery_v"]], 64)
		falseWakes, _ := strconv.Atoi(row[idx["false_wake_count_24h"]])
		sleep, _ := strconv.ParseFloat(row[idx["sleep_residency_pct"]], 64)
		retry, _ := strconv.Atoi(row[idx["retry_count_24h"]])

		if battery < 3.55 {
			lowBattery++
		}
		if falseWakes > 10 {
			wakeStorm++
		}
		if sleep < 92 {
			poorSleep++
		}
		if retry > 8 {
			retries++
		}
	}

	fmt.Printf("devices=%d low_battery=%d wake_storm=%d poor_sleep=%d retry_risk=%d\n",
		len(rows)-1, lowBattery, wakeStorm, poorSleep, retries)
}
