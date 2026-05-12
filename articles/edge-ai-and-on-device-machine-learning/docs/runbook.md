# Runbook

From this article directory:

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./edge_ai_feature_inference
cd ../cpp && make && ./edge_ai_runtime_state_machine
cd ../rust && cargo run
cd ../go && go run inference_event_router.go
```

Python workflows can also be run directly:

```bash
python3 python/edge_ai_model_budget_quantization_simulation.py
python3 python/runtime_backend_validation.py
python3 python/confidence_fallback_decision_simulation.py
python3 python/fleet_drift_version_monitoring.py
python3 python/deployment_readiness_gate.py
```
