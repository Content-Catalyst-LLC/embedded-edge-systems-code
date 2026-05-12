# Mathematical Lens: State-Space Feedback, Tracking Error, and Safety Constraints

A simplified discrete-time robot control model can be written as:

\[
x_{k+1} = Ax_k + Bu_k + w_k
\]

\[
y_k = Cx_k + v_k
\]

Where:

- \(x_k\): system state
- \(u_k\): control input
- \(y_k\): measured output
- \(A\): system dynamics matrix
- \(B\): input matrix
- \(C\): measurement matrix
- \(w_k\): process disturbance
- \(v_k\): measurement noise

A controller may compute a command using tracking error:

\[
e_k = r_k - y_k
\]

A PID-style control law can be written as:

\[
u_k = K_p e_k + K_i \sum_{j=0}^{k} e_j\Delta t + K_d \frac{e_k - e_{k-1}}{\Delta t}
\]

Robotic safety can be represented through a safe-set constraint:

\[
h(x_k) \geq 0
\]

The companion code makes these ideas executable through simulation, estimator residual analysis, saturation modeling, timing jitter, and safety-envelope validation.
