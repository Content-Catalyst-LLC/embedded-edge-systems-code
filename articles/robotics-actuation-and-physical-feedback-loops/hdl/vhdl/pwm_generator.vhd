library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity pwm_generator is
    generic (
        COUNTER_WIDTH : integer := 16
    );
    port (
        clk        : in  std_logic;
        rst        : in  std_logic;
        duty_cycle : in  unsigned(COUNTER_WIDTH-1 downto 0);
        pwm_out    : out std_logic
    );
end pwm_generator;

architecture Behavioral of pwm_generator is
    signal counter : unsigned(COUNTER_WIDTH-1 downto 0) := (others => '0');
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                counter <= (others => '0');
                pwm_out <= '0';
            else
                counter <= counter + 1;
                if counter < duty_cycle then
                    pwm_out <= '1';
                else
                    pwm_out <= '0';
                end if;
            end if;
        end if;
    end process;
end Behavioral;
