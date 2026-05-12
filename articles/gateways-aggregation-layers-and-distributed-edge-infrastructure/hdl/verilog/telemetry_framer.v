module telemetry_framer #(
    parameter DATA_WIDTH = 16
)(
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [DATA_WIDTH-1:0] feature_value,
    input wire [7:0] gateway_id,
    input wire [7:0] policy_version_id,
    output reg valid_out,
    output reg [DATA_WIDTH+16-1:0] telemetry_frame
);

always @(posedge clk) begin
    if (rst) begin
        valid_out <= 0;
        telemetry_frame <= 0;
    end else begin
        valid_out <= valid_in;
        if (valid_in) begin
            telemetry_frame <= {gateway_id, policy_version_id, feature_value};
        end
    end
end

endmodule
