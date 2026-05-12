# Runbook

From this article directory:

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./pid_control_loop
cd ../cpp && make && ./robot_state_machine
cd ../rust && cargo run
cd ../go && go run robot_telemetry_gateway.go
```

Python workflows can also be run directly:

```bash
python3 python/state_space_feedback_simulation.py
python3 python/kalman_state_estimation.py
python3 python/safety_envelope_validator.py
```
