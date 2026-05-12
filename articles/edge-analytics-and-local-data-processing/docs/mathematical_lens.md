# Mathematical Lens: Windows, Latency, Compression, Freshness, Backlog, and Local Utility

A practical mathematical lens for edge analytics begins with time, reduction, and usefulness.

\[
L_{\mathrm{local}} = L_{\mathrm{acquire}} + L_{\mathrm{preprocess}} + L_{\mathrm{window}} + L_{\mathrm{feature}} + L_{\mathrm{event}} + L_{\mathrm{action}}
\]

Total local analytics latency includes acquisition, preprocessing, windowing, feature extraction, event logic, and action.

\[
R_{\mathrm{compress}} = 1 - \frac{\mathrm{bytes}_{\mathrm{uplink}}}{\mathrm{bytes}_{\mathrm{raw}}}
\]

Compression ratio measures how much local processing reduces upstream transport.

\[
F_k = t_{\mathrm{now}} - t_{\mathrm{acquisition},k}
\]

Freshness measures the age of the local data window or derived output.

\[
B_{k+1} = \min(B_{\max}, B_k + \lambda_k - \mu_k)
\]

Buffer backlog grows when local analytical output rate exceeds uplink service rate.

\[
U_{\mathrm{edge}} = w_1 S_{\mathrm{latency}} + w_2 S_{\mathrm{bandwidth}} + w_3 S_{\mathrm{privacy}} + w_4 S_{\mathrm{continuity}} - w_5 C_{\mathrm{opacity}}
\]

Edge utility balances latency, bandwidth, privacy, continuity, and opacity cost.

\[
Q_{\mathrm{analytics}} = 1 - \left(\alpha M + \beta S + \gamma E + \delta L\right)
\]

Analytics quality can penalize missing inputs, stale outputs, event errors, and lineage gaps.
