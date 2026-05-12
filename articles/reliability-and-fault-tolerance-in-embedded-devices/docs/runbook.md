# Runbook

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./watchdog_health_policy
cd ../cpp && make && ./reliability_state_machine
cd ../rust && cargo run
cd ../go && go run fleet_reliability_aggregator.go
```
