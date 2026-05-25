#include <cmath>
#include <iostream>

double daily_energy_wh(
    int messages_per_day,
    double sensing_energy_wh,
    double processing_energy_wh,
    double transmit_energy_wh,
    double receive_energy_wh,
    double sleep_energy_wh_per_day,
    int retries
) {
    const double energy_per_message =
        sensing_energy_wh +
        processing_energy_wh +
        transmit_energy_wh * retries +
        receive_energy_wh * retries;

    return messages_per_day * energy_per_message + sleep_energy_wh_per_day;
}

double battery_life_days(double battery_wh, double daily_energy) {
    if (daily_energy <= 0.0) {
        return 0.0;
    }
    return battery_wh / daily_energy;
}

double delivery_probability(double single_attempt_success, int retries) {
    return 1.0 - std::pow(1.0 - single_attempt_success, retries);
}

int main() {
    const double energy = daily_energy_wh(24, 0.001, 0.0005, 0.003, 0.001, 0.02, 2);
    const double life = battery_life_days(20.0, energy);
    const double delivery = delivery_probability(0.80, 2);

    std::cout << "Daily energy use: " << energy << " Wh/day\n";
    std::cout << "Battery life: " << life << " days\n";
    std::cout << "Delivery probability: " << delivery * 100.0 << "%\n";

    return 0;
}
