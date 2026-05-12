# Mathematical Lens

Reliability and fault tolerance connect failure probability, detection, recovery, and availability.

\[
R(t) = e^{-\lambda t}
\]

Under a simple constant-failure-rate model, reliability decreases over time.

\[
A = \frac{\mathrm{MTBF}}{\mathrm{MTBF} + \mathrm{MTTR}}
\]

Availability improves when failures happen less often or recovery happens faster.

\[
C_{\mathrm{effective}} = C_d \cdot C_r
\]

Effective fault coverage depends on both detection coverage \(C_d\) and recovery coverage \(C_r\).

\[
T_{\mathrm{recovery}} = T_{\mathrm{detect}} + T_{\mathrm{isolate}} + T_{\mathrm{restore}} + T_{\mathrm{validate}}
\]

Recovery time includes detection, isolation, restoration, and validation.
