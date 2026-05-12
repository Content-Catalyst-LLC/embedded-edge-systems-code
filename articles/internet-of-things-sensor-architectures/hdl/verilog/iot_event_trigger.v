module iot_event_trigger #(
    parameter WIDTH = 16,
    parameter THRESHOLD = 1000
)(
    input wire clk,
    input wire rst,
    input wire sample_valid,
    input wire [WIDTH-1:0] sample_value,
    output reg event_detected
);
always @(posedge clk) begin
    if (rst) event_detected <= 0;
    else event_detected <= sample_valid && (sample_value >= THRESHOLD);
end
endmodule
