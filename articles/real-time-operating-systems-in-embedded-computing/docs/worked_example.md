# Worked Example: Deadline Miss Under Radio Burst Load

A field node misses a sensor-processing deadline only when radio traffic spikes.

The engineering review checks:

- task period, deadline, WCET, and priority
- radio task priority and burst behavior
- ISR duration and deferred-work queue depth
- mutexes shared between sensor and radio tasks
- queue high-water marks
- stack watermarks
- timer wakeups and idle residency
- watchdog progress evidence
- firmware version and runtime trace records

The problem is not simply that the device is "too slow." It may be a priority assignment problem, queue pressure problem, excessive ISR work, priority inversion, or a blocking call in a timing-critical path.
