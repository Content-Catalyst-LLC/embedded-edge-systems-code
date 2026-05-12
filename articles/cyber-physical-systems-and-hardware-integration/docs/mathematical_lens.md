# Mathematical Lens: Coupled Cyber-Physical State, Timing, Uncertainty, and Safe Action

A simplified cyber-physical system separates physical state, sensor observation, estimated state, candidate command, filtered command, and timing validity.

\[
x_{p,k+1} = f_p(x_{p,k}, u_k, w_k)
\]

\[
z_k = h_s(x_{p,k}, v_k)
\]

\[
\hat{x}_{p,k} = E(z_{1:k}, u_{1:k-1})
\]

\[
u_k = F(C(\hat{x}_{p,k}, r_k), \hat{x}_{p,k}, \mathcal{S}, \mathcal{A})
\]

\[
T_{\mathrm{cps}} + J_{\max} \leq T_{\mathrm{deadline}}
\]

\[
\epsilon_{\mathrm{total}} = \epsilon_{\mathrm{sensor}} + \epsilon_{\mathrm{calibration}} + \epsilon_{\mathrm{quantization}} + \epsilon_{\mathrm{estimation}} + \epsilon_{\mathrm{model}}
\]

The companion code implements simplified versions of these structures using a simulated motor-control CPS, sensor noise, calibration error, estimator residuals, command filtering, actuator saturation, uncertainty budgets, timing budgets, and traceability checks.
