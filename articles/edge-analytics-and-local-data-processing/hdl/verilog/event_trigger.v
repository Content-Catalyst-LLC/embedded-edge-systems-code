module event_trigger #(
    parameter FEATURE_WIDTH = 16,
    parameter THRESHOLD = 1000
)(
    input wire clk,
    input wire rst,
    input wire feature_valid,
    input wire [FEATURE_WIDTH-1:0] feature_value,
    output reg event_detected
);

always @(posedge clk) begin
    if (rst) begin
        event_detected <= 0;
    end else begin
        event_detected <= feature_valid && (feature_value >= THRESHOLD);
    end
end

endmodule
