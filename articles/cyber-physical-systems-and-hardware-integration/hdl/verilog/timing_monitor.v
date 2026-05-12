module timing_monitor #(
    parameter COUNTER_WIDTH = 32,
    parameter DEADLINE_TICKS = 150000
)(
    input wire clk,
    input wire rst,
    input wire loop_start,
    input wire loop_done,
    output reg deadline_violation
);

reg [COUNTER_WIDTH-1:0] counter;
reg active;

always @(posedge clk) begin
    if (rst) begin
        counter <= 0;
        active <= 0;
        deadline_violation <= 0;
    end else begin
        if (loop_start) begin
            active <= 1;
            counter <= 0;
            deadline_violation <= 0;
        end else if (loop_done) begin
            active <= 0;
        end else if (active) begin
            counter <= counter + 1'b1;
            if (counter >= DEADLINE_TICKS) begin
                deadline_violation <= 1;
                active <= 0;
            end
        end
    end
end

endmodule
