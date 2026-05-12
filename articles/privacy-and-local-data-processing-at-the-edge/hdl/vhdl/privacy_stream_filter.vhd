library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity privacy_stream_filter is
    generic (
        DATA_WIDTH : integer := 16;
        THRESHOLD  : integer := 1000
    );
    port (
        clk         : in  std_logic;
        rst         : in  std_logic;
        valid_in    : in  std_logic;
        raw_data_in : in  std_logic_vector(DATA_WIDTH-1 downto 0);
        valid_out   : out std_logic;
        event_out   : out std_logic
    );
end privacy_stream_filter;

architecture Behavioral of privacy_stream_filter is
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                valid_out <= '0';
                event_out <= '0';
            else
                valid_out <= valid_in;
                if valid_in = '1' and unsigned(raw_data_in) > to_unsigned(THRESHOLD, DATA_WIDTH) then
                    event_out <= '1';
                else
                    event_out <= '0';
                end if;
            end if;
        end if;
    end process;
end Behavioral;
