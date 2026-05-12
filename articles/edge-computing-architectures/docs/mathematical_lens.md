# Mathematical Lens

\[
P^\*(w_i)=\arg\min_{l_j}C(w_i,l_j)
\]

The preferred placement is the layer that minimizes total architectural cost.

\[
C(w_i,l_j)=\alpha L_{ij}+\beta B_{ij}+\gamma S_{ij}+\delta M_{ij}+\eta R_{ij}-\kappa A_{ij}
\]

Placement cost combines latency, bandwidth, security exposure, management burden, resilience risk, and autonomy benefit.

\[
L_{\mathrm{path}}=L_{\mathrm{sense}}+L_{\mathrm{compute}}+L_{\mathrm{network}}+L_{\mathrm{queue}}+L_{\mathrm{act}}
\]

End-to-end latency includes sensing, compute, transport, queueing, and action.

\[
R_{\mathrm{uplink}}=1-\frac{D_{\mathrm{forwarded}}}{D_{\mathrm{raw}}}
\]

Uplink reduction measures how much raw data volume is reduced by local filtering, summarization, buffering, or inference.

\[
O_{\mathrm{offline}}=\frac{F_{\mathrm{available\ offline}}}{F_{\mathrm{required\ during\ outage}}}
\]

Offline operability measures how much required functionality remains available during disconnection.

\[
Q_{\mathrm{edge}}=w_1S_{\mathrm{latency}}+w_2S_{\mathrm{bandwidth}}+w_3S_{\mathrm{continuity}}+w_4S_{\mathrm{privacy}}+w_5S_{\mathrm{trust}}+w_6S_{\mathrm{assurance}}-w_7C_{\mathrm{management}}
\]
