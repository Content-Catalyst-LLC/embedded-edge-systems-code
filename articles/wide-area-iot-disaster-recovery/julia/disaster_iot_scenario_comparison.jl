# Wide-area IoT disaster recovery scenario comparison in Julia.
# Synthetic demonstration only.

using CSV
using DataFrames

root = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(root, "data", "raw", "disaster_iot_scenarios_synthetic.csv")
out_path = joinpath(root, "outputs", "tables", "disaster_iot_scenario_summary_julia.csv")

df = CSV.read(data_path, DataFrame)

df.energy_per_message_wh =
    df.sensing_energy_wh .+
    df.processing_energy_wh .+
    df.transmit_energy_wh .* df.retries .+
    df.receive_energy_wh .* df.retries

df.daily_energy_wh =
    df.messages_per_day .* df.energy_per_message_wh .+
    df.sleep_energy_wh_per_day

df.estimated_battery_life_days =
    df.battery_wh ./ df.daily_energy_wh

df.delivery_probability =
    1 .- (1 .- df.single_attempt_success) .^ df.retries

df.alert_latency_s =
    df.sense_latency_s .+
    df.queue_latency_s .+
    df.tx_latency_s .+
    df.backhaul_latency_s .+
    df.process_latency_s .+
    df.notify_latency_s

mkpath(dirname(out_path))
CSV.write(out_path, df)

println(df[:, [
    :scenario_id,
    :protocol,
    :hazard_context,
    :daily_energy_wh,
    :estimated_battery_life_days,
    :delivery_probability,
    :alert_latency_s
]])
