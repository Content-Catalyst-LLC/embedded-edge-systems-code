module adc_valid_window #(
    parameter SETTLING_CYCLES = 50
)(
    input wire clk,
    input wire rst,
    input wire channel_switched,
    output reg sample_valid
);
reg [15:0] counter;

always @(posedge clk) begin
    if (rst) begin
        counter <= 0;
        sample_valid <= 0;
    end else if (channel_switched) begin
        counter <= 0;
        sample_valid <= 0;
    end else if (counter >= SETTLING_CYCLES) begin
        sample_valid <= 1;
    end else begin
        counter <= counter + 1'b1;
        sample_valid <= 0;
    end
end

endmodule
