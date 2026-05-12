# Runbook

From this article directory:

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./offline_authority_timer
cd ../cpp && make && ./gateway_sync_state_machine
cd ../rust && cargo run
cd ../go && go run gateway_sync_service.go
```

Python workflows can also be run directly:

```bash
python3 python/cloud_edge_placement_sync_simulation.py
python3 python/rollout_convergence_analysis.py
python3 python/sync_reconciliation_validation.py
python3 python/hybrid_slo_authority_checks.py
```
