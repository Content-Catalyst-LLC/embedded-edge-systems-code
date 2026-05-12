library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity watchdog_heartbeat is
    generic (COUNTER_WIDTH : integer := 32; HEARTBEAT_PERIOD : integer := 1000000);
    port (clk : in std_logic; rst : in std_logic; heartbeat : out std_logic);
end watchdog_heartbeat;

architecture Behavioral of watchdog_heartbeat is
    signal counter : unsigned(COUNTER_WIDTH-1 downto 0) := (others => '0');
    signal hb : std_logic := '0';
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                counter <= (others => '0'); hb <= '0';
            elsif counter >= to_unsigned(HEARTBEAT_PERIOD, COUNTER_WIDTH) then
                counter <= (others => '0'); hb <= not hb;
            else
                counter <= counter + 1;
            end if;
        end if;
    end process;
    heartbeat <= hb;
end Behavioral;
