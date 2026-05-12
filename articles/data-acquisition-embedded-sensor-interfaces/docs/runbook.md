# Runbook

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./acquisition_quality_monitor
cd ../cpp && make && ./acquisition_state_machine
cd ../rust && cargo run
cd ../go && go run acquisition_event_router.go
```
