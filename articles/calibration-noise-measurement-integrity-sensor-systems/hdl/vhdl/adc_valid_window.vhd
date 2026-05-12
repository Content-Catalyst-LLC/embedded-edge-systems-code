library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity adc_valid_window is
    generic (SETTLING_CYCLES : integer := 50);
    port (
        clk : in std_logic;
        rst : in std_logic;
        channel_switched : in std_logic;
        sample_valid : out std_logic
    );
end adc_valid_window;

architecture Behavioral of adc_valid_window is
    signal counter : unsigned(15 downto 0) := (others => '0');
    signal valid_reg : std_logic := '0';
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' or channel_switched = '1' then
                counter <= (others => '0');
                valid_reg <= '0';
            elsif counter >= to_unsigned(SETTLING_CYCLES, 16) then
                valid_reg <= '1';
            else
                counter <= counter + 1;
                valid_reg <= '0';
            end if;
        end if;
    end process;

    sample_valid <= valid_reg;
end Behavioral;
