fn daily_energy_wh(
    messages_per_day: u32,
    sensing_energy_wh: f64,
    processing_energy_wh: f64,
    transmit_energy_wh: f64,
    receive_energy_wh: f64,
    sleep_energy_wh_per_day: f64,
    retries: u32,
) -> f64 {
    let energy_per_message =
        sensing_energy_wh +
        processing_energy_wh +
        transmit_energy_wh * retries as f64 +
        receive_energy_wh * retries as f64;

    messages_per_day as f64 * energy_per_message + sleep_energy_wh_per_day
}

fn battery_life_days(battery_wh: f64, daily_energy: f64) -> f64 {
    if daily_energy <= 0.0 {
        0.0
    } else {
        battery_wh / daily_energy
    }
}

fn delivery_probability(single_attempt_success: f64, retries: u32) -> f64 {
    1.0 - (1.0 - single_attempt_success).powf(retries as f64)
}

fn main() {
    let energy = daily_energy_wh(24, 0.001, 0.0005, 0.003, 0.001, 0.02, 2);
    let life = battery_life_days(20.0, energy);
    let delivery = delivery_probability(0.80, 2);

    println!("Daily energy use: {:.4} Wh/day", energy);
    println!("Battery life: {:.2} days", life);
    println!("Delivery probability: {:.2}%", delivery * 100.0);
}
