library ieee;
use ieee.std_logic_1164.all;

entity peripheral_control_gate is
    port (
        enable_request : in std_logic;
        owner_valid : in std_logic;
        fault_active : in std_logic;
        peripheral_enable : out std_logic
    );
end peripheral_control_gate;

architecture rtl of peripheral_control_gate is
begin
    peripheral_enable <= enable_request when (owner_valid = '1' and fault_active = '0') else '0';
end rtl;
