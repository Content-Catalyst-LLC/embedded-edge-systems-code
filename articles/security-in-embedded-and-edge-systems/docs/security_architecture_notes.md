# Security Architecture Notes

A useful embedded and edge security architecture should make the following explicit:

1. What establishes the first trusted execution state?
2. Where are device identity and keys stored?
3. How are firmware and boot stages validated?
4. How are updates authenticated and recovered?
5. Which communications boundaries require mutual authentication?
6. Which runtime services have access to keys, sensors, actuators, storage, and networks?
7. Which security events are logged and where are logs protected?
8. How are unsupported devices identified and retired?
9. How are TinyML models, PYNQ overlays, FPGA bitstreams, and HDL modules versioned and validated?
10. What happens when trust evidence is missing or invalid?
