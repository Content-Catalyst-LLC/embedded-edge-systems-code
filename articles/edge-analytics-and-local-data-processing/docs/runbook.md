# Runbook

From this article directory:

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./edge_analytics_window_features
cd ../cpp && make && ./edge_analytics_runtime_state_machine
cd ../rust && cargo run
cd ../go && go run analytics_event_router.go
```

Python workflows can also be run directly:

```bash
python3 python/edge_stream_analytics_selective_uplink_simulation.py
python3 python/replay_backfill_integrity_validation.py
python3 python/analytics_slo_checks.py
python3 python/lineage_freshness_feature_quality_analysis.py
python3 python/deployment_readiness_gate.py
```
