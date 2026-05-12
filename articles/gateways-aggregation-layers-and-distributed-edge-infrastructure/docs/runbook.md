# Runbook

From this article directory:

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./gateway_telemetry_packet
cd ../cpp && make && ./gateway_runtime_state_machine
cd ../rust && cargo run
cd ../go && go run gateway_event_router.go
```

Python workflows can also be run directly:

```bash
python3 python/gateway_buffering_aggregation_simulation.py
python3 python/replay_dedup_validation.py
python3 python/gateway_slo_checks.py
python3 python/protocol_aggregation_quality_analysis.py
```
