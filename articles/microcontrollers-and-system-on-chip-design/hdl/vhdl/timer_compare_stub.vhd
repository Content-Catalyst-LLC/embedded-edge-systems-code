library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity timer_compare_stub is
    port (
        clk : in std_logic;
        rst : in std_logic;
        compare_value : in unsigned(31 downto 0);
        match_event : out std_logic
    );
end timer_compare_stub;

architecture rtl of timer_compare_stub is
    signal counter : unsigned(31 downto 0) := (others => '0');
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                counter <= (others => '0');
                match_event <= '0';
            else
                counter <= counter + 1;
                if counter = compare_value then
                    match_event <= '1';
                else
                    match_event <= '0';
                end if;
            end if;
        end if;
    end process;
end rtl;
