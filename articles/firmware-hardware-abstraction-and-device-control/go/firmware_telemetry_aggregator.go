package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open("../data/firmware_fleet_telemetry.csv")
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

	driverRisk := 0
	resumeRisk := 0
	updateRisk := 0
	totalFaults := 0

	for _, row := range rows[1:] {
		driverErrors, _ := strconv.Atoi(row[idx["driver_errors"]])
		resumeFailures, _ := strconv.Atoi(row[idx["suspend_resume_failures"]])
		rollbacks, _ := strconv.Atoi(row[idx["rollback_count"]])
		watchdog, _ := strconv.Atoi(row[idx["watchdog_resets"]])
		busTimeouts, _ := strconv.Atoi(row[idx["bus_timeouts"]])

		totalFaults += driverErrors + resumeFailures + rollbacks + watchdog + busTimeouts

		if driverErrors > 3 {
			driverRisk++
		}
		if resumeFailures > 2 {
			resumeRisk++
		}
		if rollbacks > 0 {
			updateRisk++
		}
	}

	fmt.Printf("devices=%d total_faults=%d driver_risk=%d resume_risk=%d update_risk=%d\n",
		len(rows)-1, totalFaults, driverRisk, resumeRisk, updateRisk)
}
