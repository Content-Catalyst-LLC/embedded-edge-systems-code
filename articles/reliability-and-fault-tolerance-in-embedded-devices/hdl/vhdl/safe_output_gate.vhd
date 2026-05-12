library ieee;
use ieee.std_logic_1164.all;

entity safe_output_gate is
    port (
        command_in : in std_logic;
        fault_active : in std_logic;
        safe_output : out std_logic
    );
end safe_output_gate;

architecture rtl of safe_output_gate is
begin
    safe_output <= '0' when fault_active = '1' else command_in;
end rtl;
