module telemetry_framer #(
    parameter SCORE_WIDTH = 16
)(
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [SCORE_WIDTH-1:0] confidence_score,
    input wire [7:0] model_version_id,
    input wire [7:0] feature_version_id,
    output reg valid_out,
    output reg [SCORE_WIDTH+16-1:0] telemetry_frame
);

always @(posedge clk) begin
    if (rst) begin
        valid_out <= 0;
        telemetry_frame <= 0;
    end else begin
        valid_out <= valid_in;
        if (valid_in) begin
            telemetry_frame <= {model_version_id, feature_version_id, confidence_score};
        end
    end
end

endmodule
