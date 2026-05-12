module adc_sampler #(
    parameter SAMPLE_WIDTH = 12
)(
    input wire clk,
    input wire rst,
    input wire sample_valid,
    input wire [SAMPLE_WIDTH-1:0] adc_data,
    output reg [SAMPLE_WIDTH-1:0] sample_out,
    output reg sample_ready
);

always @(posedge clk) begin
    if (rst) begin
        sample_out <= 0;
        sample_ready <= 0;
    end else begin
        if (sample_valid) begin
            sample_out <= adc_data;
            sample_ready <= 1;
        end else begin
            sample_ready <= 0;
        end
    end
end

endmodule
