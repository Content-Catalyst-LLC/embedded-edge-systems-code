package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open("../data/rtos_fleet_telemetry.csv")
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

	deadlineRisk := 0
	queueRisk := 0
	stackRisk := 0
	isrRisk := 0
	watchdogRisk := 0

	for _, row := range rows[1:] {
		deadlines, _ := strconv.Atoi(row[idx["deadline_misses_24h"]])
		overflows, _ := strconv.Atoi(row[idx["queue_overflows_24h"]])
		stackWatermark, _ := strconv.Atoi(row[idx["min_stack_watermark_bytes"]])
		isrTime, _ := strconv.ParseFloat(row[idx["max_isr_time_us"]], 64)
		watchdog, _ := strconv.Atoi(row[idx["watchdog_resets"]])

		if deadlines > 0 {
			deadlineRisk++
		}
		if overflows > 0 {
			queueRisk++
		}
		if stackWatermark < 512 {
			stackRisk++
		}
		if isrTime > 250 {
			isrRisk++
		}
		if watchdog > 0 {
			watchdogRisk++
		}
	}

	fmt.Printf("devices=%d deadline_risk=%d queue_risk=%d stack_risk=%d isr_risk=%d watchdog_risk=%d\n",
		len(rows)-1, deadlineRisk, queueRisk, stackRisk, isrRisk, watchdogRisk)
}
