module feature_window_counter #(
    parameter COUNT_WIDTH = 16,
    parameter WINDOW_SIZE = 512
)(
    input wire clk,
    input wire rst,
    input wire sample_valid,
    output reg window_ready,
    output reg [COUNT_WIDTH-1:0] sample_count
);

always @(posedge clk) begin
    if (rst) begin
        sample_count <= 0;
        window_ready <= 0;
    end else if (sample_valid) begin
        if (sample_count >= WINDOW_SIZE - 1) begin
            sample_count <= 0;
            window_ready <= 1;
        end else begin
            sample_count <= sample_count + 1'b1;
            window_ready <= 0;
        end
    end else begin
        window_ready <= 0;
    end
end

endmodule
