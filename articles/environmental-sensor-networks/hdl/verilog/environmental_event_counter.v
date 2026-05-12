module environmental_event_counter (
    input wire clk,
    input wire rst,
    input wire sample_valid,
    input wire event_trigger,
    output reg [31:0] sample_count,
    output reg [31:0] event_count
);
always @(posedge clk) begin
    if (rst) begin
        sample_count <= 32'd0;
        event_count <= 32'd0;
    end else begin
        if (sample_valid) begin
            sample_count <= sample_count + 32'd1;
        end
        if (event_trigger) begin
            event_count <= event_count + 32'd1;
        end
    end
end
endmodule
