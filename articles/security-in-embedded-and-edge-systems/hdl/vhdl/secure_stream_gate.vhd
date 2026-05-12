library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity secure_stream_gate is
    generic (
        DATA_WIDTH : integer := 16
    );
    port (
        clk         : in  std_logic;
        rst         : in  std_logic;
        trust_valid : in  std_logic;
        valid_in    : in  std_logic;
        data_in     : in  std_logic_vector(DATA_WIDTH-1 downto 0);
        valid_out   : out std_logic;
        data_out    : out std_logic_vector(DATA_WIDTH-1 downto 0)
    );
end secure_stream_gate;

architecture Behavioral of secure_stream_gate is
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                valid_out <= '0';
                data_out <= (others => '0');
            else
                valid_out <= valid_in and trust_valid;

                if trust_valid = '1' then
                    data_out <= data_in;
                else
                    data_out <= (others => '0');
                end if;
            end if;
        end if;
    end process;
end Behavioral;
