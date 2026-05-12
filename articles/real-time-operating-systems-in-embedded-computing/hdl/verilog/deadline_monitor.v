module deadline_monitor (
    input wire clk,
    input wire rst,
    input wire task_active,
    input wire task_complete,
    input wire [31:0] deadline_cycles,
    output reg deadline_missed,
    output reg [31:0] elapsed_cycles
);
always @(posedge clk) begin
    if (rst) begin
        deadline_missed <= 1'b0;
        elapsed_cycles <= 32'd0;
    end else if (task_active && !task_complete) begin
        elapsed_cycles <= elapsed_cycles + 32'd1;
        if (elapsed_cycles > deadline_cycles) begin
            deadline_missed <= 1'b1;
        end
    end else if (task_complete) begin
        elapsed_cycles <= 32'd0;
    end
end
endmodule
