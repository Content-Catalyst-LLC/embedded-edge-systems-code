# Runbook

From this article directory:

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./cps_firmware_interface
cd ../cpp && make && ./cps_integration_state_machine
cd ../rust && cargo run
cd ../go && go run cps_event_gateway.go
```

Python workflows can also be run directly:

```bash
python3 python/cps_timing_sensing_actuation_simulation.py
python3 python/uncertainty_budget_analysis.py
python3 python/traceability_matrix_validation.py
python3 python/hil_digital_twin_readiness.py
```
