# Workflow Overview

This companion workflow turns autonomous edge intelligence concepts into executable artifacts.

## Main computational path

1. Load sample autonomy events and configuration manifests.
2. Simulate observations from a partially observable environment.
3. Update belief state over world states such as clear path, obstacle, or hazard.
4. Select candidate actions from a decision policy.
5. Pass candidate actions through a runtime assurance filter.
6. Replace unsafe, unauthorized, stale, or late actions with fallback behavior.
7. Export autonomy events, belief-state records, filtered-action records, and summary reports.
8. Use R to report confidence drift, latency violations, fallback rates, intervention rates, and safety events.
9. Use systems-language examples to show how bounded autonomy appears in embedded code, safe validators, telemetry gateways, and hardware-adjacent accelerators.

## Engineering emphasis

The code is designed around engineering questions:

- What did the system observe?
- What did it believe?
- What action did the policy propose?
- Did runtime assurance allow, modify, reject, or replace that action?
- Was the decision inside the autonomy authority boundary?
- Was the decision inside the latency budget?
- Did confidence or input distribution drift over time?
- Did fallback, human intervention, or safety-state transitions increase?
