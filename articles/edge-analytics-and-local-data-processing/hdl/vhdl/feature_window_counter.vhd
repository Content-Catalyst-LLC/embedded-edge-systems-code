library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity feature_window_counter is
    generic (
        COUNT_WIDTH : integer := 16;
        WINDOW_SIZE : integer := 512
    );
    port (
        clk          : in  std_logic;
        rst          : in  std_logic;
        sample_valid : in  std_logic;
        window_ready : out std_logic;
        sample_count : out unsigned(COUNT_WIDTH-1 downto 0)
    );
end feature_window_counter;

architecture Behavioral of feature_window_counter is
    signal count_reg : unsigned(COUNT_WIDTH-1 downto 0) := (others => '0');
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                count_reg <= (others => '0');
                window_ready <= '0';
            elsif sample_valid = '1' then
                if count_reg >= to_unsigned(WINDOW_SIZE - 1, COUNT_WIDTH) then
                    count_reg <= (others => '0');
                    window_ready <= '1';
                else
                    count_reg <= count_reg + 1;
                    window_ready <= '0';
                end if;
            else
                window_ready <= '0';
            end if;
        end if;
    end process;

    sample_count <= count_reg;
end Behavioral;
