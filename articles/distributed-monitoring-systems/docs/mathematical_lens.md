# Mathematical Lens

\[
y_i(t) = h_i(x(s_i,t)) + n_i(t) + b_i(t)
\]

Node \(i\) observes the condition at location \(s_i\) through measurement function \(h_i\), noise \(n_i(t)\), and bias or drift \(b_i(t)\).

\[
\hat{x}(s,t) = F(y_1,\ldots,y_N,\tau_1,\ldots,\tau_N,q_1,\ldots,q_N)
\]

A system-level estimate depends on node measurements, timestamp states, and quality states.

\[
F_{\mathrm{fresh},i} = t_{\mathrm{now}} - t_{\mathrm{event},i}
\]

Freshness is measured from event time, not arrival time.

\[
\Delta t_{ij} = |t_i - t_j|
\]

Cross-node temporal skew determines whether measurements can be compared as representing the same event or time window.

\[
C_{\mathrm{coverage}} = \frac{A_{\mathrm{observed}}}{A_{\mathrm{required}}}
\]

Coverage completeness compares observed monitoring field to required monitoring field.

\[
Q_{\mathrm{usable}} = \frac{N_{\mathrm{valid, fresh, synchronized}}}{N_{\mathrm{received}}}
\]

Usable monitoring rate measures the share of received records that are valid, fresh, and synchronized enough for the intended monitoring purpose.

\[
M_{\mathrm{health}} = w_1 C_{\mathrm{coverage}} + w_2 Q_{\mathrm{usable}} + w_3 R_{\mathrm{delivery}} + w_4 S_{\mathrm{sync}} + w_5 H_{\mathrm{gateway}} + w_6 O_{\mathrm{observable}}
\]

Monitoring health can combine coverage, usable telemetry, delivery, synchronization, gateway health, and observability coverage.
