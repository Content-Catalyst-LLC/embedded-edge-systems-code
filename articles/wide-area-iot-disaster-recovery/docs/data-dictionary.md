# Data Dictionary

## disaster_iot_scenarios_synthetic.csv

| Field | Description |
|---|---|
| scenario_id | Synthetic scenario identifier |
| protocol | Wide-area IoT protocol category |
| hazard_context | Disaster or recovery context |
| node_type | Example remote IoT node |
| battery_wh | Battery capacity in watt-hours |
| messages_per_day | Scheduled messages per day |
| sensing_energy_wh | Energy per sensing event |
| processing_energy_wh | Energy per local processing event |
| transmit_energy_wh | Energy per transmission attempt |
| receive_energy_wh | Energy for acknowledgment/listening window |
| sleep_energy_wh_per_day | Sleep-mode energy per day |
| single_attempt_success | Probability that one transmission attempt succeeds |
| retries | Transmission attempts per message |
| sense_latency_s | Sensing interval or detection delay in seconds |
| queue_latency_s | Device queueing delay in seconds |
| tx_latency_s | Transmission delay in seconds |
| backhaul_latency_s | Gateway or network backhaul delay in seconds |
| process_latency_s | Processing delay in seconds |
| notify_latency_s | Notification delay in seconds |
| terrain_difficulty | Simplified terrain difficulty category |
| community_priority | Simplified priority category |

## protocol_comparison_synthetic.csv

| Field | Description |
|---|---|
| protocol | Protocol category |
| spectrum_model | Licensed, unlicensed, or satellite/non-terrestrial model |
| typical_strength | High-level technical strength |
| main_dependency | Primary dependency or system assumption |
| bandwidth_profile | Relative bandwidth profile |
| energy_profile | Relative device energy profile |
| disaster_best_fit | Strongest disaster-recovery use cases |
| key_limitation | Major deployment limitation |
