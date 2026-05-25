# Method Notes

This scaffold uses simplified models for early-stage disaster IoT planning.

## Link budget

\[
P_r = P_t + G_t + G_r - L_p - L_o
\]

A message is likely to be received when:

\[
P_r \geq S_r
\]

## Daily energy budget

\[
E_{day} = N_m(E_s + E_p + E_t + E_r) + E_{sleep}
\]

## Battery life

\[
L = \frac{B}{E_{day}}
\]

## Message delivery probability

\[
P_{deliver} = 1 - (1 - p)^k
\]

## Alert latency

\[
T_{alert} = T_{sense} + T_{queue} + T_{tx} + T_{backhaul} + T_{process} + T_{notify}
\]

## Expected value of warning

\[
EV = P_h \cdot P_d \cdot A_l - C_s
\]

These formulas are simplified for teaching. Operational deployment requires radio planning, device datasheets, terrain studies, gateway testing, spectrum review, cybersecurity review, community governance, emergency-management integration, and field drills.
