module queue_depth_counter (
    input wire clk,
    input wire rst,
    input wire enqueue,
    input wire dequeue,
    output reg [15:0] depth,
    output reg [15:0] high_water_mark
);
always @(posedge clk) begin
    if (rst) begin
        depth <= 16'd0;
        high_water_mark <= 16'd0;
    end else begin
        if (enqueue && !dequeue) begin
            depth <= depth + 16'd1;
        end else if (dequeue && !enqueue && depth > 0) begin
            depth <= depth - 16'd1;
        end

        if (depth > high_water_mark) begin
            high_water_mark <= depth;
        end
    end
end
endmodule
