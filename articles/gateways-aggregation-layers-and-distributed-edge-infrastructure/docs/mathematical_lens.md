# Mathematical Lens: Aggregation, Freshness, Buffer Risk, and Gateway Load

Gateway and aggregation layers become engineering-grade when their quality is measurable.

\[
s_t = A(z_{1:n,t}, h_{1:n,t}, q_{1:n,t}, \ell_{1:n,t})
\]

Site state \(s_t\) is produced by aggregation function \(A\) using device observations \(z\), health indicators \(h\), quality indicators \(q\), and lineage records \(\ell\).

\[
F_i(t) = t_{\mathrm{now}} - t_{\mathrm{acquisition},i}
\]

Freshness \(F_i(t)\) measures the age of device \(i\)'s latest valid measurement.

\[
B_{t+1} = \min(B_{\max}, B_t + \lambda_t - \mu_t)
\]

Buffer backlog \(B_t\) grows when local event arrival rate \(\lambda_t\) exceeds uplink service rate \(\mu_t\).

\[
\rho = \frac{\lambda}{\mu}
\]

Gateway utilization \(\rho\) compares incoming workload with service capacity.

\[
C_{\mathrm{loss}} = w_1 D_{\mathrm{drop}} + w_2 A_{\mathrm{stale}} + w_3 E_{\mathrm{lineage}} + w_4 R_{\mathrm{replay}}
\]

Context-loss cost combines dropped data, stale aggregation, lineage error, and replay risk.

\[
Q_{\mathrm{site}} = 1 - \left(\alpha M + \beta S + \gamma E + \delta L\right)
\]

A simple site-quality score penalizes missing devices \(M\), stale inputs \(S\), protocol errors \(E\), and lineage gaps \(L\).
