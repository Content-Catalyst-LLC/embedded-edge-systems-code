# Mathematical Lens: Discrete-Time Feedback, Saturation, Safety Filtering, and Timing

A simplified embedded control system can be represented in discrete time as:

\[
x_{k+1} = Ax_k + Bu_k + w_k
\]

\[
y_k = Cx_k + v_k
\]

where \(x_k\) is the plant state, \(u_k\) is the control input, \(y_k\) is the measured output, \(w_k\) is process disturbance, and \(v_k\) is measurement noise.

A PID-style candidate command can be written as:

\[
u_k^\star = K_p e_k + K_i \sum_{j=0}^{k} e_j \Delta t + K_d \frac{e_k - e_{k-1}}{\Delta t}
\]

with:

\[
e_k = r_k - y_k
\]

The candidate command must be filtered before actuation:

\[
u_k = F(u_k^\star, \hat{x}_k, \mathcal{S}, \mathcal{A})
\]

Timing validity can be expressed as:

\[
T_{\mathrm{loop}} + J_{\max} \leq T_{\mathrm{deadline}}
\]

The companion code makes these ideas executable through plant simulation, PID control, command filtering, saturation, anti-windup, timing-budget analysis, and control-loop reporting.
