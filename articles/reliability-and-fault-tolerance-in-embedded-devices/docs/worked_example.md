# Worked Example: Repeated Watchdog Reset in a Remote Gateway

A remote gateway periodically disappears from telemetry and later returns to service. The dashboard shows eventual recovery, but the diagnostic log shows repeated watchdog resets after communication queue growth.

The engineering review checks:

- reset cause
- watchdog servicing criteria
- queue occupancy
- communication timeout rate
- degraded-mode entries
- persistent-state integrity after reboot
- firmware version
- repeated-reset escalation rule

The issue is not simply that the watchdog worked. Repeated recovery is evidence of an unresolved dependability problem.
