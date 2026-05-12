package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open("../data/candidate_platforms.csv")
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

	platforms := len(rows) - 1
	secureBoot := 0
	debugLock := 0
	highLifecycle := 0
	socCount := 0

	for _, row := range rows[1:] {
		if row[idx["platform_type"]] == "soc" || row[idx["platform_type"]] == "hybrid" {
			socCount++
		}
		if row[idx["secure_boot"]] == "true" {
			secureBoot++
		}
		if row[idx["debug_lock"]] == "true" {
			debugLock++
		}
		score, _ := strconv.Atoi(row[idx["lifecycle_support_score"]])
		if score >= 8 {
			highLifecycle++
		}
	}

	fmt.Printf("platforms=%d soc_or_hybrid=%d secure_boot=%d debug_lock=%d high_lifecycle=%d\n",
		platforms, socCount, secureBoot, debugLock, highLifecycle)
}
