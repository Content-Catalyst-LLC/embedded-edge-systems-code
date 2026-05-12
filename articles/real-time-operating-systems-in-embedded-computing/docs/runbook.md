# Runbook

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./rtos_task_contract
cd ../cpp && make && ./fixed_priority_scheduler
cd ../rust && cargo run
cd ../go && go run rtos_telemetry_aggregator.go
```
