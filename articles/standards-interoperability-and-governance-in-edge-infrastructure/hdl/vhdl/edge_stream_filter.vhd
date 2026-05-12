-- VHDL Example: Edge Stream Threshold Filter
--
-- This simple entity represents a hardware-level stream filter that flags
-- values above a configured threshold.

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity edge_stream_filter is
    generic (
        DATA_WIDTH : integer := 16;
        THRESHOLD  : integer := 1000
    );
    port (
        clk       : in  std_logic;
        rst       : in  std_logic;
        valid_in  : in  std_logic;
        data_in   : in  std_logic_vector(DATA_WIDTH-1 downto 0);
        valid_out : out std_logic;
        data_out  : out std_logic_vector(DATA_WIDTH-1 downto 0);
        alert_out : out std_logic
    );
end edge_stream_filter;

architecture Behavioral of edge_stream_filter is
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                valid_out <= '0';
                data_out  <= (others => '0');
                alert_out <= '0';
            else
                valid_out <= valid_in;
                data_out  <= data_in;

                if valid_in = '1' and unsigned(data_in) > to_unsigned(THRESHOLD, DATA_WIDTH) then
                    alert_out <= '1';
                else
                    alert_out <= '0';
                end if;
            end if;
        end if;
    end process;
end Behavioral;
