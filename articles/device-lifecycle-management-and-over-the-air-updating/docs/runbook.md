# Runbook

From this article directory:

```bash
python python/ota_fleet_readiness_scoring.py
Rscript r/lifecycle_compliance_reporting.R
```

Optional systems examples:

```bash
cd c && make && ./update_slot_manager
cd ../cpp && make && ./staged_rollout_planner
cd ../rust && cargo run
cd ../go && go run ota_deployment_status_service.go
```
