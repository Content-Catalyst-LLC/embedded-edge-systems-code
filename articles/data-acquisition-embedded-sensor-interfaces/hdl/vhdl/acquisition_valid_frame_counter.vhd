library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity acquisition_valid_frame_counter is
    port (
        clk : in std_logic;
        rst : in std_logic;
        sample_valid : in std_logic;
        frame_count : out unsigned(31 downto 0)
    );
end acquisition_valid_frame_counter;

architecture rtl of acquisition_valid_frame_counter is
    signal count_reg : unsigned(31 downto 0) := (others => '0');
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                count_reg <= (others => '0');
            elsif sample_valid = '1' then
                count_reg <= count_reg + 1;
            end if;
        end if;
    end process;
    frame_count <= count_reg;
end rtl;
