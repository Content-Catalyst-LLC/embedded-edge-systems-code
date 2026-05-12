# Mathematical Lens

Firmware architecture can be evaluated through latency, state coverage, abstraction overhead, and diagnostic coverage.

\[
L_{\mathrm{path}} = L_{\mathrm{api}} + L_{\mathrm{driver}} + L_{\mathrm{bus}} + L_{\mathrm{device}} + L_{\mathrm{isr}}
\]

Control-path latency includes API overhead, driver logic, bus transaction time, device response, and interrupt latency.

\[
O_{\mathrm{abs}} = \frac{L_{\mathrm{abstracted}} - L_{\mathrm{direct}}}{L_{\mathrm{direct}}}
\]

Abstraction overhead compares abstracted access with direct hardware access.

\[
C_{\mathrm{state}} = \frac{N_{\mathrm{tested\ states}}}{N_{\mathrm{required\ states}}}
\]

State coverage measures whether required lifecycle states are tested.

\[
C_{\mathrm{detect}} = \frac{D_{\mathrm{err}}}{D_{\mathrm{total}}}
\]

Detection coverage estimates how many injected or observed control faults are detected by diagnostics, assertions, timeouts, or telemetry.

\[
R_{\mathrm{port}} = \frac{N_{\mathrm{portable\ modules}}}{N_{\mathrm{total\ modules}}}
\]

Portability ratio measures how much of the codebase can move across hardware variants without direct modification.
