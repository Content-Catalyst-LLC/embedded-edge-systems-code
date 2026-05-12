# Mathematical Lens: Latency, Memory, Quantization, Confidence, Backend Parity, and Drift

A practical mathematical lens for edge AI begins with deployability. A model is useful only if it fits the device and behaves acceptably under the actual runtime path.

\[
L_{\mathrm{total}} = L_{\mathrm{sense}} + L_{\mathrm{feature}} + L_{\mathrm{infer}} + L_{\mathrm{post}} + L_{\mathrm{action}}
\]

Total local latency includes sensing, feature extraction, inference, post-processing, and action.

\[
M_{\mathrm{total}} = M_{\mathrm{model}} + M_{\mathrm{runtime}} + M_{\mathrm{tensor}} + M_{\mathrm{firmware}} + M_{\mathrm{buffer}}
\]

Total memory demand includes the model, runtime, tensor arena, firmware, and buffers.

\[
\epsilon_q = \left| \mathrm{Metric}(f_{\theta}) - \mathrm{Metric}(Q(f_{\theta})) \right|
\]

Quantization error measures the performance difference between the original model and quantized model.

\[
\Delta_{\mathrm{backend}} = \left| f_{\mathrm{ref}}(z_t) - f_{\mathrm{target}}(z_t) \right|
\]

Backend deviation measures numerical difference between reference output and target-runtime output.

\[
a_t =
\begin{cases}
\mathrm{act}(\hat{y}_t), & c_t \geq \tau \ \mathrm{and}\ h_t = \mathrm{healthy} \\
\mathrm{fallback}, & c_t < \tau \ \mathrm{or}\ h_t \neq \mathrm{healthy}
\end{cases}
\]

Local action should depend on confidence threshold and device health, not only predicted class.

\[
D_t = d(P_{\mathrm{train}}(z), P_{\mathrm{field},t}(z))
\]

Drift proxy measures how field features differ from the training feature distribution.
