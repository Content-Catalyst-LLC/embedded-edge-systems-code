# Runbook

From this article directory:

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./bounded_autonomy_controller
cd ../cpp && make && ./autonomy_state_machine
cd ../rust && cargo run
cd ../go && go run autonomy_event_gateway.go
```

Python workflows can also be run directly:

```bash
python3 python/autonomous_edge_decision_simulation.py
python3 python/runtime_assurance_filter.py
python3 python/autonomy_drift_monitoring.py
```
