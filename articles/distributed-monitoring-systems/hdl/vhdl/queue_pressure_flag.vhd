library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity queue_pressure_flag is
    generic (WIDTH : integer := 16; THRESHOLD : integer := 800);
    port (
        queue_depth : in unsigned(WIDTH-1 downto 0);
        queue_pressure : out std_logic
    );
end queue_pressure_flag;

architecture Behavioral of queue_pressure_flag is
begin
    queue_pressure <= '1' when queue_depth >= to_unsigned(THRESHOLD, WIDTH) else '0';
end Behavioral;
