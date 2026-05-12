# Mathematical Lens

Environmental sensor networks can be modeled as distributed measurement systems.

\[
s_i(t) = E(x_i,y_i,t) + b_i(t) + \epsilon_i(t)
\]

A node-level measurement reflects the environmental condition at the node location plus bias and contextual error.

\[
T_i \approx \frac{B_i}{P_i}
\]

Expected node lifetime depends on available energy and average power consumption.

\[
C_i = \frac{M_i^{\mathrm{valid}}}{M_i^{\mathrm{expected}}}
\]

Data completeness should count valid measurements, not merely received packets.

\[
Q_{\mathrm{network}}(t) = \frac{\sum_{i=1}^{N} w_i q_i(t)}{\sum_{i=1}^{N} w_i}
\]

Network quality can be summarized as a weighted quality state across nodes, where weights may reflect site importance, parameter sensitivity, or decision relevance.
