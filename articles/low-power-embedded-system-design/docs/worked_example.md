# Worked Example: Remote Sensor Battery Drain

A remote environmental node was expected to run for eighteen months but begins reporting low battery after five months.

The engineering review checks:

- actual sleep residency
- wake count and wake causes
- noisy GPIO or sensor thresholds
- radio retry and reconnect count
- regulator quiescent current
- board-level leakage
- sensor warm-up duration
- brownout counters
- firmware version changes
- solar exposure or battery derating assumptions

The likely problem is not simply battery capacity. It may be a wake storm, link-quality retry loop, regulator/leakage issue, sensor duty-cycle mismatch, or firmware power-management regression.
