package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open("../data/acquisition_events.csv")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	reader := csv.NewReader(f)
	rows, err := reader.ReadAll()
	if err != nil {
		panic(err)
	}

	header := rows[0]
	index := map[string]int{}
	for i, h := range header {
		index[h] = i
	}

	warnings := 0
	maxJitter := 0.0
	for _, row := range rows[1:] {
		if row[index["quality_flag"]] != "valid" {
			warnings++
		}
		j, _ := strconv.ParseFloat(row[index["timestamp_jitter_ms"]], 64)
		if j > maxJitter {
			maxJitter = j
		}
	}

	fmt.Printf("events=%d warnings=%d max_timestamp_jitter_ms=%.2f\n", len(rows)-1, warnings, maxJitter)
}
