module timing_monitor #(
    parameter COUNTER_WIDTH = 32,
    parameter DEADLINE_TICKS = 80000
)(
    input wire clk,
    input wire rst,
    input wire start,
    input wire done,
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
        if (start) begin
            active <= 1;
            counter <= 0;
            deadline_violation <= 0;
        end else if (done) begin
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
