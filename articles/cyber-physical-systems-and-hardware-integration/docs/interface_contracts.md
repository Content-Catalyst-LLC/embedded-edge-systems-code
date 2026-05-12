# Interface Contracts

A CPS interface contract defines the physical, temporal, electrical, semantic, and safety meaning of an interface.

Important contract fields include:

- signal name
- physical unit
- valid range
- sampling period
- maximum sample age
- timestamp rule
- calibration state
- failure behavior
- safety semantics
- evidence record

For example, a motor speed signal should not be treated as a generic number. It should have an explicit unit, timestamp, freshness requirement, calibration rule, residual threshold, and failure behavior.

The companion repository includes `config/interface_contracts.yml` and validation scripts that check whether key CPS signals have explicit contract metadata.
