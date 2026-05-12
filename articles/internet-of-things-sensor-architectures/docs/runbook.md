# Runbook

From this article directory:

```bash
bash bash/validate_manifests.sh
bash bash/run_workflows.sh
bash bash/generate_outputs.sh
```

Optional systems examples:

```bash
cd c && make && ./iot_endpoint_queue
cd ../cpp && make && ./iot_device_gateway_state_machine
cd ../rust && cargo run
cd ../go && go run iot_event_router.go
```
