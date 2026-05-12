library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity interrupt_counter is
    port (
        clk : in std_logic;
        rst : in std_logic;
        interrupt_event : in std_logic;
        interrupt_count : out unsigned(31 downto 0)
    );
end interrupt_counter;

architecture rtl of interrupt_counter is
    signal count_reg : unsigned(31 downto 0) := (others => '0');
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                count_reg <= (others => '0');
            elsif interrupt_event = '1' then
                count_reg <= count_reg + 1;
            end if;
        end if;
    end process;

    interrupt_count <= count_reg;
end rtl;
