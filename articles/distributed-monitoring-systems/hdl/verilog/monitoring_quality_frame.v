module monitoring_quality_frame #(
    parameter DATA_WIDTH = 16,
    parameter TIME_WIDTH = 64
)(
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [DATA_WIDTH-1:0] value_in,
    input wire [TIME_WIDTH-1:0] timestamp_in,
    input wire [7:0] quality_state_id,
    input wire [7:0] coverage_zone_id,
    input wire queue_pressure,
    output reg valid_out,
    output reg [DATA_WIDTH+TIME_WIDTH+17-1:0] frame_out
);
always @(posedge clk) begin
    if (rst) begin
        valid_out <= 0;
        frame_out <= 0;
    end else begin
        valid_out <= valid_in;
        if (valid_in) begin
            frame_out <= {quality_state_id, coverage_zone_id, queue_pressure, timestamp_in, value_in};
        end
    end
end
endmodule
