# Mathematical Lens

\[
y_{\mathrm{cal}} = a y_{\mathrm{raw}} + b
\]

A linear calibration applies gain \(a\) and offset \(b\) to a raw sensor value.

\[
e = y_{\mathrm{cal}} - y_{\mathrm{ref}}
\]

Calibration error compares calibrated output to a reference.

\[
u_c = \sqrt{\sum_{i=1}^{n}u_i^2}
\]

Combined uncertainty can be approximated as the root-sum-square of independent uncertainty components.

\[
U = k u_c
\]

Expanded uncertainty multiplies combined standard uncertainty by a coverage factor.

\[
\mathrm{SNR}_{\mathrm{dB}} = 20\log_{10}\left(\frac{A_{\mathrm{signal}}}{A_{\mathrm{noise}}}\right)
\]

Signal-to-noise ratio indicates how strongly the signal stands above the noise floor.

\[
D(t) = y_{\mathrm{cal}}(t) - y_{\mathrm{ref}}(t)
\]

Drift compares calibrated value to a reference or baseline over time.

\[
C_{\mathrm{meas}} = w_1 C_{\mathrm{cal}} + w_2 C_{\mathrm{snr}} + w_3 C_{\mathrm{fresh}} + w_4 C_{\mathrm{range}} + w_5 C_{\mathrm{lineage}} + w_6 C_{\mathrm{trace}}
\]

Measurement confidence can combine calibration validity, SNR, freshness, range validity, lineage completeness, and traceability completeness.
