module timestamp_counter #(
    parameter WIDTH = 64
)(
    input wire clk,
    input wire rst,
    output reg [WIDTH-1:0] timestamp
);
always @(posedge clk) begin
    if (rst) timestamp <= 0;
    else timestamp <= timestamp + 1'b1;
end
endmodule
