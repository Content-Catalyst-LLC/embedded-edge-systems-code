module pwm_generator #(
    parameter COUNTER_WIDTH = 16
)(
    input wire clk,
    input wire rst,
    input wire [COUNTER_WIDTH-1:0] duty_cycle,
    output reg pwm_out
);

reg [COUNTER_WIDTH-1:0] counter;

always @(posedge clk) begin
    if (rst) begin
        counter <= 0;
        pwm_out <= 0;
    end else begin
        counter <= counter + 1'b1;
        pwm_out <= counter < duty_cycle;
    end
end

endmodule
