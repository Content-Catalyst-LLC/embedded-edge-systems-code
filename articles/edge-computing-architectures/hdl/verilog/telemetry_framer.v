module telemetry_framer #(parameter WIDTH=16)(
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [WIDTH-1:0] latency_ms,
    input wire [WIDTH-1:0] buffer_backlog,
    input wire [7:0] trust_state_id,
    input wire [7:0] runtime_state_id,
    output reg valid_out,
    output reg [WIDTH*2+16-1:0] telemetry_frame
);
always @(posedge clk) begin
    if (rst) begin valid_out <= 0; telemetry_frame <= 0; end
    else begin
        valid_out <= valid_in;
        if (valid_in) telemetry_frame <= {trust_state_id, runtime_state_id, latency_ms, buffer_backlog};
    end
end
endmodule
