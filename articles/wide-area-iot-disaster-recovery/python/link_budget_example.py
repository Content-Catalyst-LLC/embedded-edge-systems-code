#!/usr/bin/env python3
"""
Simplified link-budget example for wide-area IoT planning.

This is an educational model only. Production radio planning requires measured terrain,
antenna patterns, interference analysis, local regulations, and field testing.
"""

from dataclasses import dataclass

@dataclass
class LinkBudget:
    transmit_power_dbm: float
    tx_antenna_gain_dbi: float
    rx_antenna_gain_dbi: float
    path_loss_db: float
    other_losses_db: float
    receiver_sensitivity_dbm: float

    def received_power_dbm(self) -> float:
        return (
            self.transmit_power_dbm
            + self.tx_antenna_gain_dbi
            + self.rx_antenna_gain_dbi
            - self.path_loss_db
            - self.other_losses_db
        )

    def link_margin_db(self) -> float:
        return self.received_power_dbm() - self.receiver_sensitivity_dbm

    def likely_received(self) -> bool:
        return self.received_power_dbm() >= self.receiver_sensitivity_dbm

example = LinkBudget(
    transmit_power_dbm=14,
    tx_antenna_gain_dbi=2,
    rx_antenna_gain_dbi=6,
    path_loss_db=128,
    other_losses_db=8,
    receiver_sensitivity_dbm=-137,
)

print("Received power:", round(example.received_power_dbm(), 2), "dBm")
print("Link margin:", round(example.link_margin_db(), 2), "dB")
print("Likely received:", example.likely_received())
