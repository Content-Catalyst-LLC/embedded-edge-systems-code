# Mathematical Lens

\[
r_i = F(m_i, d_i, \tau_i, q_i, s_i, v_i, p_i)
\]

A usable IoT record depends not only on the measurement \(m_i\), but also on device identity \(d_i\), timestamp semantics \(\tau_i\), quality state \(q_i\), trust state \(s_i\), version state \(v_i\), and transport provenance \(p_i\).

\[
L_{\mathrm{e2e}} = L_{\mathrm{sense}} + L_{\mathrm{queue}} + L_{\mathrm{network}} + L_{\mathrm{gateway}} + L_{\mathrm{ingest}} + L_{\mathrm{process}}
\]

End-to-end latency includes sensing, local queueing, network transport, gateway handling, platform ingestion, and processing.

\[
F_{\mathrm{fresh}} = t_{\mathrm{now}} - t_{\mathrm{event}}
\]

Freshness is the age of the measurement relative to event time.

\[
R_{\mathrm{delivery}} = \frac{N_{\mathrm{delivered}}}{N_{\mathrm{expected}}}
\]

Delivery reliability compares delivered records to expected records.

\[
Q_{\mathrm{usable}} = \frac{N_{\mathrm{valid, fresh, trusted}}}{N_{\mathrm{received}}}
\]

Usable telemetry rate measures the share of received records that are valid, fresh, and trusted enough for their intended use.

\[
B_{\mathrm{pressure}} = \frac{Q_{\mathrm{current}}}{Q_{\mathrm{capacity}}}
\]

Buffer pressure compares current queue depth to buffer capacity.

\[
G_{\mathrm{fleet}} = w_1 A_{\mathrm{fleet}} + w_2 Q_{\mathrm{usable}} + w_3 T_{\mathrm{verified}} + w_4 V_{\mathrm{compliant}} + w_5 O_{\mathrm{observable}} + w_6 C_{\mathrm{bounded}}
\]

Fleet governability can combine availability, usable telemetry, verified trust, version compliance, observability coverage, and bounded command authority.
