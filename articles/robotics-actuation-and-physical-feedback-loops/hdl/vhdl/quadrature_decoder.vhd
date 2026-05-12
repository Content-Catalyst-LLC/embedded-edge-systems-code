library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity quadrature_decoder is
    port (
        clk            : in  std_logic;
        rst            : in  std_logic;
        enc_a          : in  std_logic;
        enc_b          : in  std_logic;
        position_count : out signed(31 downto 0)
    );
end quadrature_decoder;

architecture Behavioral of quadrature_decoder is
    signal previous : std_logic_vector(1 downto 0) := "00";
    signal current  : std_logic_vector(1 downto 0) := "00";
    signal count    : signed(31 downto 0) := (others => '0');
begin
    process(clk)
        variable transition : std_logic_vector(3 downto 0);
    begin
        if rising_edge(clk) then
            if rst = '1' then
                previous <= "00";
                current <= "00";
                count <= (others => '0');
            else
                previous <= current;
                current <= enc_a & enc_b;
                transition := previous & current;

                case transition is
                    when "0001" | "0111" | "1110" | "1000" =>
                        count <= count + 1;
                    when "0010" | "1011" | "1101" | "0100" =>
                        count <= count - 1;
                    when others =>
                        count <= count;
                end case;
            end if;
        end if;
    end process;

    position_count <= count;
end Behavioral;
