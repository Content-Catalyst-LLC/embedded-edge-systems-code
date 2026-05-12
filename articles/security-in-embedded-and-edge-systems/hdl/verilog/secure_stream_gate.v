module secure_stream_gate #(
    parameter DATA_WIDTH = 16
)(
    input wire clk,
    input wire rst,
    input wire trust_valid,
    input wire valid_in,
    input wire [DATA_WIDTH-1:0] data_in,
    output reg valid_out,
    output reg [DATA_WIDTH-1:0] data_out
);

always @(posedge clk) begin
    if (rst) begin
        valid_out <= 1'b0;
        data_out <= {DATA_WIDTH{1'b0}};
    end else begin
        valid_out <= valid_in && trust_valid;
        data_out <= trust_valid ? data_in : {DATA_WIDTH{1'b0}};
    end
end

endmodule
