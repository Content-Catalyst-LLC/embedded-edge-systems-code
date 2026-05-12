module wake_event_counter (
    input wire clk,
    input wire rst,
    input wire wake_event,
    input wire false_wake,
    output reg [31:0] wake_count,
    output reg [31:0] false_wake_count
);
always @(posedge clk) begin
    if (rst) begin
        wake_count <= 32'd0;
        false_wake_count <= 32'd0;
    end else begin
        if (wake_event) begin
            wake_count <= wake_count + 32'd1;
        end
        if (false_wake) begin
            false_wake_count <= false_wake_count + 32'd1;
        end
    end
end
endmodule
