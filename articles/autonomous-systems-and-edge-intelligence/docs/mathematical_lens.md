# Mathematical Lens: Belief-State Decision-Making, Safety Filtering, and Edge Authority

A simplified autonomous edge decision system can be modeled as a partially observable decision process.

\[
x_{k+1} = f(x_k, u_k, w_k)
\]

\[
z_k = h(x_k, v_k)
\]

\[
b_k = P(x_k \mid z_{1:k}, u_{1:k-1})
\]

A policy proposes a candidate action:

\[
u_k^\star = \pi(b_k, g_k, c_k)
\]

Runtime assurance filters that candidate action before execution:

\[
u_k = F(u_k^\star, b_k, \mathcal{S}, \mathcal{A})
\]

The executed action must remain inside a safe and authorized action set:

\[
h(x_k) \geq 0,\qquad u_k \in \mathcal{U}_{\mathrm{allowed}}(a_k)
\]

The companion code implements a simplified version of this stack using belief updates, decision policies, runtime assurance, latency checks, fallback actions, and drift monitoring.
