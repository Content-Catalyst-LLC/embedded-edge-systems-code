module sync_pulse_generator #(
    parameter COUNTER_WIDTH = 32,
    parameter PERIOD_TICKS = 1000000
)(
    input wire clk,
    input wire rst,
    output reg sync_pulse
);

reg [COUNTER_WIDTH-1:0] counter;

always @(posedge clk) begin
    if (rst) begin
        counter <= 0;
        sync_pulse <= 0;
    end else begin
        if (counter >= PERIOD_TICKS) begin
            counter <= 0;
            sync_pulse <= 1;
        end else begin
            counter <= counter + 1'b1;
            sync_pulse <= 0;
        end
    end
end

endmodule
