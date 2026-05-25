package main

import (
	"fmt"
	"math"
)

func DailyEnergyWh(
	messagesPerDay int,
	sensingEnergyWh float64,
	processingEnergyWh float64,
	transmitEnergyWh float64,
	receiveEnergyWh float64,
	sleepEnergyWhPerDay float64,
	retries int,
) float64 {
	energyPerMessage :=
		sensingEnergyWh +
			processingEnergyWh +
			transmitEnergyWh*float64(retries) +
			receiveEnergyWh*float64(retries)

	return float64(messagesPerDay)*energyPerMessage + sleepEnergyWhPerDay
}

func BatteryLifeDays(batteryWh float64, dailyEnergy float64) float64 {
	if dailyEnergy <= 0 {
		return 0
	}
	return batteryWh / dailyEnergy
}

func DeliveryProbability(singleAttemptSuccess float64, retries int) float64 {
	return 1.0 - math.Pow(1.0-singleAttemptSuccess, float64(retries))
}

func main() {
	energy := DailyEnergyWh(24, 0.001, 0.0005, 0.003, 0.001, 0.02, 2)
	life := BatteryLifeDays(20.0, energy)
	delivery := DeliveryProbability(0.80, 2)

	fmt.Printf("Daily energy use: %.4f Wh/day\n", energy)
	fmt.Printf("Battery life: %.2f days\n", life)
	fmt.Printf("Delivery probability: %.2f%%\n", delivery*100.0)
}
