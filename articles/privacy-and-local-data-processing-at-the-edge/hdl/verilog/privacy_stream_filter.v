module privacy_stream_filter #(
    parameter DATA_WIDTH = 16,
    parameter THRESHOLD = 16'd1000
)(
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [DATA_WIDTH-1:0] raw_data_in,
    output reg valid_out,
    output reg event_out
);

always @(posedge clk) begin
    if (rst) begin
        valid_out <= 1'b0;
        event_out <= 1'b0;
    end else begin
        valid_out <= valid_in;
        event_out <= valid_in && (raw_data_in > THRESHOLD);
    end
end

endmodule
