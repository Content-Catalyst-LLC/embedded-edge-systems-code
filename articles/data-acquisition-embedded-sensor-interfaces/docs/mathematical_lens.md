# Mathematical Lens

The acquisition chain can be modeled as a sequence from physical signal to digital record.

\[
v(t) = g(s(t)) + n_s(t)
\]

The transducer converts physical signal \(s(t)\) into an electrical or internal sensor-domain signal \(v(t)\).

\[
u(t) = h(v(t)) + n_a(t)
\]

The analog front end or sensor-internal conditioning path shapes the signal.

\[
x_k = q(u(t_k))
\]

The ADC or digital conversion path samples the conditioned signal at acquisition time \(t_k\).

\[
m_k = \{x_k, t_k, c, r, \gamma, Q_k\}
\]

A trustworthy measurement record includes value, acquisition time, channel identity, reference/scaling state, calibration version, and quality flags.
