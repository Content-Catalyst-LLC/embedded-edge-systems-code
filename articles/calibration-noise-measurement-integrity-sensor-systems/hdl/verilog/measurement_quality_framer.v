module measurement_quality_framer #(
    parameter WIDTH = 16
)(
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [WIDTH-1:0] raw_sample,
    input wire saturated,
    input wire sample_valid_window,
    input wire [7:0] quality_state_id,
    output reg valid_out,
    output reg [WIDTH+10-1:0] quality_frame
);
always @(posedge clk) begin
    if (rst) begin
        valid_out <= 0;
        quality_frame <= 0;
    end else begin
        valid_out <= valid_in;
        if (valid_in) begin
            quality_frame <= {quality_state_id, saturated, sample_valid_window, raw_sample};
        end
    end
end
endmodule
