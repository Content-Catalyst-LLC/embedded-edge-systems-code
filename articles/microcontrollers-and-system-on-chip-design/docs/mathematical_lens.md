# Mathematical Lens

Microcontroller and SoC selection can be modeled as a multi-constraint platform-fit problem.

\[
F_{\mathrm{platform}} = f(C, M, I, T, P, S, L)
\]

Platform fit depends on compute, memory, I/O, timing, power, security, and lifecycle needs.

\[
U_{\mathrm{cpu}} = \sum_{i=1}^{n} \frac{C_i}{T_i}
\]

CPU utilization estimates how much processing time is consumed by periodic or bounded workloads.

\[
M_{\mathrm{margin}} = M_{\mathrm{available}} - (M_{\mathrm{code}} + M_{\mathrm{stack}} + M_{\mathrm{heap}} + M_{\mathrm{buffers}} + M_{\mathrm{logs}} + M_{\mathrm{update}})
\]

Memory margin must include code, stacks, heap, buffers, logs, and firmware-update space.

\[
B_{\mathrm{margin}} = B_{\mathrm{available}} - B_{\mathrm{required}}
\]

Bandwidth margin captures whether internal buses, memory systems, DMA paths, and external interfaces can support the required workload.

\[
E_{\mathrm{day}} = E_{\mathrm{active}} + E_{\mathrm{sleep}} + E_{\mathrm{wake}} + E_{\mathrm{comm}} + E_{\mathrm{retention}}
\]

Daily energy includes active work, sleep, wake transitions, communication, and retained domains.

\[
R_{\mathrm{fit}} = w_C R_C + w_M R_M + w_I R_I + w_T R_T + w_P R_P + w_S R_S + w_L R_L
\]

A weighted fit score compares candidates across compute, memory, I/O, timing, power, security, and lifecycle dimensions.
