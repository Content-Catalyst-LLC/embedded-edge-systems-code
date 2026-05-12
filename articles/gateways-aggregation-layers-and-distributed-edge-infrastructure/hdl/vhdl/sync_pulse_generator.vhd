library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity sync_pulse_generator is
    generic (
        COUNTER_WIDTH : integer := 32;
        PERIOD_TICKS : integer := 1000000
    );
    port (
        clk        : in  std_logic;
        rst        : in  std_logic;
        sync_pulse : out std_logic
    );
end sync_pulse_generator;

architecture Behavioral of sync_pulse_generator is
    signal counter : unsigned(COUNTER_WIDTH-1 downto 0) := (others => '0');
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                counter <= (others => '0');
                sync_pulse <= '0';
            elsif counter >= to_unsigned(PERIOD_TICKS, COUNTER_WIDTH) then
                counter <= (others => '0');
                sync_pulse <= '1';
            else
                counter <= counter + 1;
                sync_pulse <= '0';
            end if;
        end if;
    end process;
end Behavioral;
