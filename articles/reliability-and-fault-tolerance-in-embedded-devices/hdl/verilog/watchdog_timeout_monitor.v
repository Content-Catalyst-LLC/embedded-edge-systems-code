module watchdog_timeout_monitor #(
    parameter TIMEOUT_CYCLES = 1000000
) (
    input wire clk,
    input wire rst,
    input wire heartbeat,
    output reg timeout,
    output reg [31:0] counter
);
always @(posedge clk) begin
    if (rst) begin
        counter <= 32'd0;
        timeout <= 1'b0;
    end else if (heartbeat) begin
        counter <= 32'd0;
        timeout <= 1'b0;
    end else begin
        if (counter >= TIMEOUT_CYCLES) begin
            timeout <= 1'b1;
        end else begin
            counter <= counter + 32'd1;
        end
    end
end
endmodule
