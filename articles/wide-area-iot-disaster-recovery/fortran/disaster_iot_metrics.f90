program disaster_iot_metrics
  implicit none

  integer :: messages_per_day, retries
  real :: sensing_energy_wh, processing_energy_wh, transmit_energy_wh
  real :: receive_energy_wh, sleep_energy_wh_per_day
  real :: energy_per_message, daily_energy, battery_wh, battery_life
  real :: single_attempt_success, delivery_probability

  messages_per_day = 24
  retries = 2
  sensing_energy_wh = 0.001
  processing_energy_wh = 0.0005
  transmit_energy_wh = 0.003
  receive_energy_wh = 0.001
  sleep_energy_wh_per_day = 0.02
  battery_wh = 20.0
  single_attempt_success = 0.80

  energy_per_message = sensing_energy_wh + processing_energy_wh + &
       transmit_energy_wh * retries + receive_energy_wh * retries

  daily_energy = messages_per_day * energy_per_message + sleep_energy_wh_per_day
  battery_life = battery_wh / daily_energy
  delivery_probability = 1.0 - (1.0 - single_attempt_success) ** retries

  print *, "Daily energy use:", daily_energy, "Wh/day"
  print *, "Battery life:", battery_life, "days"
  print *, "Delivery probability:", delivery_probability * 100.0, "%"
end program disaster_iot_metrics
