module watchdog_heartbeat #(parameter COUNTER_WIDTH=32, parameter HEARTBEAT_PERIOD=1000000)(
    input wire clk,
    input wire rst,
    output reg heartbeat
);
reg [COUNTER_WIDTH-1:0] counter;
always @(posedge clk) begin
    if (rst) begin counter <= 0; heartbeat <= 0; end
    else if (counter >= HEARTBEAT_PERIOD) begin counter <= 0; heartbeat <= ~heartbeat; end
    else counter <= counter + 1'b1;
end
endmodule
