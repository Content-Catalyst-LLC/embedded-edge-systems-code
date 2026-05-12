library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity safety_gate is
    generic (
        COMMAND_WIDTH : integer := 16
    );
    port (
        sensor_valid      : in  std_logic;
        timing_valid      : in  std_logic;
        thermal_valid     : in  std_logic;
        uncertainty_valid : in  std_logic;
        interface_valid   : in  std_logic;
        candidate_command : in  std_logic_vector(COMMAND_WIDTH-1 downto 0);
        fallback_command  : in  std_logic_vector(COMMAND_WIDTH-1 downto 0);
        filtered_command  : out std_logic_vector(COMMAND_WIDTH-1 downto 0);
        allowed           : out std_logic
    );
end safety_gate;

architecture Behavioral of safety_gate is
    signal valid_all : std_logic;
begin
    valid_all <= sensor_valid and timing_valid and thermal_valid and uncertainty_valid and interface_valid;
    allowed <= valid_all;
    filtered_command <= candidate_command when valid_all = '1' else fallback_command;
end Behavioral;
