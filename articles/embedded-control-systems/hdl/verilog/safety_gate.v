module safety_gate #(
    parameter COMMAND_WIDTH = 16
)(
    input wire safety_valid,
    input wire timing_valid,
    input wire thermal_valid,
    input wire current_valid,
    input wire [COMMAND_WIDTH-1:0] candidate_command,
    input wire [COMMAND_WIDTH-1:0] fallback_command,
    output wire [COMMAND_WIDTH-1:0] filtered_command,
    output wire allowed
);

assign allowed = safety_valid && timing_valid && thermal_valid && current_valid;
assign filtered_command = allowed ? candidate_command : fallback_command;

endmodule
