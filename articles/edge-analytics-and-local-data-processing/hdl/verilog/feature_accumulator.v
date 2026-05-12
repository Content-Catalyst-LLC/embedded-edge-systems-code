module feature_accumulator #(
    parameter DATA_WIDTH = 16,
    parameter ACC_WIDTH = 32
)(
    input wire clk,
    input wire rst,
    input wire sample_valid,
    input wire signed [DATA_WIDTH-1:0] sample,
    input wire window_ready,
    output reg [ACC_WIDTH-1:0] abs_sum,
    output reg [DATA_WIDTH-1:0] peak
);

wire [DATA_WIDTH-1:0] abs_sample = sample[DATA_WIDTH-1] ? (~sample + 1'b1) : sample;

always @(posedge clk) begin
    if (rst || window_ready) begin
        abs_sum <= 0;
        peak <= 0;
    end else if (sample_valid) begin
        abs_sum <= abs_sum + abs_sample;
        if (abs_sample > peak) begin
            peak <= abs_sample;
        end
    end
end

endmodule
