# Runbook

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./edge_watchdog_offline_state
cd ../cpp && make && ./edge_runtime_state_machine
cd ../rust && cargo run
cd ../go && go run edge_fleet_event_router.go
```
