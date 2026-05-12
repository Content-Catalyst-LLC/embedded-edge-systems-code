package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func main() {
	f, err := os.Open("../data/environmental_measurements.csv")
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

	warnings := 0
	lowLink := 0
	maxBuffer := 0.0

	for _, row := range rows[1:] {
		if row[idx["quality_flag"]] != "valid" && row[idx["quality_flag"]] != "event_valid" {
			warnings++
		}
		link, _ := strconv.ParseFloat(row[idx["link_quality"]], 64)
		if link < 0.60 {
			lowLink++
		}
		bufferAge, _ := strconv.ParseFloat(row[idx["buffer_age_s"]], 64)
		if bufferAge > maxBuffer {
			maxBuffer = bufferAge
		}
	}

	fmt.Printf("records=%d warnings=%d low_link_records=%d max_buffer_age_s=%.1f\n", len(rows)-1, warnings, lowLink, maxBuffer)
}
