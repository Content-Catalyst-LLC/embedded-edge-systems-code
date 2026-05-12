# Mathematical Lens

RTOS design can be evaluated through utilization, response time, blocking, jitter, queue pressure, and slack margin.

\[
U = \sum_{i=1}^{n} \frac{C_i}{T_i}
\]

Utilization estimates the processor capacity consumed by periodic tasks.

\[
R_i = C_i + B_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i}{T_j} \right\rceil C_j
\]

Fixed-priority response-time analysis includes task execution, blocking from lower-priority resource holders, and interference from higher-priority tasks.

\[
J_i = \max(t_{i,k+1} - t_{i,k}) - \min(t_{i,k+1} - t_{i,k})
\]

Jitter measures variation between activations or completions.

\[
S_{\mathrm{margin}} = D_i - R_i
\]

Slack margin measures remaining timing reserve before a task misses its deadline.

\[
Q_{\mathrm{depth}}(t+1) = Q_{\mathrm{depth}}(t) + A(t) - S(t)
\]

Queue depth grows when arrivals exceed service. A queue is not a cure for overload; it is evidence of producer/consumer pressure.
