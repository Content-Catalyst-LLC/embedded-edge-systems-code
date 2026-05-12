library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity adc_sampler is
    generic (
        SAMPLE_WIDTH : integer := 12
    );
    port (
        clk          : in  std_logic;
        rst          : in  std_logic;
        sample_valid : in  std_logic;
        adc_data     : in  std_logic_vector(SAMPLE_WIDTH-1 downto 0);
        sample_out   : out std_logic_vector(SAMPLE_WIDTH-1 downto 0);
        sample_ready : out std_logic
    );
end adc_sampler;

architecture Behavioral of adc_sampler is
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                sample_out <= (others => '0');
                sample_ready <= '0';
            else
                if sample_valid = '1' then
                    sample_out <= adc_data;
                    sample_ready <= '1';
                else
                    sample_ready <= '0';
                end if;
            end if;
        end if;
    end process;
end Behavioral;
