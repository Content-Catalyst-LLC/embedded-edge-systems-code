library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity buffer_watermark_monitor is
    generic (
        COUNT_WIDTH : integer := 16;
        HIGH_WATERMARK : integer := 200
    );
    port (
        buffer_count   : in  unsigned(COUNT_WIDTH-1 downto 0);
        high_watermark : out std_logic;
        uplink_pressure: out std_logic
    );
end buffer_watermark_monitor;

architecture Behavioral of buffer_watermark_monitor is
begin
    high_watermark <= '1' when buffer_count >= to_unsigned(HIGH_WATERMARK, COUNT_WIDTH) else '0';
    uplink_pressure <= '1' when buffer_count >= to_unsigned(HIGH_WATERMARK, COUNT_WIDTH) else '0';
end Behavioral;
