# Mathematical Lens

Low-power design is governed by average behavior, not a single current value.

\[
I_{\mathrm{avg}} = dI_a + (1-d)I_s + I_q
\]

Average current combines active current, sleep current, duty cycle, and quiescent current from regulators or always-on board elements.

\[
E_{\mathrm{comm}} = n_{\mathrm{tx}}E_{\mathrm{tx}} + n_{\mathrm{rx}}E_{\mathrm{rx}} + n_{\mathrm{retry}}E_{\mathrm{retry}}
\]

Communication energy includes transmissions, receive windows, and retries.

\[
T_{\mathrm{life}} \approx \frac{\eta B}{P_{\mathrm{avg}}}
\]

Lifetime depends on usable energy, derating, and measured average power.

\[
E_{\mathrm{event}} = E_{\mathrm{wake}} + E_{\mathrm{sense}} + E_{\mathrm{compute}} + E_{\mathrm{store}} + E_{\mathrm{comm}} + E_{\mathrm{return}}
\]

Event energy captures the full wake-to-sleep path.

\[
U = \frac{N_{\mathrm{valid}}}{E_{\mathrm{total}}}
\]

Energy utility measures valid useful outputs per unit energy.
