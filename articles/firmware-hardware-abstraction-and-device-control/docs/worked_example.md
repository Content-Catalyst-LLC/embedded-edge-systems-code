# Worked Example: Sensor Driver Resume Failure

A field device wakes from deep sleep and begins reporting stale measurements. The sensor works after cold boot, but fails after repeated suspend/resume cycles.

The engineering review checks:

- driver lifecycle state
- retained state assumptions
- sensor power sequencing
- bus timeout counters
- suspend/resume ordering
- wake-source timing
- firmware version
- board revision
- reset cause and brownout records
- diagnostic evidence after failed resume

The problem is not simply a sensor failure. It may be a driver contract failure: the device is being used after resume before its hardware state, bus state, or calibration state is valid.
