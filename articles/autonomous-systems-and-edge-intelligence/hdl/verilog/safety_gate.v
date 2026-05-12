module safety_gate #(
    parameter ACTION_WIDTH = 4
)(
    input wire safety_valid,
    input wire authority_valid,
    input wire confidence_valid,
    input wire latency_valid,
    input wire [ACTION_WIDTH-1:0] candidate_action,
    input wire [ACTION_WIDTH-1:0] fallback_action,
    output wire [ACTION_WIDTH-1:0] filtered_action,
    output wire allowed
);

assign allowed = safety_valid && authority_valid && confidence_valid && latency_valid;
assign filtered_action = allowed ? candidate_action : fallback_action;

endmodule
