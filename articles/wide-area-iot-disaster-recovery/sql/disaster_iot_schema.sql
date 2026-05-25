-- Wide-area IoT disaster recovery schema.
-- Synthetic data only.

DROP TABLE IF EXISTS disaster_iot_scenarios;

CREATE TABLE disaster_iot_scenarios (
    scenario_id TEXT PRIMARY KEY,
    protocol TEXT NOT NULL,
    hazard_context TEXT NOT NULL,
    node_type TEXT NOT NULL,
    battery_wh REAL NOT NULL,
    messages_per_day INTEGER NOT NULL,
    sensing_energy_wh REAL NOT NULL,
    processing_energy_wh REAL NOT NULL,
    transmit_energy_wh REAL NOT NULL,
    receive_energy_wh REAL NOT NULL,
    sleep_energy_wh_per_day REAL NOT NULL,
    single_attempt_success REAL NOT NULL,
    retries INTEGER NOT NULL,
    sense_latency_s REAL NOT NULL,
    queue_latency_s REAL NOT NULL,
    tx_latency_s REAL NOT NULL,
    backhaul_latency_s REAL NOT NULL,
    process_latency_s REAL NOT NULL,
    notify_latency_s REAL NOT NULL,
    terrain_difficulty TEXT NOT NULL,
    community_priority TEXT NOT NULL
);

DROP VIEW IF EXISTS disaster_iot_metrics;

CREATE VIEW disaster_iot_metrics AS
SELECT
    scenario_id,
    protocol,
    hazard_context,
    node_type,
    messages_per_day,
    retries,
    (
        sensing_energy_wh +
        processing_energy_wh +
        transmit_energy_wh * retries +
        receive_energy_wh * retries
    ) AS energy_per_message_wh,
    (
        messages_per_day *
        (
            sensing_energy_wh +
            processing_energy_wh +
            transmit_energy_wh * retries +
            receive_energy_wh * retries
        )
        + sleep_energy_wh_per_day
    ) AS daily_energy_wh,
    battery_wh / NULLIF(
        (
            messages_per_day *
            (
                sensing_energy_wh +
                processing_energy_wh +
                transmit_energy_wh * retries +
                receive_energy_wh * retries
            )
            + sleep_energy_wh_per_day
        ), 0
    ) AS estimated_battery_life_days,
    sense_latency_s + queue_latency_s + tx_latency_s + backhaul_latency_s + process_latency_s + notify_latency_s
        AS alert_latency_s
FROM disaster_iot_scenarios;
