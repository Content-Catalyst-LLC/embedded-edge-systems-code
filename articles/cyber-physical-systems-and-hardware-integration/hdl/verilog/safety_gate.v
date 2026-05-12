module safety_gate #(
    parameter COMMAND_WIDTH = 16
)(
    input wire sensor_valid,
    input wire timing_valid,
    input wire thermal_valid,
    input wire uncertainty_valid,
    input wire interface_valid,
    input wire [COMMAND_WIDTH-1:0] candidate_command,
    input wire [COMMAND_WIDTH-1:0] fallback_command,
    output wire [COMMAND_WIDTH-1:0] filtered_command,
    output wire allowed
);

assign allowed = sensor_valid && timing_valid && thermal_valid && uncertainty_valid && interface_valid;
assign filtered_command = allowed ? candidate_command : fallback_command;

endmodule
