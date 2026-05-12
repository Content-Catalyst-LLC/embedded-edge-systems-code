library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity safety_gate is
    generic (
        ACTION_WIDTH : integer := 4
    );
    port (
        safety_valid     : in  std_logic;
        authority_valid  : in  std_logic;
        confidence_valid : in  std_logic;
        latency_valid    : in  std_logic;
        candidate_action : in  std_logic_vector(ACTION_WIDTH-1 downto 0);
        fallback_action  : in  std_logic_vector(ACTION_WIDTH-1 downto 0);
        filtered_action  : out std_logic_vector(ACTION_WIDTH-1 downto 0);
        allowed          : out std_logic
    );
end safety_gate;

architecture Behavioral of safety_gate is
    signal valid_all : std_logic;
begin
    valid_all <= safety_valid and authority_valid and confidence_valid and latency_valid;
    allowed <= valid_all;
    filtered_action <= candidate_action when valid_all = '1' else fallback_action;
end Behavioral;
