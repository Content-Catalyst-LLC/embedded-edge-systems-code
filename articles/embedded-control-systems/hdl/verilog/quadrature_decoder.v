module quadrature_decoder (
    input wire clk,
    input wire rst,
    input wire enc_a,
    input wire enc_b,
    output reg signed [31:0] position_count
);

reg [1:0] previous;
reg [1:0] current;

always @(posedge clk) begin
    if (rst) begin
        previous <= 2'b00;
        current <= 2'b00;
        position_count <= 0;
    end else begin
        previous <= current;
        current <= {enc_a, enc_b};

        case ({previous, current})
            4'b0001, 4'b0111, 4'b1110, 4'b1000: position_count <= position_count + 1;
            4'b0010, 4'b1011, 4'b1101, 4'b0100: position_count <= position_count - 1;
            default: position_count <= position_count;
        endcase
    end
end

endmodule
