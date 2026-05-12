# Runbook

From this article directory:

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./embedded_pid_controller
cd ../cpp && make && ./supervisory_control_state_machine
cd ../rust && cargo run
cd ../go && go run control_event_gateway.go
```

Python workflows can also be run directly:

```bash
python3 python/embedded_control_simulation.py
python3 python/dc_motor_speed_control.py
python3 python/timing_budget_analysis.py
```
