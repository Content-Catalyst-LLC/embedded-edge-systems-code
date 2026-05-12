library ieee;
use ieee.std_logic_1164.all;

entity peripheral_enable_gate is
    port (
        enable_request : in std_logic;
        low_energy_mode : in std_logic;
        brownout_protect : in std_logic;
        peripheral_enable : out std_logic
    );
end peripheral_enable_gate;

architecture rtl of peripheral_enable_gate is
begin
    peripheral_enable <= enable_request when (low_energy_mode = '0' and brownout_protect = '0') else '0';
end rtl;
