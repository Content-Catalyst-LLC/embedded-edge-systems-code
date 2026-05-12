module interrupt_event_counter (
    input wire clk,
    input wire rst,
    input wire interrupt_event,
    input wire fault_event,
    output reg [31:0] interrupt_count,
    output reg [31:0] fault_count
);
always @(posedge clk) begin
    if (rst) begin
        interrupt_count <= 32'd0;
        fault_count <= 32'd0;
    end else begin
        if (interrupt_event) begin
            interrupt_count <= interrupt_count + 32'd1;
        end
        if (fault_event) begin
            fault_count <= fault_count + 32'd1;
        end
    end
end
endmodule
