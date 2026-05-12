# Runbook

From this article directory:

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./measurement_quality_flags
cd ../cpp && make && ./measurement_state_machine
cd ../rust && cargo run
cd ../go && go run measurement_event_router.go
```
