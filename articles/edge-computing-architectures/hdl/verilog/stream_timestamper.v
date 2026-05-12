module stream_timestamper #(parameter DATA_WIDTH=16, parameter TIME_WIDTH=64)(
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [DATA_WIDTH-1:0] data_in,
    input wire [TIME_WIDTH-1:0] timestamp_counter,
    output reg valid_out,
    output reg [DATA_WIDTH-1:0] data_out,
    output reg [TIME_WIDTH-1:0] timestamp_out
);
always @(posedge clk) begin
    if (rst) begin
        valid_out <= 0; data_out <= 0; timestamp_out <= 0;
    end else begin
        valid_out <= valid_in;
        if (valid_in) begin data_out <= data_in; timestamp_out <= timestamp_counter; end
    end
end
endmodule
